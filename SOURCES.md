# Source and decision record

## Sources actually read

1. `Devil's Advocate 벤치마크 개발 방향 초안.md`: logical flaws, counterargument validity, context, multi-turn response, fixed scripts and mixed evaluation.
2. `DA-Bench.docx`: S0–S3 proposal, minimal pairs, contradiction versus scope changes, evidence versus pressure, simple baseline strategies, human calibration.
3. `Devils_Advocate_벤치마크_제안서.docx`: modules A–F, decision-relevant questions, issue-state tracking, item rubrics, family split, blinded evaluation and auditing.
4. `Ch03_Evaluating_LLMs.pdf`, all 67 PDF pages: especially PDF pp. 9–10 (closed-ended), 19–26 (open-ended and evaluation choices), 28–30 (implementation and contamination), 39–42 (private tests and Goodhart), 46 (trajectory and outcome), 59–61 (protocol, reward hacking and validity).
5. User’s Phase 2 assignment and consolidated team notes in this conversation.

## Video access limitation

`34.mp4` exists locally and in the supplied materials. The video had no extractable transcript in the file reader. Browser playback was blocked by the Windows URL-verification restriction, and a separate local media-decoding attempt did not expose video metadata. **The video was not independently watched or transcribed.** Its goals in the slides are attributed to the detailed team proposal’s explicit account of video slides 03–06. An exact audiovisual cross-check remains outstanding. No invented video transcript is included.

## Decisions made for the implementation

| Proposal or question | Implemented decision | Reason |
|---|---|---|
| Include B and F? | Include both | They operationalize useful questioning and cumulative decision review. |
| 120 cases or larger S1–S3 plan | 48-case pilot, 12 development / 36 evaluation | Deliver inspectable runnable coverage while retaining six modules. |
| Four checks per case | Four checks at each turn, then average within case | Preserve trajectory errors and keep equal case weight. |
| Label matching | Blind extraction from natural language, then deterministic comparison | Do not reward self-reported labels or keyword matching. |
| LLM + human grading | Command-based judge integration, exported jobs, human review UI | Provider-independent and executable without credentials. |
| Primary metrics | Six module scores + equal-weight total + four diagnostics | Match the user’s consolidated scope. |
| Model benchmarks | Software fixtures only in this delivery | No model endpoint or credentials were supplied and no real-agent result is fabricated. |
| 15-minute presentation | 15 English slides, bilingual alternative notes, 900-second schedule | Suitable for either English or Korean delivery. |

The original proposals’ external paper links and performance statements were not independently verified or reused as established findings. All case numbers, thresholds, weights and pilot results are identified as this implementation’s choices. Main presentation references use source files and page/section locations rather than unsupported claims of published validation.
