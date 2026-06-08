# ─────────────────────────────────────────
#  GIT-PUSH — menu.py
#  Dev: Md. Mainul Islam (CODEX-M41NUL)
# ─────────────────────────────────────────

import os, sys, time
from config      import TOKEN_FILE
from github_api  import validate_token, get_repos, create_repo
from uploader    import upload_single_file, upload_folder, upload_zip
from auth        import load_token, save_token, delete_token
from utils       import (clear, print_success, print_error, print_info,
                          print_warn, separator, prompt, pause,
                          progress_bar, animated_dots)
from banner      import show_banner

G   = "\033[92m"
R   = "\033[91m"
O   = "\033[38;5;208m"
W   = "\033[97m"
B   = "\033[1m"
DIM = "\033[2m"
RST = "\033[0m"


# ── Repo selector ──────────────────────────────────────────────────────────────

def select_repo(token):
    animated_dots("Loading repositories", duration=2)
    repos = get_repos(token)
    if not repos:
        print_error("No repositories found.")
        return None

    print()
    separator()
    print(f"  {G}{B}  Your Repositories:{RST}\n")
    for i, r in enumerate(repos, 1):
        vis = "private" if r.get("private") else "public"
        print(f"  {O}{B}[{i:2d}]{RST}  {W}{r['full_name']}{RST}  {DIM}({vis}){RST}")
    separator()

    choice = prompt(f"Select repo [1-{len(repos)}]", example="1")
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(repos):
            owner, name = repos[idx]["full_name"].split("/", 1)
            return owner, name
    except (ValueError, IndexError):
        pass
    print_error("Invalid selection.")
    return None


# ── Menu header ────────────────────────────────────────────────────────────────

def _menu_header(username):
    print(f"\n  {O}{B}+{'=' * 44}+{RST}")
    print(f"  {O}{B}|{G}        MAIN MENU  --  GIT-PUSH          {O}|{RST}")
    print(f"  {O}{B}|{W}        Logged in as: {G}{username:<22}{O}|{RST}")
    print(f"  {O}{B}+{'=' * 44}+{RST}\n")

def _option(num, label, desc):
    print(f"  {O}{B}[{num}]{RST}  {G}{B}{label}{RST}")
    print(f"        {DIM}{W}{desc}{RST}\n")


# ── Main menu loop ─────────────────────────────────────────────────────────────

def show_menu(token, username):
    while True:
        clear()
        show_banner()
        _menu_header(username)
        _option("1", "Upload File",   "Upload a single file to a GitHub repo")
        _option("2", "Upload Folder", "Upload all files inside a folder to a GitHub repo")
        _option("3", "Upload ZIP",    "Extract a ZIP and upload all contents to a GitHub repo")
        _option("4", "Create Repo",   "Create a new GitHub repository")
        _option("5", "Settings",      "Manage your GitHub token")
        _option("0", "Exit",          "Quit GIT-PUSH")
        separator()

        choice = prompt("Select option", color=G)

        if   choice == "1": _handle_upload_file(token, username)
        elif choice == "2": _handle_upload_folder(token, username)
        elif choice == "3": _handle_upload_zip(token, username)
        elif choice == "4": _handle_create_repo(token)
        elif choice == "5":
            new_token, new_username = _handle_settings(token, username)
            if new_token:
                token    = new_token
                username = new_username
        elif choice == "0": _exit_tool(); break
        else:
            print_warn("Invalid option.")
            pause()


# ── Option 1: Upload File ──────────────────────────────────────────────────────

def _handle_upload_file(token, username):
    clear(); show_banner()
    print(f"\n  {G}{B}[ UPLOAD FILE ]{RST}\n")
    separator()

    result = select_repo(token)
    if not result: pause(); return
    owner, repo = result

    file_path = prompt("Enter file path", example="/sdcard/myproject/main.py")
    if not file_path: print_error("No path entered."); pause(); return
    file_path = os.path.expandvars(os.path.expanduser(file_path))
    if not os.path.isfile(file_path): print_error(f"File not found: {file_path}"); pause(); return

    fname      = os.path.basename(file_path)
    repo_path  = prompt("Repo destination path", example=fname)
    if not repo_path: repo_path = fname

    commit_msg = prompt("Commit message", example=f"Add {fname}")
    if not commit_msg: commit_msg = f"Upload {fname} via GIT-PUSH"

    print()
    progress_bar("Uploading", total=20)
    ok = upload_single_file(token, owner, repo, file_path, repo_path, commit_msg)
    if ok:
        print_success(f"Uploaded to: github.com/{owner}/{repo}/blob/main/{repo_path}")
    pause()


# ── Option 2: Upload Folder ────────────────────────────────────────────────────

