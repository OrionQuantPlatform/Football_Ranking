"""Verify saved actual-browser observations of the placeholder ranking.
Run: python3 dashboard/outputs/player-ranking/verify_browser.py
"""
import json
from pathlib import Path

out = Path(__file__).resolve().parent
evidence = json.loads((out / "browser-evidence.json").read_text())
report = {"command": "python3 dashboard/outputs/player-ranking/verify_browser.py",
          "setup": evidence["setup"], "status": "failed", "checks": []}
try:
    for page in evidence["pages"]:
        assert page["heading"] == "Classement joueurs", page["name"]
        assert page["title"] == "Classement joueurs — Orion"
        assert page["active"] == ["Classement joueurs"]
        assert len(page["rows"]) == 30
        for expected, row in enumerate(page["rows"], 1):
            assert row == {"value": expected, "position": f"{expected:02}", "text": "À venir", "label": f"Rang {expected}, à venir", "visible": True}, (page["name"], expected)
        assert page["playerImages"] == page["playerLinks"] == 0
        assert not page["filters"]
        assert page["width"] == page["scrollWidth"]
        assert len(page["icons"]) == 1
        icon = page["icons"][0]
        assert icon["inHeading"] and not icon["inNavbar"]
        assert icon["width"] > 0 and icon["height"] > 0 and icon["gradient"]
        assert icon["hidden"] == "true"
        labels = [link["text"] for link in page["nav"]]
        assert len(labels) == 7 and "Classements" not in labels and "Joueurs" in labels
        if page["url"].startswith("https://"):
            assert page["scripts"] == 2
        report["checks"].append({"page": page["name"], "positions": 30, "headingIcons": 1, "navbarIcons": 0, "width": page["width"], "result": "passed"})
    if "dataRequests" in evidence:
        assert evidence["dataRequests"]
        assert not any("/seasons/" in r["url"] or ".json.gz" in r["url"] for r in evidence["dataRequests"])
        report["checks"].append({"scenario": "no-full-season-download", "result": "passed"})
    removed = json.loads((out / "removed-page.json").read_text())
    assert removed["status"] == 404 and removed["filesRemoved"]
    report["checks"].append({"scenario": "national-ranking-page-removed", "result": "passed"})
    if "clubRanking" in evidence:
        assert len(evidence["clubRanking"]["rows"]) == 6
        assert evidence["clubRanking"]["heading"] == "Classement UEFA"
        report["checks"].append({"scenario": "club-uefa-history-preserved", "result": "passed"})
    report["status"] = "passed"
finally:
    (out / "browser-results.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(report, ensure_ascii=False, indent=2))
