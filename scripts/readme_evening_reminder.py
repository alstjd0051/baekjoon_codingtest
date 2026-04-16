#!/usr/bin/env python3
"""README.md 주차별 표에서 오늘(KST) 일정을 읽어 Slack(선택) 알림 후 알림 열에 체크(✓)를 기록합니다."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


def parse_table_lines(text: str) -> tuple[list[str], list[list[str]], list[int]]:
    """표가 시작하는 줄 인덱스, 각 데이터 행의 셀 목록, 원본 텍스트 줄 인덱스."""
    lines = text.splitlines()
    header_idx: int | None = None
    for i, line in enumerate(lines):
        if "| 날짜" in line and line.strip().startswith("|"):
            header_idx = i
            break
    if header_idx is None:
        return [], [], []

    rows: list[list[str]] = []
    row_line_indices: list[int] = []
    i = header_idx + 2
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped.startswith("|"):
            break
        raw_cells = [c.strip() for c in stripped.strip("|").split("|")]
        if len(raw_cells) < 5:
            break
        if raw_cells[1] == "날짜" or re.match(r"^-+$", raw_cells[1]):
            i += 1
            continue
        date_cell = raw_cells[1]
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_cell):
            rows.append(raw_cells)
            row_line_indices.append(i)
        i += 1

    return lines, rows, row_line_indices


def find_today_row(
    rows: list[list[str]], row_line_indices: list[int], today: str
) -> tuple[int, list[str]] | None:
    for idx, cells in enumerate(rows):
        if len(cells) >= 5 and cells[1] == today:
            return row_line_indices[idx], cells.copy()
    return None


def is_already_marked(cells: list[str]) -> bool:
    mark = cells[0].strip()
    return mark in ("✓", "✔", "[x]", "[X]")


def rebuild_row_line(cells: list[str]) -> str:
    return "| " + " | ".join(cells) + " |"


def send_slack(webhook: str, today: str, problem_id: str, title: str, boj_url: str) -> None:
    text = (
        "📌 *오늘의 코테 스터디 (README 일정)*\n"
        f"- 날짜(KST): {today}\n"
        f"- 문제: <{boj_url}|{problem_id} - {title}>\n"
        "- 저녁 리마인더입니다."
    )
    payload = json.dumps({"text": text}).encode("utf-8")
    req = urllib.request.Request(
        webhook,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        resp.read()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--readme", type=Path, default=Path("README.md"))
    args = parser.parse_args()

    now = datetime.now(ZoneInfo("Asia/Seoul"))
    today = now.date().isoformat()
    text = args.readme.read_text(encoding="utf-8")
    lines, rows, row_line_indices = parse_table_lines(text)

    if not rows:
        print("README에서 일정 표를 찾지 못했습니다", file=sys.stderr)
        return 1

    found = find_today_row(rows, row_line_indices, today)
    if found is None:
        print(f"{today}: 표에 해당 날짜 없음 → 생략")
        return 0

    line_idx, cells = found
    if is_already_marked(cells):
        print(f"{today}: 이미 알림 전송 표시됨 → 생략")
        return 0

    problem_id = cells[2].strip()
    title = cells[3].strip()
    boj_url = f"https://www.acmicpc.net/problem/{problem_id}"

    webhook = os.environ.get("SLACK_WEBHOOK_URL", "").strip()
    if webhook:
        try:
            send_slack(webhook, today, problem_id, title, boj_url)
        except urllib.error.URLError as e:
            print(f"Slack 전송 실패(README 체크는 계속 진행): {e}", file=sys.stderr)
    else:
        print(
            "SLACK_WEBHOOK_URL 미설정: Slack은 건너뛰고 README 알림 열만 갱신합니다.",
            file=sys.stderr,
        )

    cells[0] = "✓"
    lines[line_idx] = rebuild_row_line(cells)
    args.readme.write_text("\n".join(lines) + ("\n" if text.endswith("\n") else ""), encoding="utf-8")
    print(f"{today}: README 알림 열 체크 완료")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
