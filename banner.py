# ─────────────────────────────────────────
#  GIT-PUSH — banner.py
#  Dev: Md. Mainul Islam (CODEX-M41NUL)
# ─────────────────────────────────────────

from config import (TOOL_NAME, VERSION, DEV_NAME, DEV_BRAND, DEV_GITHUB,
                    DEV_TELEGRAM, DEV_CHANNEL, DEV_GROUP, DEV_EMAIL,
                    DEV_YOUTUBE, DEV_WHATSAPP, COPYRIGHT)

G   = "\033[92m"
R   = "\033[91m"
O   = "\033[38;5;208m"
W   = "\033[97m"
B   = "\033[1m"
DIM = "\033[2m"
RST = "\033[0m"

ASCII_ART = f"""{G}{B}
  ██████╗ ██╗████████╗      ██████╗ ██╗   ██╗███████╗██╗  ██╗
 ██╔════╝ ██║╚══██╔══╝      ██╔══██╗██║   ██║██╔════╝██║  ██║
 ██║  ███╗██║   ██║   █████╗██████╔╝██║   ██║███████╗███████║
 ██║   ██║██║   ██║   ╚════╝██╔═══╝ ██║   ██║╚════██║██╔══██║
 ╚██████╔╝██║   ██║         ██║     ╚██████╔╝███████║██║  ██║
  ╚═════╝ ╚═╝   ╚═╝         ╚═╝      ╚═════╝ ╚══════╝╚═╝  ╚═╝{RST}"""

TITLE_ROW = f"{TOOL_NAME}  v{VERSION}  -  GitHub File Uploader"

INFO_ROWS = [
    ("Tool",      TOOL_NAME, G),
    ("Version",   VERSION,   G),
    ("Dev",       DEV_NAME,  O),
    ("Brand",     DEV_BRAND, O),
]

LINK_ROWS = [
    ("GitHub",   DEV_GITHUB,   G),
    ("Telegram", DEV_TELEGRAM, O),
    ("Channel",  DEV_CHANNEL,  O),
    ("Group",    DEV_GROUP,    O),
    ("YouTube",  DEV_YOUTUBE,  R),
    ("WhatsApp", DEV_WHATSAPP, G),
    ("Email",    DEV_EMAIL,    W),
]

ALL_ROWS = INFO_ROWS + LINK_ROWS

def _calc_width():
    label_w = max(len(r[0]) for r in ALL_ROWS)
    max_row = max(1 + label_w + 2 + len(r[1]) + 1 for r in ALL_ROWS)
    title_w = len(TITLE_ROW) + 4
    copy_w  = len(COPYRIGHT) + 4
    return max(max_row, title_w, copy_w), label_w

def show_banner():
    print(ASCII_ART)
    _info_box()

def _info_box():
    W_BOX, label_w = _calc_width()

    def border(l, r):
        return f"{O}{B}{l}{'-' * W_BOX}{r}{RST}"

    def mid():
        return f"{O}{B}+{'-' * W_BOX}+{RST}"

    def center_row(text, tc=G):
        vlen = len(text)
        lpad = (W_BOX - vlen) // 2
        rpad = W_BOX - vlen - lpad
        return f"{O}{B}|{RST}{' ' * lpad}{tc}{B}{text}{RST}{' ' * rpad}{O}{B}|{RST}"

    def data_row(label, value, lc=O, vc=W):
        lbl_pad = label_w - len(label)
        used    = 1 + label_w + 2 + len(value) + 1
        rpad    = W_BOX - used
        return (
            f"{O}{B}|{RST}"
            f" {lc}{B}{label}{RST}{' ' * lbl_pad}"
            f"  {vc}{value}{RST}"
            f"{' ' * max(rpad, 0)}"
            f"{O}{B}|{RST}"
        )

    print(border("+", "+"))
    print(center_row(TITLE_ROW))
    print(mid())
    for label, value, lc in INFO_ROWS:
        print(data_row(label, value, lc=lc))
    print(mid())
    for label, value, lc in LINK_ROWS:
        print(data_row(label, value, lc=lc))
    print(mid())
    print(center_row(COPYRIGHT, tc=O))
    print(border("+", "+"))
    print()
