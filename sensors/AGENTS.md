# sensors/

## Purpose

Raw and exported data from wearable devices and personal sensors - the landing
zone for device reports over time.

## Put here

- Wearable exports: sleep, heart rate, HRV, SpO2, steps, workouts, recovery
- Device dumps from watches, rings, bands, scales, CGMs, and similar sensors
- Strava / Garmin / Apple Health / Oura / Whoop (and similar) CSV, JSON, ZIP
- Per-device or per-sync snapshots when a wearable reports into the vault

## Do not put here

- Clinical labs, imaging, medical PDFs → [`../health/`](../health/)
- Meal / nutrition notes → [`../health/`](../health/) (skill `brain-health`)
- Public health or world datasets → [`../statistics/`](../statistics/)
- Money / bank exports → [`../finance/`](../finance/)
- Orphan photos with no sensor meaning → [`../media/`](../media/)
- File inventories or index lists (this guide is not an index)

## Naming

- Prefer device + date: `YYYY-MM-DD-device-slug.ext` or `device-export-YYYY-MM.csv`
- Examples: `strava-activities.csv`, `2026-08-oura-sleep-export.csv`
- One export per source/device when practical; no spaces in filenames

## Skills

- Find sensor notes via skill `brain-search` (hub `sensors` + frontmatter)
- Health interpretation of sensor trends may use `brain-health` (data stays here)

## Shared rules

- Filenames: no spaces (skill `brain-fix` Step 2); prefer `YYYY-MM-DD-slug.ext`
- One canonical file per fact; other folders get a link or short pointer, not a duplicate
- This file is a hub **guide** (structure and purpose only) - not a file index
- Find notes via skill `brain-search` (hub + frontmatter); do not add `## Index` or file lists here
- Parent vault docs: [`../AGENTS.md`](../AGENTS.md), [`../ABOUT.md`](../ABOUT.md)
