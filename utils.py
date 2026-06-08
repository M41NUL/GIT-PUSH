# ─────────────────────────────────────────
#  GIT-PUSH — utils.py
#  Dev: Md. Mainul Islam (CODEX-M41NUL)
# ─────────────────────────────────────────

import sys, time, os

G   = "\033[92m"
R   = "\033[91m"
O   = "\033[38;5;208m"
W   = "\033[97m"
B   = "\033[1m"
DIM = "\033[2m"
RST = "\033[0m"

def clear():
    os.system("clear")

def print_success(msg):
    print(f"{G}{B}  + {RST}{W}{msg}{RST}")

def print_error(msg):
    print(f"{R}{B}  x {RST}{W}{msg}{RST}")

def print_info(msg):
    print(f"{O}{B}  > {RST}{W}{msg}{RST}")

def print_warn(msg):
    print(f"{O}{B}  ! {RST}{W}{msg}{RST}")

def separator(width=60, color=O):
    print(f"{color}{'-' * width}{RST}")

def animated_dots(label, duration=3, color=G):
    """Spinner animation for a fixed duration."""
    frames = ["|", "/", "-", "\\"]
    end_at = time.time() + duration
    i = 0
    try:
        while time.time() < end_at:
            sys.stdout.write(f"\r  {color}{B}{frames[i % 4]}{RST}  {W}{label}{RST}  ")
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
        sys.stdout.write(f"\r  {G}{B}+{RST}  {W}{label} - Done!{RST}      \n")
        sys.stdout.flush()
    except KeyboardInterrupt:
        sys.stdout.write("\n")

def progress_bar(label, total=30, color=G):
    """
    Styled progress bar:
    [=========>          ]  45%  label
    """
    bar_width = 36
    for i in range(total + 1):
        filled   = int(bar_width * i / total)
        arrow    = "=" * max(filled - 1, 0) + (">" if filled > 0 else "")
        empty    = " " * (bar_width - filled)
        pct      = int(100 * i / total)
        elapsed  = i / total
        # Color shifts: red -> orange -> green
        if pct < 40:
            bc = R
        elif pct < 75:
            bc = O
        else:
            bc = G
        sys.stdout.write(
            f"\r  {bc}{B}[{arrow}{empty}]{RST}  {W}{pct:3d}%  {DIM}{label}{RST}"
        )
        sys.stdout.flush()
        time.sleep(0.05)
    print()

def step_progress(label, current, total, color=G):
    """
    Per-file upload progress:
    [  3 / 12 ]  >>>>>>>>>>>---------  25%  filename.py
    """
    bar_width = 24
    filled    = int(bar_width * current / total)
    bar       = ">" * filled + "-" * (bar_width - filled)
    pct       = int(100 * current / total)
    sys.stdout.write(
        f"\r  {O}{B}[{current:3d}/{total:3d}]{RST}  "
        f"{color}{B}[{bar}]{RST}  "
        f"{W}{pct:3d}%  {DIM}{label:<40}{RST}"
    )
    sys.stdout.flush()

def install_progress(label, total=40, color=G):
    """
    Installer-style progress bar with package name:
    Installing python  [=========================>     ]  88%
    """
    bar_width = 30
    for i in range(total + 1):
        filled = int(bar_width * i / total)
        bar    = "#" * filled + "-" * (bar_width - filled)
        pct    = int(100 * i / total)
        if pct < 40:
            bc = R
        elif pct < 80:
            bc = O
        else:
            bc = G
        sys.stdout.write(
            f"\r  {W}{label:<22}{RST}  {bc}{B}[{bar}]{RST}  {W}{pct:3d}%{RST}"
        )
        sys.stdout.flush()
        time.sleep(0.04)
    print()

def prompt(msg, color=O, example=None):
    if example:
        print(f"\n  {DIM}{W}Example : {example}{RST}")
    return input(f"\n  {color}{B}>{RST}  {W}{msg}{RST}  ").strip()

def pause(msg="Press ENTER to continue..."):
    input(f"\n  {O}{msg}{RST}")

def confirm(msg):
    """Returns True if user types Y/y."""
    ans = input(f"\n  {O}{B}?{RST}  {W}{msg} [Y/N]{RST}  ").strip()
    return ans.upper() == "Y"
