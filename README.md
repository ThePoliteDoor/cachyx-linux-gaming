# Linux Gaming Guide

Practical, tested guides for running games on Linux using Steam Proton.
Focused on clear steps, minimal workarounds, and reproducible results.

## Common Linux Commands

**Open Terminal**
```bash
Ctrl + Alt + T

## Linux commands
Accessing Terminal: ctrl+alt+t

Battlenet Location: sudo find / \( -iname "*battle.net*" -o -iname "*battlenet*" \) 2>/dev/null

Wow Location: sudo find / -type d -iname "AddOns" 2>/dev/null | grep -i "World of Warcraft"
Making an App executable: chmod +x "filename.appimage"

## Live site
https://thepolitedoor.github.io/cachyx-linux-gaming

## Build locally
python build.py
