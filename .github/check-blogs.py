#!/usr/bin/env python3
"""Check that all blog URLs in guests.json return a successful HTTP response."""

import json
import sys
import urllib.request
import urllib.error

TIMEOUT = 10
SUCCESS_CODES = range(200, 400)  # 2xx and 3xx considered reachable

guests = json.load(open("guests.json"))
errors = []

for g in guests:
    url = g.get("blog", "")
    if not url:
        continue
    if g.get("skip_blog_check"):
        print(f"SKIP  {g['name']}  (bot-filter bypass)")
        continue
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            if r.status in SUCCESS_CODES:
                print(f"OK  {g['name']}  ({r.status})")
            else:
                errors.append(f"[{g['name']}] blog HTTP {r.status}: {url}")
    except urllib.error.HTTPError as e:
        if e.code in SUCCESS_CODES:
            print(f"OK  {g['name']}  ({e.code})")
        else:
            errors.append(f"[{g['name']}] blog HTTP {e.code}: {url}")
    except Exception as e:
        errors.append(f"[{g['name']}] blog unreachable: {url} ({e})")

if errors:
    print("\nErrors detected:")
    for err in errors:
        print(f"  ✗ {err}")
    sys.exit(1)
