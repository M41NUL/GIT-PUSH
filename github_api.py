# ─────────────────────────────────────────
#  GIT-PUSH — github_api.py
#  Dev: Md. Mainul Islam (CODEX-M41NUL)
# ─────────────────────────────────────────

import urllib.request
import urllib.error
import json
import base64
import os
from config import GITHUB_API_BASE

def _headers(token):
    return {
        "Authorization": f"token {token}",
        "Accept":        "application/vnd.github.v3+json",
        "Content-Type":  "application/json",
        "User-Agent":    "GIT-PUSH/1.0.0"
    }

def _request(method, url, token, data=None):
    body = json.dumps(data).encode("utf-8") if data else None
    req  = urllib.request.Request(url, data=body, headers=_headers(token), method=method)
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read().decode("utf-8")), r.status
    except urllib.error.HTTPError as e:
        try:
            err = json.loads(e.read().decode("utf-8"))
        except Exception:
            err = {}
        return err, e.code
    except Exception as e:
        return {"message": str(e)}, 0

def validate_token(token):
    """Check if token is valid by fetching user info."""
    data, status = _request("GET", f"{GITHUB_API_BASE}/user", token)
    if status == 200:
        return True, data.get("login", "")
    return False, ""

def get_repos(token):
    """Fetch all repos for authenticated user."""
    repos = []
    page  = 1
    while True:
        url        = f"{GITHUB_API_BASE}/user/repos?per_page=100&page={page}&sort=updated"
        data, status = _request("GET", url, token)
        if status != 200 or not data:
            break
        repos.extend(data)
        if len(data) < 100:
            break
        page += 1
    return repos

def create_repo(token, name, description="", private=False):
    """Create a new GitHub repository."""
    data, status = _request("POST", f"{GITHUB_API_BASE}/user/repos", token, {
        "name":        name,
        "description": description,
        "private":     private,
        "auto_init":   True
    })
    return status == 201, data

def get_file_sha(token, owner, repo, path):
    """Get SHA of existing file (needed for update)."""
    url        = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/contents/{path}"
    data, status = _request("GET", url, token)
    if status == 200:
        return data.get("sha")
    return None

def upload_file(token, owner, repo, path, content_bytes, commit_msg, sha=None):
    """
    Upload or update a single file to GitHub repo.
    content_bytes: raw bytes of the file.
    sha: existing file SHA for update (None for new file).
    """
    encoded = base64.b64encode(content_bytes).decode("utf-8")
    payload = {
        "message": commit_msg,
        "content": encoded,
        "branch":  "main"
    }
    if sha:
        payload["sha"] = sha

    url          = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/contents/{path}"
    data, status = _request("PUT", url, token, payload)
    return status in (200, 201), data
