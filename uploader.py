# ─────────────────────────────────────────
#  GIT-PUSH — uploader.py
#  Dev: Md. Mainul Islam (CODEX-M41NUL)
# ─────────────────────────────────────────

import os, sys, zipfile, tempfile, shutil
from github_api import upload_file, get_file_sha
from utils      import print_success, print_error, print_info, print_warn, \
                       step_progress, progress_bar, confirm
from watermark  import add_watermark

G   = "\033[92m"
R   = "\033[91m"
O   = "\033[38;5;208m"
W   = "\033[97m"
B   = "\033[1m"
RST = "\033[0m"


def _read_bytes(path):
    with open(path, "rb") as f:
        return f.read()


def _upload_single(token, owner, repo, local_path, repo_path, commit_msg):
    try:
        content = _read_bytes(local_path)
    except Exception as e:
        print_error(f"Cannot read: {e}")
        return False
    sha     = get_file_sha(token, owner, repo, repo_path)
    ok, _   = upload_file(token, owner, repo, repo_path, content, commit_msg, sha)
    return ok


def upload_single_file(token, owner, repo, local_path, repo_path, commit_msg):
    progress_bar("Uploading file", total=20)
    ok = _upload_single(token, owner, repo, local_path, repo_path, commit_msg)
    if ok:
        print_success(f"Uploaded : {repo_path}")
        _watermark_prompt(token, owner, repo)
    else:
        print_error(f"Failed   : {repo_path}")
    return ok


def upload_folder(token, owner, repo, local_folder, repo_prefix, commit_msg):
    file_list = []
    for root, dirs, files in os.walk(local_folder):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for fname in files:
            if fname.startswith("."): continue
            full  = os.path.join(root, fname)
            rel   = os.path.relpath(full, local_folder).replace("\\", "/")
            rpath = f"{repo_prefix}/{rel}" if repo_prefix else rel
            file_list.append((full, rpath))

    total = len(file_list)
    if total == 0:
        print_warn("No files found.")
        return 0, 0, 0

    print_info(f"Found {total} file(s). Uploading...\n")
    ok_count = fail_count = 0

    for i, (full_path, repo_path) in enumerate(file_list, 1):
        fname = os.path.basename(full_path)
        step_progress(fname, i, total)
        ok = _upload_single(token, owner, repo, full_path, repo_path, commit_msg)
        if ok: ok_count += 1
        else:  fail_count += 1

    print()
    _watermark_prompt(token, owner, repo)
    return ok_count, fail_count, total


def upload_zip(token, owner, repo, zip_path, repo_prefix, commit_msg):
    if not zipfile.is_zipfile(zip_path):
        print_error("Invalid ZIP file.")
        return 0, 0, 0

    tmp_dir = tempfile.mkdtemp(prefix="gitpush_")
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(tmp_dir)
        entries = os.listdir(tmp_dir)
        root    = os.path.join(tmp_dir, entries[0]) \
                  if len(entries) == 1 and os.path.isdir(os.path.join(tmp_dir, entries[0])) \
                  else tmp_dir
        return upload_folder(token, owner, repo, root, repo_prefix, commit_msg)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def _watermark_prompt(token, owner, repo):
    """Ask user if they want to add UPLOADED_WITH.md to the repo."""
    print()
    if confirm("Add 'Uploaded with GIT-PUSH' credit file to this repo?"):
        ok = add_watermark(token, owner, repo)
        if ok:
            print_success("UPLOADED_WITH.md added to repo.")
        else:
            print_error("Could not add credit file.")
