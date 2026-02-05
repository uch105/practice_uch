#!/bin/bash
# generate_docs_clean.sh - Version with ANSI color code removal

DOC_DIR="$HOME/.linux-command-docs"
mkdir -p "$DOC_DIR/docs"

# Function to remove ANSI color codes
clean_ansi() {
    sed -e 's/\x1b\[[0-9;]*m//g'
}

# Function to clean command names
clean_command() {
    local cmd="$1"
    echo "$cmd" | tr -cd '[:alnum:]_.-' | sed 's/^[^a-zA-Z0-9]*//;s/[^a-zA-Z0-9]*$//'
}

# Main documentation generation
COUNT=0
TOTAL_COMMANDS=0
FAILED_COMMANDS=()

echo "Finding all system commands..."
find /usr/bin /usr/sbin /bin /sbin /usr/local/bin -type f -executable -printf "%f\n" 2>/dev/null > "$DOC_DIR/all_commands.tmp"

[ -d "/snap/bin" ] && find "/snap/bin" -type l -exec readlink -f {} \; 2>/dev/null | xargs -I{} basename {} >> "$DOC_DIR/all_commands.tmp"

sort -u "$DOC_DIR/all_commands.tmp" > "$DOC_DIR/all_commands.txt"
TOTAL_COMMANDS=$(wc -l < "$DOC_DIR/all_commands.txt")

echo "Generating clean documentation for $TOTAL_COMMANDS commands..."

while read -r raw_cmd; do
    cmd=$(clean_command "$raw_cmd")
    [ -z "$cmd" ] && continue
    
    output_file="$DOC_DIR/docs/$cmd.txt"
    
    # Skip if already processed
    [ -s "$output_file" ] && continue

    # Try man page with ANSI removal
    if man "$cmd" >/dev/null 2>&1; then
        man -Tutf8 "$cmd" | col -bx | clean_ansi > "$output_file" 2>/dev/null || rm -f "$output_file"
    fi

    # Fallback to --help
    if [ ! -s "$output_file" ]; then
        "$cmd" --help 2>&1 | head -n 50 | clean_ansi > "$output_file" 2>/dev/null || {
            rm -f "$output_file"
            echo "No docs: $cmd" > "$output_file"
        }
    fi

    COUNT=$((COUNT + 1))
    echo -ne "Processed $COUNT/$TOTAL_COMMANDS commands ($cmd)\r"
done < "$DOC_DIR/all_commands.txt"

echo -e "\nDocumentation generated in $DOC_DIR/docs"
echo "Cleaning existing files from ANSI codes..."

# Clean all existing files (in case you need to fix old ones)
find "$DOC_DIR/docs" -name "*.txt" -exec sed -i 's/\x1b\[[0-9;]*m//g' {} \;

echo "Done! All ANSI color codes removed."
