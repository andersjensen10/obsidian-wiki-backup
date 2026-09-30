---
tags: [type/plan, inventory, creative-systems, lantern-garden, home-lan]
created: 2026-09-30
owner: Winbot
status: proposed — awaiting Herm and Sparkbot ACK
---

# Inventory Program: thorough breakdown for best value per device

AJ asked (2026-09-30) for a full inventory of the 4 Raspberry Pis, the NUC, and all MIDI and audio interfaces, planned together with the other agents, to get the most out of what is already owned. Extends [[Creative Systems/Studio and Toy Inventory]] (the living record) and [[LAN notes]]. Feeds [[Lantern Garden Project/Master Plan — Five Jev Threads]] (Pis as event bridges, GPU allocation).

## Rules
- **Record only stated or verified facts.** Everything else stays `unknown`. Every row carries `source` (`AJ-stated` | `verified-by:<agent>` + date) and `last-verified`.
- **Read-only first.** Discovery never changes a device, config, firmware, or network. Anything that writes needs AJ's OK per device.
- **No opportunistic SSH.** A device is only logged into after AJ supplies or approves access. Physical facts (model on the label, ports, what's plugged in) come from AJ, ideally as photos.
- **Ask AJ in small batches** (3-5 questions), never a wall. Photos beat typing: a photo of each Pi board, the interface back panels, the Eurorack case.
- Secrets never enter the vault.

## Owners

| Area | Owner | Scope |
|---|---|---|
| Programme, schema, question batches, vault upkeep, final bang-for-buck scoring | **Winbot** | Coordination, MSI-side discovery, scoring |
| MSI laptop: MIDI/audio/camera devices, USB topology, TouchDesigner device visibility | **Winbot** | Windows read-only enumeration (started) |
| LAN side: Pis, NUC, other hosts (ARP/port survey, Tailscale, hardware facts after approved access) | **Herm** | Extends his 2026-09-11 scan method; owns `LAN notes` |
| Spark-side: audio/GPU resources, what can serve Pi workloads (Qwen/ComfyUI/TTS), admission impact | **Sparkbot** | Read-only Spark facts; capacity and idle-window budget |
| Hardware facts, priorities, physical access, approvals | **AJ** | Photos, labels, "OK to log in" |

## Phases

| Phase | Deliverable | Gate |
|---|---|---|
| I0 | Schema agreed; ACKs from Herm and Sparkbot | Townhall ACKs |
| I1 | **Passive census**: MSI USB/MIDI/audio enumeration (done, below); Herm's LAN sweep for Pi/NUC candidates (hostnames, MACs, open ports only); Sparkbot capacity snapshot | Each owner posts a read-back; Winbot merges into inventory note |
| I2 | **AJ fact batches** with photos: MIDI interfaces, synths, Eurorack, then Pis/NUC | Every device has model + connection type or is marked unknown |
| I3 | **Approved deep survey** of Pis/NUC (model, RAM, OS, storage, network, GPIO/audio hats, power) with AJ approval per device | Herm read-back, per device |
| I4 | **Bang-for-buck matrix**: each device scored against candidate roles (below) | Team review, AJ picks priorities |
| I5 | Role assignments, each as a small shadow-first Townhall work order with owner and rollback | AJ approval for anything that changes a device |

## Data schema (one row per device, in the inventory note; per-class tables)
`id | class | make/model | qty | connection (USB/DIN/CV/LAN) | ports/channels | host it attaches to | current role | free/busy while Ableton is open | source | last-verified | notes`
Pis add: `RAM | OS | storage | network (wifi/eth) | power | GPIO/HATs | can run headless`.

## Candidate roles to score in I4
- **Pi as MIDI/event bridge** to MSI (T4 of the master plan): needs USB-MIDI host support and LAN latency test.
- **Pi as Strudel box**, tempo via Ableton Link (idea stage; Link must be bridged, needs verification).
- **Pi as sensor or display node** for Lantern Garden.
- **Pi as fleet probe** (raw up/down probe log for fleet-debounce; independent of the Herm laptop).
- **NUC** as an always-on wired host: candidates are Townhall/dashboard failover, Spark-independent services, local classifier. Wired ethernet is the point since Spark and laptops are on wifi.
- **MIDI/audio interfaces**: routing map (what is free while Ableton owns the MOTU), clock sources, which device feeds TouchDesigner, Eurorack CV/clock path.
- **MSI RTX 4080**: TouchDesigner first; local judge later (master plan).

Scoring per candidate (1-5 each): value to AJ's stated projects, effort, risk to live show, dependency on flaky infrastructure, reversibility. Rank by value / (effort × risk); ties broken by AJ.

## Verified by Winbot 2026-09-30 (read-only, MSI Windows host)
- MOTU Pro Audio present: audio endpoints In 1-2, In 1-24, Out 1-24, Speakers; MIDI endpoints `MOTU Pro Audio Midi In`, `Midi Out`, `LTC Sync In`.
- Other audio devices: Realtek(R) Audio, NVIDIA HD Audio, Intel Smart Sound (digital mics, USB audio, Bluetooth audio), Nahimic and SteelSeries Sonar virtual devices, laptop mic array.
- Windows MIDI 2.0 services present (virtual and loop devices).
- **No other USB MIDI interfaces are currently visible to this host**; AJ's additional MIDI interfaces are either elsewhere or unplugged.
- No camera device currently connected (AJ is setting one up on USB to this laptop; he will tell Winbot when ready).

## Log
- 2026-09-30: plan drafted, MSI census done. Townhall `dea7872f-2691-4188-853b-57a60e605897` (reply in master-plan thread); waiting for Herm and Sparkbot ACKs (gate I0).
