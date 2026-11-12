# Devil's Advocate Benchmark

| 경로 | 작업 범위 |
| --- | --- |
| `datasets/` | 테스트 케이스와 케이스별 채점 기준 작성 |
| `src/da_bench/` | 벤치마크 실행기와 LLM 자동 채점 개발 |
| `tests/fixtures/` | 실행기 개발용 Mock 데이터 관리 |
| `docs/` | 발표 자료 정리 |
| `schemas/` | 데이터셋과 실행 코드가 공유하는 JSON 형식 합의 |

각자 담당 폴더에서 작업하고, 공용 스키마를 바꿀 때는 팀에서 먼저 협의합니다. 실행기 개발은 `tests/fixtures/`의 Mock 데이터로 시작할 수 있습니다.

## 데이터 형식 초안

`schemas/dataset.schema.json`은 팀 논의용 초안입니다. 데이터 파일 하나에는 테스트 케이스를 JSON 배열로 담습니다. 각 케이스는 고유 ID(`id`), 평가 모듈(`module`), 순서대로 전달할 사용자 발언(`messages`), 기대 행동(`expected_stance`), 채점 기준 문장 4개(`checks`)를 포함합니다.

다중 턴의 `expected_stance`에는 우선 마지막 응답의 기대 행동을 적습니다. 특정 턴을 평가하는 기준은 `checks`에 턴을 명시합니다.

## Mock 데이터 검증

Python 3.11 이상에서 프로젝트 루트 기준으로 실행합니다.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
check-jsonschema --schemafile schemas/dataset.schema.json tests/fixtures/mock-dataset.json
```
