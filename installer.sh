#!/data/data/com.termux/files/usr/bin/bash
# ─────────────────────────────────────────
#  GIT-PUSH — installer.sh
#  Dev: Md. Mainul Islam (CODEX-M41NUL)
# ─────────────────────────────────────────

G="\033[92m"
R="\033[91m"
O="\033[38;5;208m"
W="\033[97m"
B="\033[1m"
DIM="\033[2m"
RST="\033[0m"

clear

echo -e "${G}${B}"
echo "  ██████╗ ██╗████████╗      ██████╗ ██╗   ██╗███████╗██╗  ██╗"
echo " ██╔════╝ ██║╚══██╔══╝      ██╔══██╗██║   ██║██╔════╝██║  ██║"
echo " ██║  ███╗██║   ██║   █████╗██████╔╝██║   ██║███████╗███████║"
echo " ██║   ██║██║   ██║   ╚════╝██╔═══╝ ██║   ██║╚════██║██╔══██║"
echo " ╚██████╔╝██║   ██║         ██║     ╚██████╔╝███████║██║  ██║"
echo "  ╚═════╝ ╚═╝   ╚═╝         ╚═╝      ╚═════╝ ╚══════╝╚═╝  ╚═╝"
echo -e "${RST}"
echo -e "  ${O}${B}Installer  v1.0.0  |  github.com/M41NUL${RST}"
echo -e "  ${W}GitHub File Uploader for Termux${RST}"
echo ""
echo -e "  ${O}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RST}"
echo ""

# ── Shade block progress bar ──────────────────────────────────────────────────
progress_bar() {
    local label="$1"
    local total=40
    local bar_width=24
    for i in $(seq 1 $total); do
        local filled=$(( bar_width * i / total ))
        local empty=$(( bar_width - filled ))

        local bar=""
        if [ $filled -gt 0 ]; then
            [ $filled -gt 1 ] && bar=$(printf '%0.s▓' $(seq 1 $(( filled - 1 ))))
            bar="${bar}▒"
        fi
        local emp=""
        [ $empty -gt 0 ] && emp=$(printf '%0.s░' $(seq 1 $empty))

        local pct=$(( 100 * i / total ))
        if   [ $pct -lt 40 ]; then bc="${R}"
        elif [ $pct -lt 80 ]; then bc="${O}"
        else bc="${G}"; fi

        printf "\r  ${W}%-22s${RST}  ${bc}${B}▕%s%s▏${RST}  ${W}%3d%%${RST}" \
               "$label" "$bar" "$emp" "$pct"
        sleep 0.03
    done
    echo ""
}

ok_msg()   { echo -e "  ${G}${B}+${RST}  ${W}$1${RST}"; }
skip_msg() { echo -e "  ${O}${B}o${RST}  ${DIM}${W}$1  (already installed)${RST}"; }
step_msg() { echo -e "\n  ${O}${B}>${RST}  ${W}$1${RST}"; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FLAG_FILE="$SCRIPT_DIR/.installed"
STORAGE_FLAG="$SCRIPT_DIR/.storage_granted"

# ── Already installed → just launch ──────────────────────────────────────────
if [ -f "$FLAG_FILE" ]; then
    echo -e "  ${G}${B}+  Already installed! Launching GIT-PUSH...${RST}\n"
    sleep 1
    cd "$SCRIPT_DIR"
    python main.py
    exit 0
fi

# ── Step 1: Update ────────────────────────────────────────────────────────────
step_msg "Updating package lists..."
progress_bar "apt update"
apt update -y -q 2>/dev/null
ok_msg "Package lists updated"

# ── Step 2: Python ────────────────────────────────────────────────────────────
step_msg "Checking Python..."
if command -v python &>/dev/null || command -v python3 &>/dev/null; then
    skip_msg "Python"
else
    progress_bar "Installing Python"
    apt install -y -q python 2>/dev/null || apt install -y -q python3 2>/dev/null
    ok_msg "Python installed"
fi

# ── Step 3: pip ───────────────────────────────────────────────────────────────
step_msg "Checking pip..."
if command -v pip &>/dev/null; then
    skip_msg "pip"
else
    progress_bar "Installing pip"
    apt install -y -q python-pip 2>/dev/null
    ok_msg "pip installed"
fi

# ── Step 4: git ───────────────────────────────────────────────────────────────
step_msg "Checking git..."
if command -v git &>/dev/null; then
    skip_msg "git"
else
    progress_bar "Installing git"
    apt install -y -q git 2>/dev/null
    ok_msg "git installed"
fi

# ── Step 5: requests ──────────────────────────────────────────────────────────
step_msg "Checking Python packages..."
if python -c "import requests" 2>/dev/null || python3 -c "import requests" 2>/dev/null; then
    skip_msg "requests"
else
    progress_bar "pip install requests"
    pip install requests -q 2>/dev/null
    ok_msg "requests installed"
fi

# ── Step 6: Storage permission ────────────────────────────────────────────────
echo ""
echo -e "  ${O}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RST}"

if [ -f "$STORAGE_FLAG" ] || [ -d "/sdcard/Android" ]; then
    echo -e "\n  ${G}${B}+  Storage permission already granted. Skipping.${RST}"
else
    echo -e "\n  ${G}${B}  Requesting Android storage permission...${RST}"
    echo -e "  ${W}A dialog will appear -- tap ALLOW to enable /sdcard access.${RST}\n"
    termux-setup-storage
    sleep 2
    touch "$STORAGE_FLAG"
    ok_msg "Storage permission granted"
fi

touch "$FLAG_FILE"

# ── Done ──────────────────────────────────────────────────────────────────────
echo ""
echo -e "  ${O}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RST}"
echo -e "\n  ${G}${B}+  Installation complete!${RST}\n"

for i in 3 2 1; do
    printf "\r  ${O}${B}Starting GIT-PUSH in ${G}$i${O}...${RST}   "
    sleep 1
done
echo -e "\r  ${G}${B}Launching GIT-PUSH...${RST}              \n"

cd "$SCRIPT_DIR"
python main.py
