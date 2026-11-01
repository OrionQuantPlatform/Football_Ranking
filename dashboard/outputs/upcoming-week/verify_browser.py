"""Independent canonical-data oracle for saved browser DOM observations.

Run from the repository root:
python3 dashboard/outputs/upcoming-week/verify_browser.py
"""
import datetime as dt
import gzip
import hashlib
import json
import pathlib
import unicodedata
import urllib.parse
from zoneinfo import ZoneInfo

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = pathlib.Path(__file__).resolve().parent
PARIS = ZoneInfo("Europe/Paris")
FOCUS = {"l_4WFCIZ", "l_0ErfuF", "l_1Isor4", "l_0ALvwF", "l_3FJFUl",
         "l_4QexZg", "l_4H43wr", "l_0bfbkO", "l_38d9HA", "l_2WZ2tt"}
manifest = json.loads((ROOT / "data/raw/index.json").read_text())
evidence = json.loads((OUT / "browser-evidence.json").read_text())
report = {"command": "python3 dashboard/outputs/upcoming-week/verify_browser.py",
          "expected": "Visible IDs, order, team/league names and Paris times match canonical fixtures; pagination is complete.",
          "status": "failed", "checks": []}
page_groups = {}


def normalize(text):
    return "".join(c for c in unicodedata.normalize("NFD", text.lower())
                   if unicodedata.category(c) != "Mn")


try:
    for case in evidence["scenarios"]:
        if "fixtures" not in case:
            continue
        params = urllib.parse.parse_qs(urllib.parse.urlparse(case["url"]).query)
        value = lambda key, default="": params.get(key, [default])[0]
        now = dt.datetime.fromisoformat(case["capturedAt"].replace("Z", "+00:00"))
        today = now.astimezone(PARIS).date()
        selected_day = today
        if "/calendrier" in case["url"] and value("week"):
            try:
                selected_day = dt.date.fromisoformat(value("week"))
            except ValueError:
                pass
        monday = selected_day - dt.timedelta(days=selected_day.weekday())
        sunday = monday + dt.timedelta(days=6)
        season = next(s for s in manifest["seasons"] if s["id"] == value("season", manifest["defaultSeason"]))
        fixtures, sources = {}, []
        for chunk in season["chunks"]:
            if value("focus") == "europe" and chunk["leagueId"] not in FOCUS:
                continue
            source = chunk["tables"]["fixtures"]
            payload = (ROOT / "data" / source["path"]).read_bytes()
            assert hashlib.sha256(payload).hexdigest() == source["sha256"]
            sources.append(source["path"])
            for row in json.loads(gzip.decompress(payload)):
                if row["status"] != "not_started":
                    continue
                if value("league", "all") != "all" and row.get("league", {}).get("id") != value("league"):
                    continue
                names = " ".join([row.get("home_team", {}).get("name", ""), row.get("away_team", {}).get("name", ""), row.get("league", {}).get("name", "")])
                if normalize(value("q")) not in normalize(names):
                    continue
                try:
                    kickoff = dt.datetime.fromisoformat(str(row.get("time_utc") or "").replace("Z", "+00:00"))
                    if kickoff.tzinfo is None:
                        raise ValueError("ambiguous time")
                except (TypeError, ValueError, KeyError):
                    kickoff = None
                try:
                    day = kickoff.astimezone(PARIS).date() if kickoff else dt.date.fromisoformat(row["date"])
                except (TypeError, ValueError, KeyError):
                    continue
                if day < today or not monday <= day <= sunday or (kickoff and kickoff <= now):
                    continue
                fixtures.setdefault(row["id"], (row, day, kickoff))
        ordered = sorted(fixtures.values(), key=lambda item: (item[1], item[2] or dt.datetime.max.replace(tzinfo=dt.timezone.utc), item[0]["id"]))
        start = (case.get("page", 1) - 1) * 40
        expected = ordered[:6] if "/calendrier" not in case["url"] else ordered[start:start + 40]
        actual = case["fixtures"]
        # Simultaneous kickoffs have no sporting order. JS's locale collation of
        # opaque IDs differs from Python's ASCII order; compare chronology and
        # group membership, then reconcile every page together below.
        assert len(actual) == len(expected), case["name"]
        assert len({r["id"] for r in actual}) == len(actual), case["name"]
        chronology = lambda item: (item[1], item[2] or dt.datetime.max.replace(tzinfo=dt.timezone.utc))
        actual_keys = [chronology(fixtures[r["id"]]) for r in actual]
        assert actual_keys == sorted(actual_keys), case["name"]
        if expected:
            assert actual_keys[0] == chronology(expected[0]) and actual_keys[-1] == chronology(expected[-1]), case["name"]
        if len(ordered) <= (6 if "/calendrier" not in case["url"] else 40):
            assert {r["id"] for r in actual} == set(fixtures), case["name"]
        if case.get("page"):
            group = page_groups.setdefault(case["url"], {"expected": set(fixtures), "pages": {}})
            group["pages"][case["page"]] = [r["id"] for r in actual]
        for observed in actual:
            row, day, kickoff = fixtures[observed["id"]]
            for name in (row["home_team"]["name"], row["away_team"]["name"], row["league"]["name"]):
                assert name in observed["text"], (case["name"], name)
            if kickoff:
                assert dt.datetime.fromisoformat(observed["time"].replace("Z", "+00:00")) == kickoff
                assert observed["label"] == kickoff.astimezone(PARIS).strftime("%H:%M")
            else:
                assert not observed.get("time") and "Horaire à confirmer" in observed["text"]
            assert "0–0" not in observed["text"] and "0 – 0" not in observed["text"]
        report["checks"].append({"scenario": case["name"], "week": [str(monday), str(sunday)],
                                 "expectedTotal": len(ordered), "verifiedVisible": len(actual), "page": case.get("page", 1),
                                 "canonicalSources": len(sources), "result": "passed"})
    for url, group in page_groups.items():
        count = (len(group["expected"]) + 39) // 40
        if set(group["pages"]) == set(range(1, count + 1)):
            ids = [value for page in range(1, count + 1) for value in group["pages"][page]]
            assert len(ids) == len(set(ids)) == len(group["expected"])
            assert set(ids) == group["expected"]
            report["checks"].append({"scenario": "complete-pagination", "url": url, "verifiedUniqueFixtures": len(ids), "result": "passed"})
    report["status"] = "passed"
finally:
    (OUT / "oracle-results.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(report, ensure_ascii=False, indent=2))
