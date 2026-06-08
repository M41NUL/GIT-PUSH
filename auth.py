# ─────────────────────────────────────────
#  GIT-PUSH — auth.py
#  Dev: Md. Mainul Islam (CODEX-M41NUL)
# ─────────────────────────────────────────

import os
from config     import TOKEN_FILE
from github_api import validate_token
from utils      import (clear, print_success, print_error, print_info,
                         print_warn, separator, prompt, animated_dots)
from banner     import show_banner

G   = "\033[92m"
R   = "\033[91m"
O   = "\033[38;5;208m"
W   = "\033[97m"
B   = "\033[1m"
DIM = "\033[2m"
RST = "\033[0m"


def load_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            t = f.read().strip()
            return t if t else None
    return None


def save_token(token):
    with open(TOKEN_FILE, "w") as f:
        f.write(token)
    os.chmod(TOKEN_FILE, 0o600)


def delete_token():
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)


def login_screen():
    """
    Show login page before main menu.
    If token already saved and valid  -> return token silently.
    If no token                       -> show login screen.
    Returns valid token string or None if user cancels.
    """
    token = load_token()

    # Token exists — validate silently
    if token:
        ok, username = validate_token(token)
        if ok:
            return token, username
        else:
            # Token invalid — force re-login
            delete_token()
            print_warn("Saved token is invalid or expired. Please login again.")

    # No token — show login screen
    while True:
        clear()
        show_banner()

        print(f"  {O}{B}+{'=' * 44}+{RST}")
        print(f"  {O}{B}|{G}           LOGIN  --  GIT-PUSH             {O}|{RST}")
        print(f"  {O}{B}+{'=' * 44}+{RST}")
        print()
        print(f"  {W}A GitHub Personal Access Token is required.{RST}")
        print(f"  {DIM}{W}Go to: GitHub → Settings → Developer settings{RST}")
        print(f"  {DIM}{W}       → Tokens (classic) → Generate new token{RST}")
        print(f"  {DIM}{W}Scopes: repo  |  delete_repo  |  gist{RST}")
        print(f"  {DIM}{W}Token is stored locally only (~/.gitpush_token){RST}")
        print()
        separator()
        print()
        print(f"  {O}{B}[1]{RST}  {W}Enter Token{RST}")
        print(f"  {O}{B}[0]{RST}  {W}Exit{RST}")
        print()
        separator()

        choice = prompt("Select option", color=G)

        if choice == "0":
            return None, None

        elif choice == "1":
            token = prompt("Enter GitHub Personal Access Token", example="ghp_xxxxxxxxxxxx")
            if not token:
                print_error("No token entered.")
                continue

            print()
            animated_dots("Validating token", duration=2)
            ok, username = validate_token(token)

            if not ok:
                print_error("Invalid token. Please check and try again.")
                import time; time.sleep(1)
                continue

            save_token(token)
            print_success(f"Login successful! Welcome, {username}")
            import time; time.sleep(1)
            return token, username

        else:
            print_warn("Invalid option.")
            import time; time.sleep(0.5)
