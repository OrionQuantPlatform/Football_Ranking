"""Read-only data inventory used by the DataScout comparison.

From the repository root:
python3 dashboard/outputs/datascout-benchmark/inspect_orion_data.py
"""
import collections
import gzip
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
DATA = ROOT / "data"


def read(relative):
    path = DATA / relative
    with (gzip.open(path, "rt") if path.suffix == ".gz" else path.open()) as f:
        return json.load(f)


index = read("raw/index.json")
season = next(s for s in index["seasons"] if s["id"] == "2026/2027")
counts = collections.Counter()
fields = set()
rows = played = 0
for chunk in season["chunks"]:
    for row in read(chunk["tables"]["performances"]["path"]):
        rows += 1
        fields.update(row)
        if isinstance(row.get("minutes"), (int, float)) and row["minutes"] > 0:
            played += 1
        counts.update(k for k, v in row.items() if v is not None)

profiles = read("raw/profile-index.json")
profile_report = {}
for kind in ["players", "teams"]:
    count = 0
    keys, present = collections.Counter(), collections.Counter()
    for relative in profiles["tables"]:
        if f"/profiles_{kind}/" not in relative:
            continue
        for row in read(relative):
            value = row.get("observation", {}).get("data")
            if not isinstance(value, dict):
                continue
            count += 1
            keys.update(value.keys())
            present.update(k for k, v in value.items() if v is not None)
    profile_report[kind] = {"observations": count, "fields": dict(keys), "nonNull": dict(present)}

report = {
    "scope": "2026/2027 canonical normalized performances across all 44 competition chunks; not deduplicated unique players",
    "rows": rows,
    "playedRows": played,
    "fields": sorted(fields),
    "nonNullCounts": dict(counts),
    "profileInventory": "profile-field-inventory.json",
    "missingPlayerProfileFields": ["date of birth/age", "preferred foot", "height", "contract expiry", "market value", "injury/transfer history"],
    "missingPhysicalData": ["tracked total running distance", "sprint count", "top speed"],
    "positionCaveat": "role is null throughout normalized performances; positionId and formation coordinates require football-role mapping before positional percentiles",
}
(OUT / "data-readiness.json").write_text(json.dumps(report, indent=2) + "\n")
(OUT / "profile-field-inventory.json").write_text(json.dumps(profile_report, indent=2) + "\n")
print(json.dumps({"performanceRows": rows, "playedRows": played, "knownRole": counts["role"], "playerProfileObservations": profile_report["players"]["observations"], "teamProfileObservations": profile_report["teams"]["observations"]}, indent=2))
