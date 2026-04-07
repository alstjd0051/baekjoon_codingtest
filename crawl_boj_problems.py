"""README 문제 목록을 기반으로 백준 문제를 크롤링합니다."""
from __future__ import annotations

import argparse
import csv
import re
import time
from dataclasses import dataclass
from html import unescape
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
DEFAULT_README = ROOT / "README.md"
DEFAULT_SCHEDULE_CSV = (
    ROOT / "assets" / "[AI 24기] 코딩테스트 스터디 일정 - 24기 _ 코테 스터디.csv"
)
DEFAULT_OUTPUT = ROOT / "docs" / "problems.md"
DEFAULT_DOCS_DIR = ROOT / "docs" / "problems"

ROW_PATTERN = re.compile(
    r"^\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*\[바로가기\]\((https://www\.acmicpc\.net/problem/\d+)\)\s*\|$"
)
SECTION_IDS = {
    "description": "problem_description",
    "input": "problem_input",
    "output": "problem_output",
}
TITLE_PATTERN = re.compile(r"<title>\s*(.*?)\s*</title>", re.IGNORECASE | re.DOTALL)
LIMIT_PATTERN = re.compile(
    r'<table[^>]*id="problem-info"[^>]*>(.*?)</table>',
    re.IGNORECASE | re.DOTALL,
)
SECTION_PATTERN_TEMPLATE = r'<div[^>]*id="{section_id}"[^>]*>(.*?)</div>'
TAG_PATTERN = re.compile(r"<[^>]+>")
WS_PATTERN = re.compile(r"\s+")


@dataclass
class ProblemItem:
    date: str
    problem_id: str
    title_in_readme: str
    url: str
    title_in_boj: str
    description: str
    input_desc: str
    output_desc: str
    limit_text: str


def parse_readme_table(readme_text: str) -> list[tuple[str, str, str, str]]:
    items: list[tuple[str, str, str, str]] = []
    for raw_line in readme_text.splitlines():
        line = raw_line.strip()
        match = ROW_PATTERN.match(line)
        if match is None:
            continue
        items.append(match.groups())
    return items


def _extract_study_year(csv_text: str) -> int:
    match = re.search(r"(\d{4})\.\d{1,2}\.\d{1,2}\s*-\s*(\d{4})\.\d{1,2}\.\d{1,2}", csv_text)
    if match:
        return int(match.group(1))
    return 2026


def parse_csv_schedule(csv_path: Path) -> list[tuple[str, str, str, str]]:
    text = csv_path.read_text(encoding="utf-8-sig")
    year = _extract_study_year(text)
    rows = list(csv.reader(text.splitlines()))
    items: list[tuple[str, str, str, str]] = []

    for idx, row in enumerate(rows):
        if "일자" not in row:
            continue
        date_idx = row.index("일자")
        if idx + 1 >= len(rows):
            continue
        problem_row = rows[idx + 1]
        if "문제" not in problem_row:
            continue
        problem_idx = problem_row.index("문제")

        for offset in range(1, 8):
            if date_idx + offset >= len(row) or problem_idx + offset >= len(problem_row):
                continue
            date_cell = row[date_idx + offset].strip()
            problem_cell = problem_row[problem_idx + offset].strip()
            if not date_cell or not problem_cell:
                continue

            date_match = re.fullmatch(r"(\d{1,2})/(\d{1,2})", date_cell)
            problem_match = re.fullmatch(r"(.*?)\((\d+)\)", problem_cell)
            if date_match is None or problem_match is None:
                continue

            month, day = int(date_match.group(1)), int(date_match.group(2))
            title = problem_match.group(1).strip()
            problem_id = problem_match.group(2).strip()
            iso_date = f"{year:04d}-{month:02d}-{day:02d}"
            url = f"https://www.acmicpc.net/problem/{problem_id}"
            items.append((iso_date, problem_id, title, url))

    unique = sorted({item[0]: item for item in items}.values(), key=lambda x: x[0])
    return unique


def strip_html(html: str) -> str:
    text = TAG_PATTERN.sub(" ", html)
    text = unescape(text)
    text = WS_PATTERN.sub(" ", text)
    return text.strip()


def extract_section(html: str, section_id: str) -> str:
    pattern = re.compile(
        SECTION_PATTERN_TEMPLATE.format(section_id=re.escape(section_id)),
        re.IGNORECASE | re.DOTALL,
    )
    match = pattern.search(html)
    if match is None:
        return ""
    return strip_html(match.group(1))


def fetch_html(url: str, timeout: float) -> str:
    request = Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/123.0.0.0 Safari/537.36"
            )
        },
    )
    with urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def parse_problem_html(
    html: str, date: str, problem_id: str, title_in_readme: str, url: str
) -> ProblemItem:
    title_match = TITLE_PATTERN.search(html)
    title_in_boj = strip_html(title_match.group(1)) if title_match else ""
    if " - " in title_in_boj:
        title_in_boj = title_in_boj.split(" - ", 1)[0].strip()

    limit_match = LIMIT_PATTERN.search(html)
    limit_text = strip_html(limit_match.group(1)) if limit_match else ""

    return ProblemItem(
        date=date,
        problem_id=problem_id,
        title_in_readme=title_in_readme.strip(),
        url=url,
        title_in_boj=title_in_boj,
        description=extract_section(html, SECTION_IDS["description"]),
        input_desc=extract_section(html, SECTION_IDS["input"]),
        output_desc=extract_section(html, SECTION_IDS["output"]),
        limit_text=limit_text,
    )


