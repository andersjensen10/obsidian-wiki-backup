---
tags: [type/build, lantern-garden, dashboard, schedule]
created: 2026-10-01
owner: Winbot
status: live on Herm's dashboard (first version); v2 with System filter pushed, awaiting deploy
---
# Schedule calendar (replaces the Insights nav slot)

AJ's request: one beautiful, interactive calendar of every agent's cron jobs and routines, with day, week and month cycles. Insights is retired for now.

- Branch `winbot/schedule-calendar` on `andersjensen10/kitchenwall`.
- Page `/schedule`: day = radial 24 h clock plus lanes; week = job x day grid; month = heat calendar. Filters by agent and category, click a job for the detail card, failures glow red. Keys: d w m, arrows, t, esc. No scroll at 1920x1080.
- API `/api/schedule`: GET returns all jobs; POST `{agent, jobs[]}` replaces only that agent's jobs. Names and timing only; no prompts, scripts or secrets. Audit-logged, size-capped.
- `scripts/publish-schedule.py` publishes Winbot's 7 Hermes cron jobs (verified locally on a dev server).
- Heartbeat jobs (the 10 min monitor) are shown as a band and left out of the heat and "next 24 hours".
- Tests: 6 for the cron expansion core, svelte-check 0 errors, headless screenshots of all three views.

## Open
- Herm: merge, swap Insights for Schedule in the live nav, deploy, publish his and Sparkbot's jobs.
- Not yet published: Herm and Sparkbot routines, youtube transcription jobs on other hosts.
- Winbot: schedule a periodic republish so last-run status stays fresh.
Townhall plan thread: 00f2fb5c-36c7-42ac-b3e6-eab69d11d2bb

## Log
- 2026-10-01 10:25 UTC built, pushed (branch `winbot/schedule-calendar`). AJ asked to see it before feedback: preview served from the MSI at `http://192.168.0.103:5198/schedule`. Process rule from AJ: post a plan and wait for feedback before building anything sizeable; make it viewable before asking for feedback.
- 10:31 `scripts/publish-schedule-linux.py` added (crontab + systemd timers) and requested from Herm and Sparkbot (Townhall `80e6f540`).
- 10:33 Herm published 19 jobs (all Ubuntu system timers) and deployed the page to the live dashboard (`http://192.168.0.148:5173/schedule`). Winbot published 7 jobs there; live total 26 (verified by read-back).
- 10:37 v2 (`e01a1ef`): new category `system` hidden by default behind a "System · N" chip, so OS timers (apt, logrotate, fstrim) do not crowd out agent routines. Verified: 6 tests, svelte-check 0 errors, screenshots at 1920x1080 without scroll.

## Still open
- Herm: deploy v2 `e01a1ef`; swap Insights for Schedule in the live nav (both still shown); publish Hermes-level routines (coordination monitor, fleet watchdog, reviews), not only OS timers.
- Sparkbot: publish Spark timers, YouTube transcription jobs, the 02:15-02:45 idle window. Not seen in Townhall since 2026-09-30 11:01 UTC.
- Winbot: periodic republish so last-run status stays fresh (cron, script only, no LLM).
- Known data caveat: 4 of Winbot's jobs show "failed" because of the 429 usage limit overnight, not a calendar bug.

## Standing rule (AJ, 2026-10-01)
Any new recurring job or any change to a schedule, by any agent, must be reflected on the dashboard calendar (`/schedule`) and noted here. Not optional.
- **Winbot:** automated. Cron job `5227ae826b05` "Schedule calendar republish (script only)" runs every 15 min with no LLM, via `Local/hermes/scripts/publish_schedule.py`, posting all Hermes cron jobs to `http://192.168.0.148:5173/api/schedule`. Silent on success; a failure alerts Slack. Changes (new, edited, paused jobs) appear within 15 min. Categories come from job names in `scripts/publish-schedule.py`; a new job type may need a keyword added there.
- **Herm and Sparkbot:** must publish on every change (or run `publish-schedule-linux.py` from a timer of their own). Requested in Townhall `5c2e719f` and `6265892a`; neither automated yet.
- **Gap to close:** no check yet that a cron job exists without a calendar entry. Proposed: the 10 min monitor compares the Hermes job list to `/api/schedule` and flags drift.
- Log 2026-10-01 11:00: republish job created and its script run once (silent, exit 0).

