# ─────────────────────────────────────────
#  GIT-PUSH — config.py
#  Dev: Md. Mainul Islam (CODEX-M41NUL)
# ─────────────────────────────────────────

from datetime import datetime
import os

TOOL_NAME       = "GIT-PUSH"
VERSION         = "1.0.0"
GITHUB_USER     = "M41NUL"
GITHUB_REPO     = "GIT-PUSH"

GITHUB_RAW      = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/main"
GITHUB_API_BASE = "https://api.github.com"
VERSION_URL     = f"{GITHUB_RAW}/config.py"

TOKEN_FILE      = os.path.expanduser("~/.gitpush_token")

DEV_NAME        = "Md. Mainul Islam"
DEV_BRAND       = "CODEX-M41NUL"
DEV_GITHUB      = "github.com/M41NUL"
DEV_TELEGRAM    = "t.me/mdmainulislaminfo"
DEV_CHANNEL     = "t.me/codexm41nul"
DEV_GROUP       = "t.me/codex_m41nul"
DEV_EMAIL       = "devmainulislam@gmail.com"
DEV_YOUTUBE     = "youtube.com/@codexm41nul"
DEV_WHATSAPP    = "+8801308850528"

YEAR            = datetime.now().year
COPYRIGHT       = f"© {YEAR} CODEX-M41NUL. All Rights Reserved."
