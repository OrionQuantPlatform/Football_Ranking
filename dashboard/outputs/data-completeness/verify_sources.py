"""Reconcile real HTTP responses and saved browser JSON with canonical files.

Run from the repository root:
python3 dashboard/outputs/data-completeness/verify_sources.py
"""
import gzip
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
DATA = ROOT / "data"
API = "http://127.0.0.1:8765/api/archive/"


def read(path):
    path = Path(path)
    with (gzip.open(path, "rt") if path.suffix == ".gz" else path.open()) as f:
        return json.load(f)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


lookup = read(DATA / "raw/match-observations.json")
shards = read(DATA / "raw/observation-shards.json")
families = sorted({name for shard in shards.values() for name in shard["tables"]})


def match_source(mid):
    location = lookup[mid][0]
    shard = shards[location["shard"]]
    doc = read(DATA / shard["document"]["path"])[location["ordinal"]]
    endpoints = {}
    for name in doc["endpoints"]:
        rows = read(DATA / shard["tables"][name]["path"])
        endpoints[name] = next(row["response"] for row in rows if row["documentId"] == doc["id"])
    return {**doc["metadata"], "endpoints": endpoints}


references = {mid: match_source(mid) for mid in ["m_49qvGz", "m_4XOc3a", "m_0k4IES"]}
old_id = next(mid for mid, locations in lookup.items() if "2024-2025" in shards[locations[0]["shard"]]["document"]["path"])
references[old_id] = match_source(old_id)
report = {"canonicalShards": len(shards), "families": families, "matches": [], "browser": []}
for mid, expected in references.items():
    actual = json.load(urlopen(API + "matches/" + mid))
    assert actual == expected, mid
    report["matches"].append({"id": mid, "season": expected["season"], "status": expected["fixture"]["status"], "sha256": digest(expected), "families": {k: v.get("status") for k, v in expected["endpoints"].items()}, "apiEqualsCanonical": True})

for name, mid in [("upcoming", "m_0k4IES"), ("historical", old_id)]:
    path = OUT / f"browser-{name}-archive.json"
    if path.exists():
        assert read(path) == references[mid], name
        report["browser"].append({"section": name, "browserEqualsCanonical": True})

primary = references["m_49qvGz"]
player_id = "p_4QqLFm"
players = primary["endpoints"]["players"]["data"]
player = next(p for p in players if p["player"]["id"] == player_id)
halves = next(p for p in primary["endpoints"]["player_halves"]["data"]["players"] if p["player"]["id"] == player_id)
report["teamPeriods"] = [{"period": p["period"], "groups": len(p["groups"]), "metrics": sum(len(g["items"]) for g in p["groups"])} for p in primary["endpoints"]["stats"]["data"]["periods"]]
report["playerPeriods"] = [{"period": p.get("period", "All"), "groups": len(p["stats"]), "metrics": sum(len(g["stats"]) for g in p["stats"])} for p in [player, *halves["periods"]]]

keys = {"players/halves": "player_halves", "advanced": "advanced_teams", "advanced/players": "advanced_players", "advanced/network": "pass_networks"}
browser_path = OUT / "browser-match-json.json"
if browser_path.exists():
    payloads = read(browser_path)
    assert len(payloads) == 14
    for section, actual in payloads.items():
        expected = primary if section == "archive" else primary["endpoints"][keys.get(section, section)]["data"]
        assert actual == expected, section
        report["browser"].append({"section": section, "browserEqualsCanonical": True, "sha256": digest(expected)})

player_path = OUT / "browser-player-json.json"
if player_path.exists():
    values = read(player_path)
    for source in ["players", "player_halves", "advanced_players", "heatmaps"]:
        original = primary["endpoints"][source]["data"]
        expected = next(p for p in (original if isinstance(original, list) else original["players"]) if p["player"]["id"] == player_id)
        actual = values[source]["data"]
        rows = actual if isinstance(actual, list) else actual["players"]
        assert rows == [expected], source
    original = primary["endpoints"]["shots"]["data"]
    for before, after in zip(original["periods"], values["shots"]["data"]["periods"], strict=True):
        assert after["shots"] == [s for s in before["shots"] if s["player"]["id"] == player_id]
    # Events retain complete multi-player entries; participation is checked on original IDs.
    events = primary["endpoints"]["events"]["data"]["events"]
    assert values["events"]["data"]["events"] == [e for e in events if player_id in json.dumps(e)]
    assert values["pass_networks"]["data"]["networks"] == [n for n in primary["endpoints"]["pass_networks"]["data"]["networks"] if n["team"]["id"] == player["team_id"]]
    for side in ["home", "away"]:
        for group in ["starters", "subs"]:
            assert values["lineups"]["data"][side][group] == [p for p in primary["endpoints"]["lineups"]["data"][side][group] if p["player_id"] == player_id]
    profile_index = read(DATA / "raw/profile-index.json")
    ref = profile_index["entities"]["players:" + player_id][-1]
    expected_profile = read(DATA / ref["path"])[ref["ordinal"]]["observation"]
    assert values["profile"] == expected_profile
    manifest = read(DATA / "raw/index.json")
    chunk = next(c for s in manifest["seasons"] if s["id"] == "2026/2027" for c in s["chunks"] if c["leagueId"] == "l_3FJFUl")
    performance = next(p for p in read(DATA / chunk["tables"]["performances"]["path"]) if p["id"] == "m_49qvGz:" + player_id)
    identity = next(p for p in read(DATA / chunk["tables"]["players"]["path"]) if p["id"] == performance["playerRef"])
    expected_performance = {k: v for k, v in performance.items() if k != "playerRef"}
    expected_performance.update(name=identity["name"], imageUrl=identity["imageUrl"])
    assert values["performance"] == expected_performance
    report["playerSourcesCompared"] = len(values)

if (OUT / "browser-statistics.json").exists():
    stats = read(OUT / "browser-statistics.json")
    assert {k: len(v) for k, v in stats["team"].items()} == {p["period"]: p["metrics"] for p in report["teamPeriods"]}
    assert set(stats["player"]) == {p["period"] for p in report["playerPeriods"]}
    for period, rows in stats["player"].items():
        source = player if period == "All" else next(p for p in halves["periods"] if p["period"] == period)
        expected = [(item.get("key") or label) for g in source["stats"] for label, item in g["stats"].items()]
        assert [r["key"] for r in rows] == expected, period
    report["statisticsCountsAndPlayerKeysMatch"] = True

(OUT / "source-inventory.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"canonicalShards": len(shards), "families": len(families), "httpMatches": len(references), "browserFamilies": len(report["browser"]), "playerSources": report.get("playerSourcesCompared"), "statistics": report.get("statisticsCountsAndPlayerKeysMatch")}, indent=2))
