# 02:30 readiness — 2026-09-15

Status: **BLOCKED**

## Exact gate

The selected candidate, `Qwen/Qwen3-Coder-30B-A3B-Instruct` / `AtomicChat/Qwen3-Coder-30B-A3B-GGUF` / `qwen3-coder-30b-a3b-Q4_K_M.gguf`, is not locally available. No candidate file, revision, or checksum-backed manifest was found. The dedicated isolated candidate server profile is also missing. No download was started.

The 04:00 benchmark slot is consumed by this blocked readiness. The next normal cycle must start from a fresh preflight; no catch-up benchmark is scheduled.

## Gate results

- **Toshiba:** identified as `/dev/sdb1`, serial `35DQP0GHT`, UUID `C6686E4C686E3AF7`; mounted read-write at `/media/aj/TOSHIBA EXT1`; 977,833,627,648 bytes free (48%); temporary write/read/delete passed. Historical NTFS dirty-volume warnings remain in kernel logs; no current I/O error was observed.
- **Fallback:** `/home/aj/llm-benchmark-local` temporary write/read/delete passed; 244,171,907,072 bytes free.
- **Runner tests:** PASS — `3 passed in 0.00s` using `/home/aj/llm-benchmark-runner/.venv/bin/pytest -q`.
- **Suite:** PASS — `/home/aj/llm-benchmark-runner/suite.json`, locked `1.0.0`, 10 cases, C1/C2/C4.
- **llama-server:** present — build 931, commit `4df29be4f4c3673f428170fda944a5b19f743bb`.
- **Production:** PASS — `192.168.0.139:8014/health` returned HTTP 200 and `{"status":"ok"}`; alias remains `qwen3.8-27b-aggressive-q5`; PID 3517121 unchanged. Production was not touched.
- **Candidate metadata:** research identifies `Q4_K_M` and an estimated 18.56 GB file, but local revision and checksum are unavailable.
- **Isolated profile:** BLOCKED — no profile found under `/media/aj/TOSHIBA EXT1/LLM-Library/server-profiles`, `/home/aj/llm-benchmark-runner/profiles`, or `/home/aj/llm-benchmark-runner/server-profiles`.

Full machine-readable evidence: [`readiness.json`](readiness.json).

## Safety actions

No download, repair, restart, production swap, benchmark, or catch-up scheduling was performed. No partial file is treated as a candidate.
