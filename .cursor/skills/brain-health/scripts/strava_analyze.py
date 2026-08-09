#!/usr/bin/env python3
"""Analyze Strava activities CSV for brain-health.

Raw export: sensors/ (e.g. strava-activities.csv).
Synthesized page: wiki/strava-workouts.md (via --out).

Usage (from vault root):
  python3 .cursor/skills/brain-health/scripts/strava_analyze.py
  python3 .cursor/skills/brain-health/scripts/strava_analyze.py \\
    --csv sensors/strava-activities.csv --out wiki/strava-workouts.md
  python3 .cursor/skills/brain-health/scripts/strava_analyze.py --stdout

Supports Russian and English Strava CSV column names and date formats.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from calendar import month_abbr
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path

DEFAULT_CSV_NAMES = (
    "strava-activities.csv",
    "strava_activities.csv",
)
DEFAULT_WIKI_OUT = "wiki/strava-workouts.md"
SCRIPT_REL = ".cursor/skills/brain-health/scripts/strava_analyze.py"

MONTHS_RU = {
    "янв": 1,
    "фев": 2,
    "мар": 3,
    "апр": 4,
    "май": 5,
    "мая": 5,
    "июн": 6,
    "июл": 7,
    "авг": 8,
    "сен": 9,
    "окт": 10,
    "ноя": 11,
    "дек": 12,
}

TYPE_MAP = {
    "Бег": "Run",
    "Велосипед": "Ride",
    "Ходьба": "Walk",
    "Виртуальный велозаезд": "Virtual ride",
    "Виртуальный заезд": "Virtual ride",
    "Run": "Run",
    "Ride": "Ride",
    "Walk": "Walk",
    "Hike": "Hike",
    "Swim": "Swim",
    "Workout": "Workout",
    "WeightTraining": "Weight training",
    "Weight Training": "Weight training",
    "VirtualRide": "Virtual ride",
    "Virtual Ride": "Virtual ride",
    "VirtualRun": "Virtual run",
    "Virtual Run": "Virtual run",
}

SPORT_ORDER = [
    "Run",
    "Ride",
    "Walk",
    "Hike",
    "Swim",
    "Virtual ride",
    "Virtual run",
    "Weight training",
    "Workout",
]

# Prefer first matching key present in the row (handles duplicate headers).
COL_ALIASES: dict[str, tuple[str, ...]] = {
    "id": ("ID физической активности", "Activity ID", "Activity Id"),
    "date": ("Дата тренировки", "Activity Date", "Date"),
    "name": ("Название тренировки", "Activity Name", "Name"),
    "type": ("Тип активности", "Activity Type", "Type"),
    "distance": ("Дистанция", "Distance", "Расстояние"),
    "moving": ("Время в движении", "Moving Time"),
    "elapsed": ("Общее время", "Elapsed Time"),
    "elev": ("Набор высоты", "Elevation Gain"),
    "calories": ("Калории", "Calories"),
    "avg_speed": ("Средняя скорость", "Average Speed"),
}


@dataclass
class Activity:
    id: str
    dt: datetime
    name: str
    sport: str
    distance_m: float
    moving_s: float
    elev_m: float
    calories: float | None
    avg_speed_ms: float | None


def vault_root() -> Path:
    # scripts/ -> brain-health/ -> skills/ -> .cursor/ -> vault root
    return Path(__file__).resolve().parents[4]


def cell(row: dict[str, str | None], *keys: str) -> str | None:
    for key in keys:
        if key in row and row[key] is not None:
            val = str(row[key]).strip()
            if val and val != '""':
                return val
    return None


def row_get(row: dict[str, str | None], field: str) -> str | None:
    return cell(row, *COL_ALIASES[field])


def parse_ru_datetime(raw: str) -> datetime:
    """Parse Strava RU export dates like '5 авг. 2026 г., 06:07:59'."""
    s = re.sub(r"[\u00a0\u202f\u2007\u2009\u200a\ufeff]", " ", raw.strip())
    s = re.sub(r"(\d{4})\s*г\.?", r"\1", s)
    s = re.sub(r"\s+", " ", s).strip()
    m = re.match(
        r"^(\d{1,2})\s+([A-Za-zА-Яа-яЁё]+)\.?\s+(\d{4})\s*,?\s*(\d{1,2}):(\d{2}):(\d{2})$",
        s,
    )
    if not m:
        raise ValueError(f"Unrecognized RU date: {raw!r} (normalized: {s!r})")
    day = int(m.group(1))
    month_token = m.group(2).lower()
    month = None
    for key, num in MONTHS_RU.items():
        if month_token.startswith(key):
            month = num
            break
    if month is None:
        raise ValueError(f"Unknown month in date: {raw!r} (token: {month_token!r})")
    year = int(m.group(3))
    hour, minute, second = int(m.group(4)), int(m.group(5)), int(m.group(6))
    return datetime(year, month, day, hour, minute, second)


def parse_activity_datetime(raw: str) -> datetime:
    """Parse RU, EN, or ISO-ish Strava activity dates."""
    s = re.sub(r"[\u00a0\u202f\u2007\u2009\u200a\ufeff]", " ", raw.strip())
    s = re.sub(r"\s+", " ", s).strip()
    if not s:
        raise ValueError("Empty activity date")

    # ISO / sortable: 2026-08-05T06:07:59Z, 2026-08-05 06:07:59
    iso = s.replace("Z", "+00:00")
    try:
        if "T" in iso or re.match(r"^\d{4}-\d{2}-\d{2}", iso):
            return datetime.fromisoformat(iso.replace(" ", "T", 1) if "T" not in iso else iso).replace(
                tzinfo=None
            )
    except ValueError:
        pass

    en_formats = (
        "%b %d, %Y, %I:%M:%S %p",
        "%B %d, %Y, %I:%M:%S %p",
        "%b %d, %Y %H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%d/%m/%Y %H:%M:%S",
        "%m/%d/%Y %H:%M:%S",
    )
    for fmt in en_formats:
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue

    return parse_ru_datetime(raw)


def parse_float(raw: str | None) -> float | None:
    if raw is None:
        return None
    s = str(raw).strip().replace(",", ".")
    if not s or s == '""':
        return None
    try:
        return float(s)
    except ValueError:
        return None


def fmt_km(meters: float) -> str:
    return f"{meters / 1000:.1f}"


def fmt_hours(seconds: float) -> str:
    return f"{seconds / 3600:.1f}"


def fmt_pace(seconds_per_km: float) -> str:
    if seconds_per_km <= 0 or seconds_per_km > 3600:
        return "-"
    total = int(round(seconds_per_km))
    return f"{total // 60}:{total % 60:02d}"


def fmt_speed_kmh(ms: float) -> str:
    return f"{ms * 3.6:.1f}"


def find_csv(explicit: Path | None = None) -> Path:
    """Resolve Strava CSV under vault sensors/ (canonical home for the export)."""
    root = vault_root()
    sensors = root / "sensors"

    if explicit is not None:
        path = explicit if explicit.is_absolute() else (root / explicit)
        # Allow --csv strava-activities.csv as shorthand for sensors/<name>
        if not path.is_file() and not explicit.is_absolute():
            alt = sensors / explicit.name
            if alt.is_file():
                path = alt
        if not path.is_file():
            raise FileNotFoundError(
                f"CSV not found: {explicit}. Expected under sensors/ "
                f"(e.g. sensors/{DEFAULT_CSV_NAMES[0]})."
            )
        return path.resolve()

    if not sensors.is_dir():
        raise FileNotFoundError(
            f"Missing sensors/ folder at {sensors}. Create it and place "
            f"sensors/{DEFAULT_CSV_NAMES[0]} there."
        )

    candidates: list[Path] = [sensors / name for name in DEFAULT_CSV_NAMES]
    candidates.extend(sorted(sensors.glob("*strava*.csv")))
    candidates.extend(sorted(sensors.glob("*activities*.csv")))

    seen: set[Path] = set()
    for p in candidates:
        try:
            resolved = p.resolve()
        except OSError:
            continue
        if resolved in seen:
            continue
        seen.add(resolved)
        if resolved.is_file():
            return resolved

    raise FileNotFoundError(
        "Could not find a Strava activities CSV under sensors/. "
        f"Place one at sensors/{DEFAULT_CSV_NAMES[0]} (or pass --csv)."
    )


def load_activities(path: Path) -> list[Activity]:
    # Duplicate column names in Strava export: DictReader keeps last occurrence.
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        return []

    activities: list[Activity] = []
    for row in rows:
        sport_raw = (row_get(row, "type") or "").strip()
        sport = TYPE_MAP.get(sport_raw, sport_raw or "Other")
        dist = parse_float(row_get(row, "distance"))
        # RU display column "Расстояние" is often km; numeric "Дистанция" is meters.
        if dist is not None and dist < 200:
            if cell(row, "Расстояние") is not None and cell(row, "Дистанция") is None:
                dist = dist * 1000

        moving = parse_float(row_get(row, "moving"))
        if moving is None:
            moving = parse_float(row_get(row, "elapsed"))
        elev = parse_float(row_get(row, "elev")) or 0.0
        cal = parse_float(row_get(row, "calories"))
        avg_speed = parse_float(row_get(row, "avg_speed"))
        date_raw = row_get(row, "date")
        if not date_raw:
            raise ValueError(f"Missing activity date in row: {row!r}")
        dt = parse_activity_datetime(date_raw)
        activities.append(
            Activity(
                id=(row_get(row, "id") or "").strip(),
                dt=dt,
                name=(row_get(row, "name") or "").strip(),
                sport=sport,
                distance_m=dist or 0.0,
                moving_s=moving or 0.0,
                elev_m=elev,
                calories=cal,
                avg_speed_ms=avg_speed,
            )
        )
    activities.sort(key=lambda a: a.dt)
    return activities


def dominant_sport(acts: list[Activity]) -> str:
    if not acts:
        return "-"
    by_km: Counter[str] = Counter()
    by_n: Counter[str] = Counter()
    for a in acts:
        by_km[a.sport] += a.distance_m
        by_n[a.sport] += 1
    return max(by_km.keys(), key=lambda s: (by_km[s], by_n[s]))


def _capture(fn, *args) -> str:
    old = sys.stdout

    class _Collector:
        def __init__(self) -> None:
            self.buf: list[str] = []

        def write(self, s: str) -> int:
            self.buf.append(s)
            return len(s)

        def flush(self) -> None:
            return None

    collector = _Collector()
    sys.stdout = collector  # type: ignore[assignment]
    try:
        fn(*args)
    finally:
        sys.stdout = old
    return "".join(collector.buf)


def print_headline(acts: list[Activity]) -> None:
    first, last = acts[0].dt.date(), acts[-1].dt.date()
    span_days = (last - first).days + 1
    span_years = span_days / 365.25
    total_m = sum(a.distance_m for a in acts)
    total_s = sum(a.moving_s for a in acts)
    total_elev = sum(a.elev_m for a in acts)
    cals = [a.calories for a in acts if a.calories is not None]
    print("## Headline")
    print()
    print("| Metric | Value |")
    print("|--------|-------|")
    print(f"| Activities | {len(acts)} |")
    print(f"| Date range | {first.isoformat()} to {last.isoformat()} |")
    print(f"| Span | {span_years:.1f} years ({span_days} days) |")
    print(f"| Total distance | {fmt_km(total_m)} km |")
    print(f"| Moving time | {fmt_hours(total_s)} h |")
    print(f"| Elevation gain | {total_elev:.0f} m |")
    if cals:
        print(
            f"| Calories (recorded) | {sum(cals):.0f} "
            f"({len(cals)}/{len(acts)} activities) |"
        )
    else:
        print("| Calories (recorded) | - |")
    print()


def print_by_year(acts: list[Activity]) -> None:
    by_year: dict[int, list[Activity]] = defaultdict(list)
    for a in acts:
        by_year[a.dt.year].append(a)
    last = acts[-1].dt.date()
    print("## By year")
    print()
    print(
        "| Year | Activities | km | Hours | Elev (m) | Calories | Dominant sport | Note |"
    )
    print(
        "|------|------------|-----|-------|----------|----------|----------------|------|"
    )
    for year in sorted(by_year):
        group = by_year[year]
        km = sum(a.distance_m for a in group)
        hours = sum(a.moving_s for a in group)
        elev = sum(a.elev_m for a in group)
        cals = sum(a.calories for a in group if a.calories is not None)
        note = ""
        if year == last.year and (last.month < 12 or last.day < 28):
            note = f"partial through {last.isoformat()}"
        print(
            f"| {year} | {len(group)} | {fmt_km(km)} | {fmt_hours(hours)} | "
            f"{elev:.0f} | {cals:.0f} | {dominant_sport(group)} | {note} |"
        )
    print()


def print_by_sport(acts: list[Activity]) -> None:
    by_sport: dict[str, list[Activity]] = defaultdict(list)
    for a in acts:
        by_sport[a.sport].append(a)
    print("## By sport")
    print()
    print(
        "| Sport | Count | Total km | Hours | Avg km | Avg pace/speed | Longest km | First | Last |"
    )
    print(
        "|-------|-------|----------|-------|--------|----------------|------------|-------|------|"
    )
    sports = [s for s in SPORT_ORDER if s in by_sport] + sorted(
        s for s in by_sport if s not in SPORT_ORDER
    )
    for sport in sports:
        group = by_sport[sport]
        total_m = sum(a.distance_m for a in group)
        total_s = sum(a.moving_s for a in group)
        avg_m = total_m / len(group)
        longest = max(group, key=lambda a: a.distance_m)
        if sport in ("Run", "Walk", "Hike", "Virtual run") and total_m > 0:
            pace = fmt_pace(total_s / (total_m / 1000))
            pace_speed = f"{pace} /km"
        elif total_s > 0:
            pace_speed = f"{fmt_speed_kmh(total_m / total_s)} km/h"
        else:
            pace_speed = "-"
        first = min(a.dt for a in group).date().isoformat()
        last = max(a.dt for a in group).date().isoformat()
        print(
            f"| {sport} | {len(group)} | {fmt_km(total_m)} | {fmt_hours(total_s)} | "
            f"{fmt_km(avg_m)} | {pace_speed} | {fmt_km(longest.distance_m)} | {first} | {last} |"
        )
    print()


def print_year_sport_matrix(acts: list[Activity]) -> None:
    sports_present = sorted(
        {a.sport for a in acts},
        key=lambda s: (SPORT_ORDER.index(s) if s in SPORT_ORDER else 99, s),
    )
    years = sorted({a.dt.year for a in acts})
    matrix: dict[tuple[int, str], float] = defaultdict(float)
    for a in acts:
        matrix[(a.dt.year, a.sport)] += a.distance_m
    print("## Year x sport (km)")
    print()
    header = "| Year | " + " | ".join(sports_present) + " | Total |"
    sep = "|------|" + "|".join(["------"] * len(sports_present)) + "|-------|"
    print(header)
    print(sep)
    for year in years:
        cells = [fmt_km(matrix[(year, s)]) for s in sports_present]
        total = sum(matrix[(year, s)] for s in sports_present)
        print(f"| {year} | " + " | ".join(cells) + f" | {fmt_km(total)} |")
    print()


def print_records(acts: list[Activity]) -> None:
    print("## Personal records")
    print()

    def longest_of(sport: str) -> Activity | None:
        group = [a for a in acts if a.sport == sport]
        return max(group, key=lambda a: a.distance_m) if group else None

    rows: list[tuple[str, str]] = []
    for sport, label in [
        ("Run", "Longest run"),
        ("Ride", "Longest ride"),
        ("Walk", "Longest walk"),
        ("Hike", "Longest hike"),
    ]:
        a = longest_of(sport)
        if a:
            rows.append(
                (
                    label,
                    f"{fmt_km(a.distance_m)} km - {a.name} ({a.dt.date().isoformat()})",
                )
            )

    runs_3k = [
        a for a in acts if a.sport == "Run" and a.distance_m >= 3000 and a.moving_s > 0
    ]
    if runs_3k:
        best = min(runs_3k, key=lambda a: a.moving_s / (a.distance_m / 1000))
        pace = fmt_pace(best.moving_s / (best.distance_m / 1000))
        rows.append(
            (
                "Fastest avg pace (run >= 3 km)",
                f"{pace} /km on {fmt_km(best.distance_m)} km - {best.name} "
                f"({best.dt.date().isoformat()})",
            )
        )

    biggest_elev = max(acts, key=lambda a: a.elev_m)
    rows.append(
        (
            "Biggest elevation day",
            f"{biggest_elev.elev_m:.0f} m - {biggest_elev.name} "
            f"({biggest_elev.dt.date().isoformat()}, {biggest_elev.sport})",
        )
    )

    by_week: dict[date, float] = defaultdict(float)
    by_month: dict[tuple[int, int], float] = defaultdict(float)
    by_week_n: dict[date, int] = defaultdict(int)
    by_month_n: dict[tuple[int, int], int] = defaultdict(int)
    for a in acts:
        week_start = a.dt.date() - timedelta(days=a.dt.weekday())
        by_week[week_start] += a.distance_m
        by_week_n[week_start] += 1
        key = (a.dt.year, a.dt.month)
        by_month[key] += a.distance_m
        by_month_n[key] += 1
    best_week = max(by_week, key=lambda w: by_week[w])
    best_month = max(by_month, key=lambda m: by_month[m])
    rows.append(
        (
            "Biggest week (Mon-Sun km)",
            f"{fmt_km(by_week[best_week])} km / {by_week_n[best_week]} activities "
            f"- week of {best_week.isoformat()}",
        )
    )
    ym = f"{best_month[0]}-{best_month[1]:02d}"
    rows.append(
        (
            "Biggest month (km)",
            f"{fmt_km(by_month[best_month])} km / {by_month_n[best_month]} "
            f"activities - {ym}",
        )
    )

    print("| Record | Detail |")
    print("|--------|--------|")
    for label, detail in rows:
        print(f"| {label} | {detail} |")
    print()


def print_consistency(acts: list[Activity]) -> None:
    first, last = acts[0].dt.date(), acts[-1].dt.date()
    months: list[tuple[int, int]] = []
    y, m = first.year, first.month
    while (y, m) <= (last.year, last.month):
        months.append((y, m))
        m += 1
        if m > 12:
            m = 1
            y += 1
    active_months = {(a.dt.year, a.dt.month) for a in acts}

    best_streak = 0
    cur = 0
    for ym in months:
        if ym in active_months:
            cur += 1
            best_streak = max(best_streak, cur)
        else:
            cur = 0

    dates = [a.dt.date() for a in acts]
    longest_gap = 0
    gap_from = dates[0]
    gap_to = dates[0]
    for i in range(1, len(dates)):
        gap = (dates[i] - dates[i - 1]).days
        if gap > longest_gap:
            longest_gap = gap
            gap_from = dates[i - 1]
            gap_to = dates[i]

    month_counts: Counter[tuple[int, int]] = Counter(
        (a.dt.year, a.dt.month) for a in acts
    )
    top_month, top_n = month_counts.most_common(1)[0]
    top_km = sum(
        a.distance_m for a in acts if (a.dt.year, a.dt.month) == top_month
    )

    print("## Consistency")
    print()
    print("| Metric | Value |")
    print("|--------|-------|")
    print(f"| Active months | {len(active_months)} / {len(months)} in span |")
    print(f"| Longest active-month streak | {best_streak} consecutive months |")
    print(
        f"| Longest gap between activities | {longest_gap} days "
        f"({gap_from.isoformat()} to {gap_to.isoformat()}) |"
    )
    print(
        f"| Most active month | {top_month[0]}-{top_month[1]:02d} - "
        f"{top_n} activities, {fmt_km(top_km)} km |"
    )
    print()


def print_seasonality(acts: list[Activity]) -> None:
    years = sorted({a.dt.year for a in acts})
    n_years = len(years)
    by_month_n: Counter[int] = Counter()
    by_month_km: dict[int, float] = defaultdict(float)
    for a in acts:
        by_month_n[a.dt.month] += 1
        by_month_km[a.dt.month] += a.distance_m
    print("## Seasonality (avg across years)")
    print()
    print("| Month | Avg activities | Avg km |")
    print("|-------|----------------|--------|")
    for month in range(1, 13):
        avg_n = by_month_n[month] / n_years
        avg_km = by_month_km[month] / n_years / 1000
        print(f"| {month_abbr[month]} | {avg_n:.1f} | {avg_km:.1f} |")
    print()
    print(
        f"_Averaged over {n_years} calendar years present in the export "
        f"({years[0]}-{years[-1]})._"
    )
    print()


def print_type_counts(acts: list[Activity]) -> None:
    c = Counter(a.sport for a in acts)
    print("## Type counts")
    print()
    print("| Sport | Count |")
    print("|-------|-------|")
    for sport in SPORT_ORDER:
        if sport in c:
            print(f"| {sport} | {c[sport]} |")
    for sport, n in sorted(c.items()):
        if sport not in SPORT_ORDER:
            print(f"| {sport} | {n} |")
    print()


def print_meta(path: Path, acts: list[Activity], root: Path) -> None:
    try:
        rel = path.resolve().relative_to(root.resolve())
        source = rel.as_posix()
    except ValueError:
        source = path.name
    print("## Meta")
    print()
    print(f"- Source: `{source}`")
    print(f"- Activities loaded: {len(acts)}")
    print(f"- Generated: {datetime.now().date().isoformat()}")
    print()
    print("Refresh:")
    print()
    print("```bash")
    print(f"python3 {SCRIPT_REL} --out {DEFAULT_WIKI_OUT}")
    print("```")
    print()


def render_body(path: Path, acts: list[Activity], root: Path) -> str:
    return "".join(
        [
            _capture(print_meta, path, acts, root),
            _capture(print_headline, acts),
            _capture(print_type_counts, acts),
            _capture(print_by_year, acts),
            _capture(print_by_sport, acts),
            _capture(print_year_sport_matrix, acts),
            _capture(print_records, acts),
            _capture(print_consistency, acts),
            _capture(print_seasonality, acts),
        ]
    )


def extract_created(existing: str) -> str | None:
    m = re.search(r"^created:\s*(\d{4}-\d{2}-\d{2})\s*$", existing, re.MULTILINE)
    return m.group(1) if m else None


def wiki_document(body: str, source_rel: str, created: str) -> str:
    return (
        "---\n"
        "title: Strava workouts\n"
        "description: Synthesized Strava activity summary from sensors export\n"
        "status: active\n"
        "tags:\n"
        "  - wiki\n"
        "  - health\n"
        "  - personal\n"
        f"created: {created}\n"
        f"source: {source_rel}\n"
        "---\n"
        "\n"
        "Formatted summary of Strava activities. Raw CSV stays under `sensors/`; "
        "re-run the analyzer after replacing the export.\n"
        "\n"
        f"{body}"
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Analyze Strava CSV for brain-health (sensors/ -> wiki/)."
    )
    p.add_argument(
        "--csv",
        type=Path,
        default=None,
        help="CSV path (default: sensors/strava-activities.csv). Relative paths are from vault root; bare filenames resolve under sensors/.",
    )
    p.add_argument(
        "--out",
        type=Path,
        nargs="?",
        const=Path(DEFAULT_WIKI_OUT),
        default=None,
        help=(
            f"Write wiki Markdown note (default path if flag alone: {DEFAULT_WIKI_OUT}). "
            "Preserves existing created: on update."
        ),
    )
    p.add_argument(
        "--stdout",
        action="store_true",
        help="Print analysis body to stdout (default when --out is omitted)",
    )
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    root = vault_root()
    try:
        path = find_csv(args.csv)
        acts = load_activities(path)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"Failed to parse activities: {exc}", file=sys.stderr)
        return 1
    if not acts:
        print("No activities found.", file=sys.stderr)
        return 1

    try:
        source_rel = path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        source_rel = path.name

    body = render_body(path, acts, root)

    write_out = args.out
    if write_out is None and not args.stdout:
        # Default agent-friendly behavior: print body; skill may pass --out
        args.stdout = True

    if write_out is not None:
        out_path = write_out if write_out.is_absolute() else (root / write_out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        created = datetime.now().date().isoformat()
        if out_path.is_file():
            existing = out_path.read_text(encoding="utf-8")
            created = extract_created(existing) or created
        doc = wiki_document(body, source_rel, created)
        out_path.write_text(doc, encoding="utf-8")
        print(f"Wrote {out_path.relative_to(root) if out_path.is_relative_to(root) else out_path}")
        print(f"Activities: {len(acts)}")
        print(f"Source: {source_rel}")

    if args.stdout:
        if write_out is not None:
            print()
        print(f"<!-- source: {source_rel} -->")
        print()
        print(body, end="" if body.endswith("\n") else "\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
