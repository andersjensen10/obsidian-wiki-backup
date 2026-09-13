---
tags: [benchmarking, storage, spark-infra]
status: blocked
---

# Storage and Runtime

## Intended Toshiba layout

Target mount: `/media/aj/TOSHIBA EXT` (device `/dev/sdb1`, NTFS label `TOSHIBA EXT`). The drive has not mounted successfully: the NTFS volume is marked dirty and the normal mount was refused. Do not force-mount or repair it automatically; resolve with AJ, a safe Windows `chkdsk`, or an explicitly approved repair procedure first.

After mounting, use a dedicated layout:

```text
/media/aj/TOSHIBA EXT/LLM-Library/
├── models/              # GGUF files, one directory per model/revision
├── manifests/           # checksums, model cards, download metadata
├── server-profiles/     # reproducible llama.cpp launch profiles
├── runs/                # raw benchmark outputs and logs
└── quarantine/          # incomplete or failed downloads
```

Keep only manifests and links in Obsidian; large model files and raw logs stay on Toshiba. Every completed model file gets a SHA-256 checksum and download source/revision record.

## Integrity follow-up — 2026-09-13

A read-only audit found the NTFS volume still reported dirty after `ntfsfix`, and traversal encountered an I/O error under an existing temporary model path. AJ has since repaired/reconnected the drive. It is now mounted read-write at `/media/aj/TOSHIBA EXT1` with about 911 GB free; the model library is present and a temporary write/read/delete test passed. The mountpoint suffix `EXT1` is the active path and must be used by automation. Kernel logs still contain dirty-volume warnings from the mount attempt, so continue monitoring for new I/O errors and do not delete existing data automatically.

The previous local staging path remains available as fallback. Persistent mounting and SMART/enclosure health checks remain follow-up work. If new I/O errors appear, stop downloads, preserve/copy high-value data, and perform a clean unmount plus approved filesystem repair rather than force-mounting.
## Production safety

Benchmark candidates in an isolated server profile/port where possible. Never restart the production llama.cpp service for a benchmark without an explicit approved maintenance window. Capture the current service command and rollback command before any swap. A promotion is a separate, verified operation after AJ reviews the report.

## Current Spark baseline

The live llama.cpp server is on port 8014 with two parallel slots and Qwen 3.8 Q5 plus a speculative draft model. Existing model directories are under `/home/aj/llama-models`; do not migrate or delete them as part of benchmark setup.
