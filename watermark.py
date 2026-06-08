# ─────────────────────────────────────────
#  GIT-PUSH — watermark.py
#  Dev: Md. Mainul Islam (CODEX-M41NUL)
# ─────────────────────────────────────────

from datetime import datetime
from github_api import upload_file, get_file_sha

WATERMARK_FILE = "UPLOADED_WITH.md"

WATERMARK_CONTENT = """\
# Uploaded with GIT-PUSH

| | |
|--|--|
| **Tool** | GIT-PUSH v1.0.0 |
| **Dev** | Md. Mainul Islam |
| **Brand** | CODEX-M41NUL |
| **GitHub** | [github.com/M41NUL](https://github.com/M41NUL) |
| **Telegram** | [t.me/codexm41nul](https://t.me/codexm41nul) |
| **Channel** | [t.me/codexm41nul](https://t.me/codexm41nul) |
| **Group** | [t.me/codex_m41nul](https://t.me/codex_m41nul) |
| **YouTube** | [youtube.com/@codexm41nul](https://youtube.com/@codexm41nul) |
| **WhatsApp** | +8801308850528 |
| **Email** | devmainulislam@gmail.com |

---

[![GIT-PUSH](https://img.shields.io/badge/Uploaded%20with-GIT--PUSH-brightgreen?style=flat-square)](https://github.com/M41NUL/GIT-PUSH)
[![CODEX-M41NUL](https://img.shields.io/badge/dev-CODEX--M41NUL-orange?style=flat-square)](https://github.com/M41NUL)
[![Telegram](https://img.shields.io/badge/Telegram-codexm41nul-2CA5E0?style=flat-square&logo=telegram)](https://t.me/codexm41nul)

---

<sub>© {year} CODEX-M41NUL. All Rights Reserved.</sub>
""".format(year=datetime.now().year)


def add_watermark(token, owner, repo):
    """Upload UPLOADED_WITH.md to the repo."""
    sha = get_file_sha(token, owner, repo, WATERMARK_FILE)
    ok, _ = upload_file(
        token, owner, repo,
        WATERMARK_FILE,
        WATERMARK_CONTENT.encode("utf-8"),
        "Add GIT-PUSH watermark",
        sha
    )
    return ok
