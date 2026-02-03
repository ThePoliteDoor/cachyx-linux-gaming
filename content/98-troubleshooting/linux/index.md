# Linux Troubleshooting

![Linux terminal](/images/linux-terminal.png)

Common issues and fixes for Steam Proton and Battle.net.

## How to open your Terminal

**Ctrl + Alt + T**

## How to find where Battle.net Installed

`sudo find / \( -iname "*battle.net*" -o -iname "*battlenet*" \) 2>/dev/null`

## Battle.net shows only xGB free

Cause:
Battle.net reads fake disk space from the Proton prefix.

Fix:
`STEAM_COMPAT_DATA_PATH=/games/Steam/Battlenet %command%`

## Battle.net stuck updating agent

Fix:
1. Close Battle.net
2. Restart Steam
3. Launch Battle.net again

## Game won’t launch after update

Fix:
- Switch to Proton Experimental or 10
- Restart Steam

## Where to find World of Warcraft addons

`sudo find / -type d -iname "AddOns" 2>/dev/null | grep -i "World of Warcraft"`

## How to make an Application Executable

`chmod +x "filename.appimage"`
