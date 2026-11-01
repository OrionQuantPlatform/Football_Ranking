"""Reconcile saved production DOM/network observations from the real browser.

Run from repository root:
python3 dashboard/outputs/vercel-insights/verify_browser.py
"""
import json
from pathlib import Path
from urllib.parse import urlparse

out = Path(__file__).resolve().parent
evidence = json.loads((out / "browser-evidence.json").read_text())
report = {
    "command": "python3 dashboard/outputs/vercel-insights/verify_browser.py",
    "setup": evidence["setup"],
    "expected": "One versioned SDK script per integration on every route, production scripts and telemetry POSTs return 200, no duplicate scripts after client navigation.",
    "status": "failed",
    "checks": [],
}
expected = {"@vercel/speed-insights/next": "2.0.0", "@vercel/analytics/next": "2.0.1"}
try:
    for page in evidence["pages"]:
        scripts = page["scripts"]
        assert len(scripts) == 2, page["name"]
        assert {s["sdk"]: s["version"] for s in scripts} == expected
        for script in scripts:
            assert script["defer"] and urlparse(script["src"]).scheme == "https"
            if "speed-insights" in script["sdk"]:
                assert script["route"] == urlparse(page["url"]).path
        if "loading-shell" not in page["name"]:
            assert page.get("heading") and len(page["nav"]) == 7
        report["checks"].append({"page": page["name"], "url": page["url"], "sdkScripts": 2, "result": "passed"})
    requests = {}
    for event in evidence["network"]:
        request = requests.setdefault(event["requestId"], {})
        request.update({key: event[key] for key in ("url", "method", "status") if key in event})
    prefixes = {s["sdk"]: s["src"].rsplit("/", 1)[0] for s in evidence["pages"][0]["scripts"]}
    for sdk, base in prefixes.items():
        assert any(r.get("url") == base + "/script.js" and r.get("method") == "GET" and r.get("status") == 200 for r in requests.values()), sdk
        endpoint = "/vitals" if "speed-insights" in sdk else "/view"
        posts = [r for r in requests.values() if r.get("url") == base + endpoint and r.get("method") == "POST" and r.get("status") == 200]
        assert len(posts) >= (1 if "speed-insights" in sdk else 3), sdk
        report["checks"].append({"sdk": sdk, "scriptStatus": 200, "successfulTelemetryPosts": len(posts), "result": "passed"})
    errors = [e for e in evidence.get("console", []) if e["level"] == "error" and any(s in e["message"].lower() for s in ("analytics", "speed-insights"))]
    assert not errors, errors
    report["status"] = "passed"
finally:
    (out / "browser-results.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(report, ensure_ascii=False, indent=2))