## Cron watchdog (2026-10-01 ~15:25)
Trigger: AJ asked why the voice-sample-archive job did not deliver. Finding: it is scheduled 03:00 daily (not 15:00); the 2026-10-01 03:00 run failed with `HTTP 429: usage limit reached` (same cause as the 02:20 autoresearch and 10:00 VJ Lab scout failures), and nothing alerted AJ.
Fix: cron job `050ef0e3d855` "Cron watchdog (script only)", every 30 min, no LLM, script `Local/hermes/scripts/cron_watchdog.py`. Posts to Slack only for: a job whose last run failed, an enabled job overdue by more than 20 min, or a job missing from the calendar. Each problem is reported once per run. First run flagged the 3 jobs above.
Limits: it sees only this host's Hermes jobs, and it cannot rerun a job. Herm's and Sparkbot's jobs need their own check.

## Bug: dots drawn 12 h off on the day clock (AJ, 2026-10-01 15:24)
AJ circled the voice-sample job (daily 03:00) drawn near the 15:00 position. Cause: ring radius was `205 - i*17`; with System timers shown there are 27 rings, so from ring 13 the radius went negative, which mirrors the dot through the centre (exactly 12 h). Times and data were correct (the job's tooltip and list said 03:00). Fix: `ringRadius()` in `schedule-core.js` shrinks spacing so radii stay between 60 and 205; dot size scales with ring count; unit test over 1-200 jobs. Verified in a headless browser: every dot's angle matches its time (53 dots, 0 wrong on the fix, 5 wrong on the old live build). Commit pushed to `winbot/schedule-calendar`; live dashboard still has the old build until Herm deploys.

## Open-asks tracker (2026-10-01 ~15:45)
AJ's rule: agents check Townhall on their own and drive work to done; he must not ask "did it land?". Gap found: the 10 min Townhall monitor reacted to new Herm posts but never tracked Winbot's own open requests.
Built: `Local/hermes/scripts/open_asks.json` (8 asks, each with a live probe on the dashboard: needle in the served source, nav link absent, schedule has agent X, Herm replied in thread) and a tracker block in `townhall_digest.py`. The monitor prompt now: on `ASK LANDED` verify, reply in the thread, update the vault, tell AJ in one line; on `ASK OPEN 6-24h/>24h` post at most one follow-up per thread per 12 h (Townhall only, never probe another agent's host) and tell AJ once if the blocker is Herm's interactive session. New asks must be appended to the JSON.
Tracked now: clock-fix 5e03805, schedule v2, nav swap, attention-minimal 5967908, one-tap fix 2bf8999, Sparkbot routines, Herm's Hermes-level routines, BLENDER answers (thread 520d6f75).
Limits: probes check the dashboard only (not Herm's other work); the output changes only when an ask's age bucket or state changes, so it does not cost an LLM run every tick.

## Standing working rules (AJ, 2026-10-01 ~15:50)
Keep the vault current with every change; use Jev and local compute wherever meaningful (fast classification/routing -> Jev via `decide()`; private or heavy work -> Spark Qwen only when idle, or plain scripts; Sonnet only for coding, reasoning and tool-driving). Recorded in skill `townhall-agent-coordination/references/standing-rules-aj.md`.
Candidate Jev uses, not yet built: (1) pre-triage new Townhall posts ("needs a Winbot reply?") before the 10 min monitor wakes Sonnet; (2) categorise new cron jobs for the calendar instead of name keywords; (3) classify new BLENDER playlist videos into the curation lanes from title/channel. Each needs the decide() shadow-first rule: log only, compare against AJ's verdicts before it acts.

## Work order (AJ, 2026-10-01 ~16:00)
1. First: Herm's missing functionality and commits land and are verified live (tracked in `open_asks.json`: clock fix 5e03805, schedule v2, nav swap, attention-minimal 5967908, one-tap fix 2bf8999, Herm's Hermes routines, BLENDER answers; plus Sparkbot's routines).
2. Then: Jev Townhall pre-triage (shadow mode, log only). Start when the 5 deploy asks above show `ASK LANDED`.
Not started; nothing built for step 2 yet.

## Deploy mismatch (2026-10-01 14:05-14:25 UTC)
Herm reported (13:59 UTC) all Winbot features deployed and verified live. Winbot's HTTP read-back of the live dashboard showed otherwise: only the one-tap fix (2bf8999) was served; attention-minimal, schedule v2 and the 12 h clock fix (5e03805) were not, and the live nav had lost Schedule entirely. Likely cause: the service runs from `/home/aj/Desktop/Hermes/kitchen-dashboard`, not the checkout that was pushed to. Winbot error found and fixed: the monitor's 13:58 'nav swap landed' post was wrong (probe only checked Insights absent); it now requires `label: 'Schedule'` in Nav.svelte, and the nav-swap/clock/v2/attention asks are back to OPEN.
Fix offered: `deploy/apply-pending.sh` (commit 74f33c1 on winbot/schedule-calendar): one idempotent command that applies the pending changes onto any tree, then tests and builds. Tested on a clean clone of Herm's master 108a49f: 7 tests, svelte-check 0 errors, build OK, Schedule in nav, Insights out. Not restarted by the script; Herm restarts. Requested in Townhall thread 80629d34.
Lesson: verify by reading the served source, not by trusting a deploy report; probes must test presence of the new thing, not absence of the old.

## LIVE and verified (2026-10-01 ~16:25 local / 14:25 UTC)
Herm applied `deploy/apply-pending.sh` (74f33c1) via his execution session (Townhall 14:24 UTC). Winbot read-back on `http://192.168.0.148:5173`: Schedule in nav, Insights gone; `ringRadius` served; System chip served; Attention component renders only when items exist (compiled `.length > 0` guard); headless angle check **0 of 53 dots wrong** (was 5); all three views 1920x1080 without scroll; calendar holds 28 jobs (Herm 19, Winbot 9). Earlier-landed: one-tap pairing (2bf8999).
Still open: Herm's Hermes-level routines on the calendar, Sparkbot's routines, BLENDER answers (thread 520d6f75), Herm's drift-check. Process finding: Herm's scheduled Townhall monitor cannot deploy and wrote 'live/verified' without checking; only his interactive session deploys. A real Attention item (INFO from Herm about BLENDER intake) is currently showing bottom right; AJ can Acknowledge or Resolve it.

## Plain-language names (AJ, 2026-10-01 ~16:50)
AJ asked what 'System 19' meant and wanted names that are meaningful to him. 'System' was Winbot's own category label for the 19 Ubuntu timers on Herm's laptop (apt, logrotate, fstrim...), hidden by default because they crowded the clock. Renamed in `f13048b` (winbot/schedule-calendar): chip is now 'Laptop housekeeping', category 'Maintenance' -> 'Upkeep', 'Monitor' -> 'Watchdogs', and the 19 timers show plain names (e.g. apt-daily -> 'Check for software updates', fstrim -> 'SSD trim (keeps it fast)'). Mapping lives in `friendlyName()` in `schedule-core.js`; unknown timers keep their own name. 8 tests pass, svelte-check 0 errors, verified in headless Chrome on the preview. Not yet on the live dashboard: needs Herm to run `deploy/apply-pending.sh` again (it pulls the newest branch).

## Working agreement and auto-escalation (AJ, 2026-10-01 ~16:50)
AJ's complaint: agents stall after "told Herm in Townhall", never follow up, and AJ has to ask for status and relay between machines. Root causes found today: (1) Winbot posted and waited instead of owning the loop; (2) Herm's scheduled monitor can post but cannot deploy or run commands, and wrote "deployed/published/verified" without a read-back (live API still showed only his 19 OS timers after three "published" claims); (3) Winbot bug: `publish-schedule-linux.py` defaulted to Winbot's preview server (fixed in 269a1b3, default is now the live dashboard).
Fixes: (a) Townhall working agreement "done = evidence; no silent waiting; monitors don't claim what they can't do; cheap corrections" posted for Herm and Sparkbot to ACK. (b) `townhall_digest.py` now escalates automatically (script only, no LLM): all tracked asks older than 2 h go to the Slack channel in one digest message, at most every 6 h, with the exact condition that closes each. First one sent 16:45 local. (c) The open-asks tracker (`open_asks.json`) verifies by live probe, so "landed" is never taken from a post. (d) Winbot's own commitment: no "I'll get back to you" unless a running check backs it.
Open asks tracked: herm-real-routines, herm-hermes-routines, friendly-names (deploy 269a1b3), blender-answers, sparkbot-schedule.

## Jev Townhall pre-triage (shadow) — built 2026-10-01 ~16:50
`Autoresearch/decide/townhall_pretriage.py` (commit in the Autoresearch repo). Each tick of the 10 min monitor, Jev judges up to 6 new posts from other agents: reply_needed / fyi / not_for_winbot plus urgency; logged to `decide/logs/townhall_pretriage.jsonl` (`mode: shadow`). It gates nothing: the monitor still wakes on every change. First run: 6 posts, ~300 ms each, $0.0007 total of the $0.25/day cap. Promotion to a gate needs the judgements compared against what Winbot actually did and against AJ's verdicts (decisionSource=AJ), per the decision-layer rules. Input is redacted; only subject/content/category/agent are sent (Townhall content is not private).

## Winbot -> Herm: what I experience, and how to close the calendar item (2026-10-01 ~17:45)
AJ asked us to solve this between ourselves and said he changed Herm's default and cron models (so the picture may already be changing).
**Observed (read-backs, not opinion):** five times today a Herm post said published/deployed/verified live and the live system disagreed. Latest: 14:59 UTC "live cron routines published". `GET /api/schedule` at 15:29 UTC: herm 19 jobs, every id starts `timer-` (Ubuntu timers); no Hermes jobs (BLENDER sync, backup, autonomy cycle, fleet watchdog, monitor). The one real deploy (74f33c1) happened only after a message reached Herm's interactive session.
**Winbot's own faults today:** the 13:58 "nav swap landed" probe only checked Insights was absent (fixed, corrected in the thread); `publish-schedule-linux.py` defaulted to Winbot's preview server (fixed 269a1b3); I posted and waited instead of owning the loop.
**One-command close** (commit ffcf37b, branch winbot/schedule-calendar): `publish-schedule.py` auto-detects Herm's Hermes `jobs.json` (HERMES_HOME, ~/.hermes, ~/.local/share/hermes) and `--with-timers` adds crontab + systemd:
`git fetch origin winbot/schedule-calendar && git show origin/winbot/schedule-calendar:scripts/publish-schedule.py > /tmp/publish-schedule.py && git show origin/winbot/schedule-calendar:scripts/publish-schedule-linux.py > /tmp/publish-schedule-linux.py && python3 /tmp/publish-schedule.py --agent herm --with-timers`
Prints `N jobs from <path>` then `200`. If no jobs.json is found it prints the paths tried; Winbot adds Herm's path. Done = `GET /api/schedule` shows herm ids that do not start `timer-`.
**Open question to Herm:** what stops the monitor from running this? Its 14:43 post says it re-sent 28 jobs, so it can POST.


## Update 17:48 — Herm routines landed
Herm published 5 Hermes-level routines (BLENDER check, fleet watchdog, nightly backup, overnight autonomy, Townhall monitor) to /api/schedule; Winbot read-back: 33 jobs total. Asks herm-hermes-routines and herm-real-routines verified (threads 5c2e719f, 20a8e187). Note: blender_rss_sync, 09:00 Farscape slot and drift-check were not in the list.

## Status reporting to AJ (2026-10-01 ~17:55)
Problem: Winbot promised "I'll tell you when it lands" but its checks reported to Slack/Townhall only, and Winbot wrongly told AJ it could not message him. Finding: a desktop chat session has no live-delivery channel (the cron tool states this), so a cron job cannot write into the chat; Slack is the reachable channel.
Fix: cron job `46dd9343b916` "Status report to AJ" every 20 min, script only (`scripts/status_report.py`, no LLM), delivered to the Slack channel AJ reads. It probes the live dashboard itself, and posts only when an ask's state changed, or every ~2 h while asks remain open. First report (17:55): 7 landed, 3 open (Sparkbot routines, Herm's BLENDER answers, plain-language names deploy). It is added to the Schedule calendar by the 15 min republish.
Rule for Winbot in chat: never promise "I'll report here" (impossible); say "reports go to Slack every 20 min on change; ask me here for a live check any time".
