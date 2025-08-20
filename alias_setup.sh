#!/bin/bash

# Path to your executable
EXEC_PATH="$(pwd)/dist/matrix"

# Determine shell and RC file
if [ -n "$ZSH_VERSION" ]; then
    RC_FILE="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ]; then
    RC_FILE="$HOME/.bashrc"
else
    echo "Unsupported shell. Please manually add the alias."
    exit 1
fi

# Alias to add
ALIAS_CMD="alias matrix=\"$EXEC_PATH\""

# Check if alias already exists
if grep -Fxq "$ALIAS_CMD" "$RC_FILE"; then
    echo "Alias already exists in $RC_FILE"
else
    echo "$ALIAS_CMD" >> "$RC_FILE"
    echo "Alias added to $RC_FILE"
fi

echo "To activate the alias now, run: source $RC_FILE"