def _handle_upload_folder(token, username):
    clear(); show_banner()
    print(f"\n  {G}{B}[ UPLOAD FOLDER ]{RST}\n")
    separator()

    result = select_repo(token)
    if not result: pause(); return
    owner, repo = result

    folder_path = prompt("Enter folder path", example="/sdcard/myproject/")
    if not folder_path: print_error("No path entered."); pause(); return
    folder_path = os.path.expandvars(os.path.expanduser(folder_path))
    if not os.path.isdir(folder_path): print_error(f"Folder not found: {folder_path}"); pause(); return

    repo_prefix = prompt("Repo subfolder (leave blank for root)", example="src")
    commit_msg  = prompt("Commit message", example="Upload project files")
    if not commit_msg: commit_msg = "Upload folder via GIT-PUSH"

    print()
    ok, fail, total = upload_folder(token, owner, repo, folder_path, repo_prefix, commit_msg)
    print()
    print_success(f"Done. Uploaded: {ok}/{total}  |  Failed: {fail}")
    if ok > 0:
        print_success(f"Repo: github.com/{owner}/{repo}")
    pause()


# ── Option 3: Upload ZIP ───────────────────────────────────────────────────────

def _handle_upload_zip(token, username):
    clear(); show_banner()
    print(f"\n  {G}{B}[ UPLOAD ZIP ]{RST}\n")
    separator()

    result = select_repo(token)
    if not result: pause(); return
    owner, repo = result

    zip_path = prompt("Enter ZIP file path", example="/sdcard/myproject.zip")
    if not zip_path: print_error("No path entered."); pause(); return
    zip_path = os.path.expandvars(os.path.expanduser(zip_path))
    if not os.path.isfile(zip_path): print_error(f"File not found: {zip_path}"); pause(); return

    repo_prefix = prompt("Repo subfolder (leave blank for root)", example="")
    commit_msg  = prompt("Commit message", example="Upload project from ZIP")
    if not commit_msg: commit_msg = "Upload ZIP contents via GIT-PUSH"

    print()
    print_info("Extracting ZIP and uploading...")
    print()
    ok, fail, total = upload_zip(token, owner, repo, zip_path, repo_prefix, commit_msg)
    print()
    print_success(f"Done. Uploaded: {ok}/{total}  |  Failed: {fail}")
    if ok > 0:
        print_success(f"Repo: github.com/{owner}/{repo}")
    pause()


# ── Option 4: Create Repo ──────────────────────────────────────────────────────

def _handle_create_repo(token):
    clear(); show_banner()
    print(f"\n  {G}{B}[ CREATE REPO ]{RST}\n")
    separator()

    repo_name   = prompt("Enter repository name", example="my-new-project")
    if not repo_name: print_error("No name entered."); pause(); return

    description = prompt("Enter description (optional)", example="My awesome project")
    vis         = prompt("Visibility — public or private", example="public")
    private     = vis.lower().strip() == "private"

    print()
    animated_dots("Creating repository", duration=2)
    ok, data = create_repo(token, repo_name, description, private)
    if ok:
        print_success(f"Repo created: {data.get('html_url', '')}")
    else:
        print_error(f"Failed: {data.get('message', 'Unknown error')}")
    pause()


# ── Option 5: Settings ─────────────────────────────────────────────────────────

def _handle_settings(token, username):
    """Returns (new_token, new_username) or (token, username) if unchanged."""
    while True:
        clear(); show_banner()
        print(f"\n  {G}{B}[ SETTINGS ]{RST}\n")
        separator()

        # Show current token info
        masked = token[:4] + "*" * (len(token) - 8) + token[-4:] if len(token) > 8 else "****"
        print(f"  {W}Logged in as : {G}{B}{username}{RST}")
        print(f"  {W}Token        : {DIM}{masked}{RST}")
        print(f"  {W}Token file   : {DIM}{TOKEN_FILE}{RST}")
        print()
        separator()
        print()
        _option("1", "Update Token", "Replace current token with a new one")
        _option("2", "Remove Token", "Delete saved token (will ask on next launch)")
        _option("0", "Back",         "Return to main menu")
        separator()

        choice = prompt("Select option", color=G)

        if choice == "1":
            new_token = prompt("Enter new GitHub token", example="ghp_xxxxxxxxxxxx")
            if not new_token: print_error("No token entered."); time.sleep(1); continue

            animated_dots("Validating token", duration=2)
            ok, new_username = validate_token(new_token)
            if not ok:
                print_error("Invalid token.")
                time.sleep(1); continue

            save_token(new_token)
            print_success(f"Token updated. Logged in as: {new_username}")
            time.sleep(1)
            return new_token, new_username

        elif choice == "2":
            confirm = prompt("Type YES to confirm token removal", example="YES")
            if confirm.strip().upper() == "YES":
                delete_token()
                print_success("Token removed.")
                print_warn("You will be asked to login on next launch.")
                time.sleep(2)
                return token, username
            else:
                print_info("Cancelled.")
                time.sleep(1)

        elif choice == "0":
            return token, username

        else:
            print_warn("Invalid option.")
            time.sleep(0.5)


# ── Exit ───────────────────────────────────────────────────────────────────────

def _exit_tool():
    print(f"\n  {G}{B}Goodbye from GIT-PUSH!{RST}")
    print(f"  {O}github.com/M41NUL  |  t.me/codexm41nul{RST}\n")
