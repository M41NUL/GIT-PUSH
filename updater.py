# ─────────────────────────────────────────
#  GIT-PUSH — updater.py
#  Dev: Md. Mainul Islam (CODEX-M41NUL)
# ─────────────────────────────────────────

import urllib.request
import re
import os
import time
from config import VERSION, GITHUB_RAW
from utils  import animated_dots, print_success, print_info, print_warn

FILES_TO_UPDATE = [
    "main.py", "config.py", "banner.py", "updater.py",
    "github_api.py", "uploader.py", "menu.py", "utils.py"
]

def _fetch(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "GIT-PUSH/updater"})
        with urllib.request.urlopen(req, timeout=8) as r:
            return r.read().decode("utf-8")
    except Exception:
        return None

def _parse_version(raw):
    m = re.search(r'VERSION\s*=\s*["\']([^"\']+)["\']', raw)
    return m.group(1) if m else None

def _version_tuple(v):
    try:    return tuple(int(x) for x in v.strip().split("."))
    except: return (0,)

def check_and_update():
    animated_dots("Checking for updates", duration=5)
    raw = _fetch(f"{GITHUB_RAW}/config.py")
    if raw is None:
        print_warn("Could not reach GitHub. Skipping update check.")
        return False

    remote_ver = _parse_version(raw)
    if remote_ver is None:
        print_warn("Could not parse remote version.")
        return False

    if _version_tuple(remote_ver) <= _version_tuple(VERSION):
        print_success(f"Already up to date  (v{VERSION})")
        return False

    print_info(f"Update found: v{VERSION} -> v{remote_ver}")
    _apply_update(remote_ver)
    return True

def _apply_update(new_ver):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    failed   = []
    for fname in FILES_TO_UPDATE:
        url  = f"{GITHUB_RAW}/{fname}"
        data = _fetch(url)
        if data is None:
            failed.append(fname)
            continue
        try:
            with open(os.path.join(base_dir, fname), "w", encoding="utf-8") as f:
                f.write(data)
        except Exception:
            failed.append(fname)

    if failed:
        print_warn(f"Some files failed to update: {', '.join(failed)}")
    else:
        print_success(f"Updated to v{new_ver} successfully!")
        time.sleep(1)
