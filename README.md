<div align="center">

```
  ██████╗ ██╗████████╗      ██████╗ ██╗   ██╗███████╗██╗  ██╗
 ██╔════╝ ██║╚══██╔══╝      ██╔══██╗██║   ██║██╔════╝██║  ██║
 ██║  ███╗██║   ██║   █████╗██████╔╝██║   ██║███████╗███████║
 ██║   ██║██║   ██║   ╚════╝██╔═══╝ ██║   ██║╚════██║██╔══██║
 ╚██████╔╝██║   ██║         ██║     ╚██████╔╝███████║██║  ██║
  ╚═════╝ ╚═╝   ╚═╝         ╚═╝      ╚═════╝ ╚══════╝╚═╝  ╚═╝
```

**GitHub File Uploader for Termux**

[![Version](https://img.shields.io/badge/version-1.0.0-brightgreen?style=flat-square)](https://github.com/M41NUL/GIT-PUSH)
[![Platform](https://img.shields.io/badge/platform-Termux%20%7C%20Android-orange?style=flat-square)](https://github.com/M41NUL/GIT-PUSH)
[![Language](https://img.shields.io/badge/language-Python%203-blue?style=flat-square)](https://github.com/M41NUL/GIT-PUSH)
[![License](https://img.shields.io/badge/license-MIT-red?style=flat-square)](https://github.com/M41NUL/GIT-PUSH)
[![Author](https://img.shields.io/badge/dev-CODEX--M41NUL-yellow?style=flat-square)](https://github.com/M41NUL)
[![Telegram](https://img.shields.io/badge/Telegram-Channel-2CA5E0?style=flat-square&logo=telegram)](https://t.me/codexm41nul)
[![Stars](https://img.shields.io/github/stars/M41NUL/GIT-PUSH?style=flat-square&color=yellow)](https://github.com/M41NUL/GIT-PUSH/stargazers)
[![Forks](https://img.shields.io/github/forks/M41NUL/GIT-PUSH?style=flat-square&color=blue)](https://github.com/M41NUL/GIT-PUSH/network/members)
[![Issues](https://img.shields.io/github/issues/M41NUL/GIT-PUSH?style=flat-square&color=red)](https://github.com/M41NUL/GIT-PUSH/issues)
[![Last Commit](https://img.shields.io/github/last-commit/M41NUL/GIT-PUSH?style=flat-square&color=brightgreen)](https://github.com/M41NUL/GIT-PUSH/commits/main)
[![Repo Size](https://img.shields.io/github/repo-size/M41NUL/GIT-PUSH?style=flat-square&color=orange)](https://github.com/M41NUL/GIT-PUSH)

</div>

---

## What is GIT-PUSH?

**GIT-PUSH** is a Termux-based GitHub file uploader tool. Upload single files, entire folders, or ZIP archives directly to any of your GitHub repositories — no git commands needed. Just run the tool, select your repo, and push.

> Upload files to GitHub from your Android device in seconds.

---

## Features

- Upload a single file to any repo
- Upload an entire folder (recursive, all files)
- Upload a ZIP file — auto-extracted and uploaded with folder structure preserved
- Create a new GitHub repository (public or private)
- GitHub token saved once — never asked again
- Repo list auto-loaded from your account
- Custom commit message for every upload
- Auto update check from GitHub on every launch
- Smart installer — skips already installed packages

---

## Project Structure

```
GIT-PUSH/
├── main.py        - Entry point (banner, update check, menu)
├── config.py      - Tool config, version, developer info
├── banner.py      - ASCII banner + auto-size info box
├── github_api.py  - GitHub API (upload, create repo, token validation)
├── uploader.py    - File, folder, ZIP upload logic
├── menu.py        - Interactive menu and input handlers
├── updater.py     - Auto update from GitHub
├── utils.py       - Colors, animations, progress bar, prompts
└── installer.sh   - Smart installer + storage permission + launcher
```

---

## Installation

### Step 1 - Clone the repo

```bash
git clone https://github.com/M41NUL/GIT-PUSH.git
cd GIT-PUSH
```

### Step 2 - Run installer

```bash
bash installer.sh
```

The installer will:
- Update Termux packages
- Install Python, pip, git
- Request Android storage permission via termux-setup-storage
- Skip already installed packages automatically
- Auto-launch main.py after a 3-second countdown

### Step 3 - Run manually (after first install)

```bash
cd GIT-PUSH
python main.py
```

---

## All Commands

| Command | Description |
|---------|-------------|
| `git clone https://github.com/M41NUL/GIT-PUSH.git` | Clone the repo |
| `cd GIT-PUSH` | Enter project folder |
| `bash installer.sh` | Install dependencies and launch |
| `python main.py` | Run tool manually |
| `git pull origin main` | Pull latest update manually |
| `rm -rf GIT-PUSH` | Remove / uninstall the tool |

---

## Uninstall

```bash
cd /sdcard
rm -rf GIT-PUSH
```

To also remove the saved token:

```bash
rm -f ~/.gitpush_token
```

---

## GitHub Token Setup

GIT-PUSH requires a GitHub Personal Access Token. You only need to enter it once.

**How to generate:**

1. Go to **GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)**
2. Click **Generate new token (classic)**
3. Set a name — example: `GIT-PUSH`
4. Select the following scopes:

| Scope | Required for |
|-------|-------------|
| `repo` | Upload files, create repos, read repo list |
| `delete_repo` | Delete repositories |
| `gist` | Create and manage gists |

5. Click **Generate token**
6. Copy the token — it will only be shown once
7. Paste it into GIT-PUSH on first run

> Token is stored locally at `~/.gitpush_token` on your device only. It is never sent anywhere except directly to the GitHub API.

---

## Menu Options

```
[1]  Upload File    - Upload a single file to a GitHub repo
[2]  Upload Folder  - Upload all files inside a folder to a GitHub repo
[3]  Upload ZIP     - Extract a ZIP and upload all contents to a GitHub repo
[4]  Create Repo    - Create a new GitHub repository
[5]  Settings       - Save or update your GitHub token
[0]  Exit
```

---

## Upload File Example

```
Enter file path          : /sdcard/myproject/main.py
Repo destination path    : main.py
Commit message           : Add main.py
```

```
+ Uploaded to: github.com/M41NUL/myrepo/blob/main/main.py
```

---

## Upload Folder Example

```
Enter folder path        : /sdcard/myproject/
Repo subfolder           : (leave blank for root)
Commit message           : Upload project files
```

```
  [1/5]  main.py
  [2/5]  config.py
  [3/5]  static/style.css
  [4/5]  templates/index.html
  [5/5]  README.md

+ Done. Uploaded: 5/5  |  Failed: 0
+ Repo: github.com/M41NUL/myrepo
```

---

## Upload ZIP Example

```
Enter ZIP file path      : /sdcard/myproject.zip
Repo subfolder           : (leave blank for root)
Commit message           : Upload project from ZIP
```

ZIP structure is preserved exactly as-is inside the repo.

```
myproject.zip
├── main.py
├── config.py
└── static/
    └── style.css

Uploaded as:
repo/
├── main.py
├── config.py
└── static/style.css
```

---

## Create Repo Example

```
Enter repository name    : my-new-project
Enter description        : My awesome project
Visibility               : public
```

```
+ Repo created: https://github.com/M41NUL/my-new-project
```

---

## Developer

<div align="center">

| | |
|--|--|
| **Name** | Md. Mainul Islam |
| **Brand** | CODEX-M41NUL |
| **GitHub** | [github.com/M41NUL](https://github.com/M41NUL) |
| **Telegram** | [t.me/mdmainulislaminfo](https://t.me/mdmainulislaminfo) |
| **Channel** | [t.me/codexm41nul](https://t.me/codexm41nul) |
| **Group** | [t.me/codex_m41nul](https://t.me/codex_m41nul) |
| **YouTube** | [youtube.com/@codexm41nul](https://youtube.com/@codexm41nul) |
| **WhatsApp** | +8801308850528 |
| **Email** | devmainulislam@gmail.com |

</div>

---

## Support

If this tool helped you, give it a star on GitHub and join the Telegram channel for updates.

[![Star on GitHub](https://img.shields.io/github/stars/M41NUL/GIT-PUSH?style=social)](https://github.com/M41NUL/GIT-PUSH)
[![Telegram](https://img.shields.io/badge/Join-Telegram%20Channel-2CA5E0?style=flat-square&logo=telegram)](https://t.me/codexm41nul)

---

<div align="center">
<sub>© 2026 CODEX-M41NUL. All Rights Reserved.</sub>
</div>
