# 6324 풀이

URL 형식은 `protocol://host[:port][/path]` 이므로 구분자를 순서대로 잘라서 각 항목을 얻으면 된다.

- 먼저 `://` 기준으로 `protocol`과 나머지 문자열 분리
- 나머지에서 `/`가 있으면 `host[:port]`와 `path` 분리, 없으면 `path=<default>`
- `host[:port]`에서 `:`가 있으면 `host`, `port` 분리, 없으면 `port=<default>`
- 출력은 문제에서 요구한 라벨(`Protocol`, `Host`, `Port`, `Path`)과 공백 형식 유지
