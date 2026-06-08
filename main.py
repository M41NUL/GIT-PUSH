#!/usr/bin/env python3
# ─────────────────────────────────────────
#  GIT-PUSH — main.py
#  Dev: Md. Mainul Islam (CODEX-M41NUL)
# ─────────────────────────────────────────

import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils   import clear, print_success, print_info, separator
from banner  import show_banner
from updater import check_and_update
from auth    import login_screen
from menu    import show_menu

O   = "\033[38;5;208m"
G   = "\033[92m"
W   = "\033[97m"
B   = "\033[1m"
RST = "\033[0m"

def main():
    clear()
    show_banner()
    separator(color=O)
    print_info("Initializing GIT-PUSH...")
    print()

    try:
        check_and_update()
    except KeyboardInterrupt:
        pass
    except Exception:
        pass

    print()
    print_success("Ready!")
    time.sleep(1)

    # Login screen — runs once, skips if token already saved
    token, username = login_screen()
    if not token:
        print_info("Exiting.")
        sys.exit(0)

    # Main menu
    show_menu(token, username)

if __name__ == "__main__":
    main()