def build_problem_markdown(item: ProblemItem) -> str:
    lines = [
        f"# BOJ {item.problem_id} - {item.title_in_boj or item.title_in_readme}",
        "",
        f"- 날짜: `{item.date}`",
        f"- 문제 번호: `{item.problem_id}`",
        f"- 원문 링크: {item.url}",
        "",
        "## 문제 설명",
        "",
        item.description or "(설명 없음)",
        "",
        "## 입력",
        "",
        item.input_desc or "(입력 설명 없음)",
        "",
        "## 출력",
        "",
        item.output_desc or "(출력 설명 없음)",
        "",
        "## 제한",
        "",
        item.limit_text or "(제한 정보 없음)",
        "",
    ]
    return "\n".join(lines)


def write_problem_markdown_files(items: list[ProblemItem], docs_dir: Path) -> None:
    docs_dir.mkdir(parents=True, exist_ok=True)
    for item in items:
        path = docs_dir / f"{item.problem_id}.md"
        path.write_text(build_problem_markdown(item), encoding="utf-8")


def build_summary_markdown(
    source: str,
    readme_path: Path,
    schedule_csv_path: Path,
    target_date: str | None,
    items: list[ProblemItem],
    errors: list[str],
) -> str:
    lines = [
        "# 크롤링 결과",
        "",
        "## 문제 목록",
        "",
        "| 날짜 | 문제 번호 | 문제명 | 링크 | 문서 |",
        "| --- | --- | --- | --- | --- |",
    ]

    for item in items:
        lines.append(
            f"| {item.date} | {item.problem_id} | {item.title_in_readme} | "
            f"[바로가기]({item.url}) | `docs/problems/{item.problem_id}.md` |"
        )

    if errors:
        lines.extend(["", "## 오류", ""])
        for err in errors:
            lines.append(f"- {err}")
    lines.append("")
    return "\n".join(lines)


def crawl(
    source: str,
    readme_path: Path,
    schedule_csv_path: Path,
    target_date: str | None,
    output_path: Path,
    docs_dir: Path | None,
    delay: float,
    timeout: float,
    fail_fast: bool,
) -> int:
    if source == "csv":
        rows = parse_csv_schedule(schedule_csv_path)
    else:
        readme_text = readme_path.read_text(encoding="utf-8")
        rows = parse_readme_table(readme_text)

    if target_date:
        rows = [row for row in rows if row[0] == target_date]

    if not rows:
        raise ValueError("크롤링할 일정이 없습니다. source/target-date 설정을 확인하세요.")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    results: list[ProblemItem] = []
    errors: list[str] = []

    for index, (date, problem_id, title_in_readme, url) in enumerate(rows, start=1):
        print(f"[{index}/{len(rows)}] 크롤링 중: {problem_id} - {title_in_readme.strip()}")
        try:
            html = fetch_html(url, timeout=timeout)
            results.append(
                parse_problem_html(html, date, problem_id, title_in_readme, url)
            )
        except (HTTPError, URLError, TimeoutError, ValueError) as exc:
            message = f"{problem_id} 실패: {exc}"
            errors.append(message)
            print(f"  ! {message}")
            if fail_fast:
                break

        if delay > 0:
            time.sleep(delay)

    output_path.write_text(
        build_summary_markdown(
            source=source,
            readme_path=readme_path,
            schedule_csv_path=schedule_csv_path,
            target_date=target_date,
            items=results,
            errors=errors,
        ),
        encoding="utf-8",
    )
    if docs_dir is not None:
        write_problem_markdown_files(results, docs_dir)
    print(f"\n저장 완료: {output_path}")
    if docs_dir is not None:
        print(f"문제별 문서 저장: {docs_dir}")
    print(f"성공 {len(results)}건 / 실패 {len(errors)}건")
    return 0 if not errors else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="README 문제 목록을 읽어 백준 문제 페이지를 크롤링합니다."
    )
    parser.add_argument(
        "--source",
        choices=["readme", "csv"],
        default="readme",
        help="일정 소스 선택 (기본값: readme)",
    )
    parser.add_argument(
        "--readme",
        type=Path,
        default=DEFAULT_README,
        help=f"문제 목록이 있는 README 경로 (기본값: {DEFAULT_README})",
    )
    parser.add_argument(
        "--schedule-csv",
        type=Path,
        default=DEFAULT_SCHEDULE_CSV,
        help=f"일정 CSV 경로 (기본값: {DEFAULT_SCHEDULE_CSV})",
    )
    parser.add_argument(
        "--target-date",
        type=str,
        default=None,
        help="특정 날짜만 크롤링 (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"크롤링 결과 JSON 저장 경로 (기본값: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--docs-dir",
        type=Path,
        default=DEFAULT_DOCS_DIR,
        help=(
            "문제별 Markdown 저장 디렉터리 "
            f"(기본값: {DEFAULT_DOCS_DIR}, 비활성화: --docs-dir none)"
        ),
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.2,
        help="요청 간 대기 시간(초). 서버 부하 완화를 위해 기본 0.2초",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=10.0,
        help="각 요청 타임아웃(초)",
    )
    parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="첫 실패에서 즉시 중단",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    docs_dir: Path | None
    if str(args.docs_dir).lower() == "none":
        docs_dir = None
    else:
        docs_dir = args.docs_dir
    return crawl(
        source=args.source,
        readme_path=args.readme,
        schedule_csv_path=args.schedule_csv,
        target_date=args.target_date,
        output_path=args.output,
        docs_dir=docs_dir,
        delay=args.delay,
        timeout=args.timeout,
        fail_fast=args.fail_fast,
    )


if __name__ == "__main__":
    raise SystemExit(main())
