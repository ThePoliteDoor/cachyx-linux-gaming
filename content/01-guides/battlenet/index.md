# Install Battle.net on Linux using Steam Proton

![Battle.net on Linux](/images/battlenet-linux.png)

This guide installs **Battle.net** as a **Non-Steam Game** and runs it using **Proton**.

> This is the simplest and most reliable way to run Blizzard games on Linux.

## Tested setup

- Steam (native Linux)
- Proton Experimental / Proton 10
- CachyOS

## Step 1: Download the installer

Download Battle.net from the official site:

- https://www.blizzard.com/download

Save the file somewhere easy to find. For example, I saved it in the folder where I will install the game for easy reference.

## Step 2: Add Battle.net to Steam

1. Open Steam
2. Click **Games → Add a Non-Steam Game**
3. Browse and select `Battle.net-Setup.exe`
4. Right-click the entry → **Properties**
5. Enable in the Compatibility tab **- Force the use of a compatibility tool**
6. Select **Proton Experimental** or **Proton 10 (recommended)**

## Step 3: Fix the install location (IMPORTANT)

You can skip this step, but it is strongly recommended to avoid issues later on.

By default, Steam installs Proton data inside your home folder.
If you install games on a different partition, Battle.net may fail due to incorrect disk size detection.

Set this in **Properties/Launch Options**:

`STEAM_COMPAT_DATA_PATH=/games/Steam/Battlenet %command%`

Replace the path with wherever you plan to install Battle.net.

Why this matters:

- Avoids the fake xGB free space bug
- Keeps games off `/home`
- Makes cleanup and backups easy

## Step 4: Run the installer

1. Click **Play** in Steam
2. Install Battle.net normally
3. Log in to verify it works
4. Close Battle.net

> First launch may freeze. Restart it if needed.

## Step 5: Rename and Change Shortcut

1. Right-click the **Battle.net-Setup.exe** → **Properties**
2. In the Shortcut tab, rename it to **Battle.net**
3. Click the empty icon and apply your downloaded icon
4. Set **TARGET** and **START IN** as shown below

The exact path depends on where you installed Battle.net.

TARGET: `"/games/Steam/Battlenet/pfx/drive_c/Program Files (x86)/Battle.net/Battle.net.exe"`

START IN: `/games/Steam/Battlenet/pfx/drive_c/Program Files (x86)/Battle.net/`


How to find your Battle.net install path (Terminal)

`sudo find / \( -iname "*battle.net*" -o -iname "*battlenet*" \) 2>/dev/null`


## Step 6: Install games

**All** Blizzard games will install inside:
`/games/Steam/Battlenet/`


- [World of Warcraft on Linux](/games/world-of-warcraft/)

## Common problems

- Installer shows low disk space -> prefix not set
- Stuck on updating Blizzard Agent -> restart Battle.net
- Blank window -> relaunch from Steam

More fixes are listed in the troubleshooting section.

## Prefer video?

Watch the full step-by-step video guide here:
[link](https://youtu.be/2PO4FA-5CZI)
