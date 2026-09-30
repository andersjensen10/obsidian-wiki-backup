# Chiana Robust Harvest Plan

## What went wrong last time

During the 17:03–19:03 timebox, I ran 50+ web searches and extracted ~144KB of raw data. But **I never wrote it back into the vault**. The data sat in cache spillover files.

The core failure: **harvest → cache, not harvest → cache → merge → update → verify.**

---

## The correct workflow (for future timeboxes)

### Phase 1: Audit (first 10 minutes)

1. **Count existing files** — `find` the target character directory, count files by type.
2. **Read current dossier** — get the full file, note sections needing data.
3. **Read supporting files** — production credits, interviews, media provenance. Note placeholders.
4. **Check cache** — list spillover/cache files from previous runs.
5. **Map gaps** — compare existing content against canonical appearance list. Flag episodes without dedicated notes.

**Output**: Gap analysis table listing every section/file needing data.

### Phase 2: Harvest (parallel, 30 minutes)

Run **3–4 parallel extraction batches**, not 50 individual searches:

| Batch | Target | Strategy |
|-------|--------|----------|
| A | **Analysis & criticism** | Farscape Continues, Bibble.org, Reactor, TerraFermasCapers |
| B | **Actor interviews** | The Companion, Little Review, podcasts, convention panels |
| C | **Episode guides** | epguides, Snurcher, fandom wiki appearance lists |
| D | **Comics & tie-ins** | BOOM! Studios wiki, comic summaries, graphic novels |

Hard limit: 4 batches, 2 extractions per batch. If a batch yields <1KB, pivot or skip.

### Phase 3: Merge (40 minutes — **critical phase**)

Write extracted data back into vault files using `patch`:

1. Read the full target file.
2. Identify which new data points belong where.
3. Apply `patch` for each section update.
4. Update the `updated:` timestamp.
5. Add new source citations at the end.

**Merge order**: Main dossier → interview files → production notes → media provenance → comics/episodes

### Phase 4: Verify (20 minutes)

1. **File-level check**: Read each modified file end-to-end. No content lost, citations real, no duplicates.
2. **Gap check**: Count remaining evidence gaps. Update the list.
3. **Cache check**: Archive spillover files to `Curator/Research Harvests/`.
4. **Final report**: One-page summary of what changed, what remains, what's next.

### Phase 5: Plan next run (20 minutes)

Before the timebox ends, write a TODO:
- Which gaps are highest-value?
- Which episodes need dedicated notes?
- What can be done independently (comics, episode-specific notes)?

---

## Timebox allocation (2 hours)

| Phase | Duration | Priority |
|-------|----------|----------|
| 1. Audit | 10 min | Critical |
| 2. Harvest | 30 min | High |
| 3. Merge | 40 min | Critical — **this is what I skipped last time** |
| 4. Verify | 20 min | High |
| 5. Plan | 20 min | Medium |

---

## Completed in this extended timebox (19:03–19:30)

### Merged into Chiana.md
- ✅ Post-series comics overview (BOOM! Studios 6 volumes, Volume 4 *Tangled Roots* with Chiana co-lead status)
- ✅ Alternate reality versions (Jessica, Chiana/Aeryn, Noranti/Chiana, Unrealized Heavy Chiana, Married Chiana from *Gone and Back*, John Quixote VR Chiana)
- ✅ "A Clockwork Nebari" analysis entry
- ✅ "Losing Time" precognition arc (3.09 → 3.19)

### New standalone files created
- ✅ `Comics/Farscape Comics — Chiana Appearances.md` (3.5KB) — volume-level overview
- ✅ `Episodes/A Clockwork Nebari — Chiana analysis.md` (2.2KB) — Nebari politics episode
- ✅ `Episodes/Losing Time — Chiana analysis.md` (1.9KB) — precognition arc start
- ✅ `Episodes/Alternate Reality Chiana versions.md` (3.3KB) — all alternate universe variants

### Remaining from previous plan
- [x] Episode-by-episode: 3 key episodes done (Clockwork, Losing Time, Alternate Reality)
- [x] Comics: First-pass volume overview complete
- [ ] Peacekeeper Wars scene-level evidence
- [ ] Image archival
- [ ] Propstore costume lots

---

## Lessons learned

1. **Always merge during the timebox, not after.** Cache ≠ vault.
2. **4 parallel batches, not 50 individual searches.**
3. **Read the full file before patching.**
4. **Archive spillover immediately.**
5. **The merge is the bottleneck.** Allocate more time to Phase 3 than Phase 2.
6. **Status tracking.** Every file should have a `status:` field (placeholder → draft → first-pass → verified → complete).
7. **Create standalone files for complex topics.** Comics, alternate realities, and precognition arcs are better as separate notes with links from the main dossier than as long sections that make the main file unwieldy.
