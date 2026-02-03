# World of Warcraft Addons on Linux

![WoW Addons on Linux](/images/wow-addons-linux.png)

This guide shows how to install and manage **World of Warcraft addons on Linux** using three reliable methods:

- Manual installation
- WowUp
- CurseForge

> Understanding manual installation first helps you troubleshoot and avoid common issues later.

## Tested setup

- OS: CachyOS (Arch-based Linux)
- Desktop: Wayland
- Game: World of Warcraft (Retail)
- Launcher: Battle.net (Steam Protn)
- Addon managers: WowUp, CurseForge

Other distros should work similarly, but paths and commands may differ.


## Step 1: Find your World of Warcraft folder

If you’re unsure where WoW is installed, open a terminal:

**Ctrl + Alt + T**

Run:

`sudo find / -type d -iname "AddOns" 2>/dev/null | grep -i "World of Warcraft"`

Depending on your install, you may see:

**_retail_**, **_classic_** or **_classic_era_**

Remember this path — you’ll need it for all addon methods.

## Step 2: Manual addon installation (recommended first)

Manual installation confirms that your addon path is correct.

1. Go to [Curseforge](https://www.curseforge.com/)
2. Search for an addon (example: *RareScanner*)
3. Download the addon as a ZIP file and Extract it
4. Navigate to: **World of Warcraft/_retail_/Interface/AddOns**
5. Move the extracted addon folder directly into AddOns.
6. Restart WoW or reload the UI: **/reload**
7. Open the AddOns menu and confirm it is enabled.

To remove a manually installed addon, simply delete its folder.

## Step 3: Using WowUp on Linux

WowUp is lightweight and works well on Linux.

1. Download the AppImage version for Linux [WowUp app](https://wowup.io/)
2. Make it executable: `chmod +x WowUp*.AppImage`
3. Run it: `./WowUp*.AppImage` or double **click** on the App
4. On first launch, WowUp will not auto-detect WoW. Add the game manually.
5. Once detected, you can search and install addons normally.

After installing addons, **/reload** the UI in the game

## Step 4: Using CurseForge on Linux

CurseForge works similarly to WowUp.

1. Download the AppImage version for Linux [CurseForge app](https://www.curseforge.com/download/app)
2. Make the AppImage executable: `chmod +x CurseForge*.AppImage`
3. Run it: `./CurseForge*.AppImage` or double **click** on the App
4. Manually point it to your WoW install
5. Once done, you can serach and install addons normally.

Reload the UI in-game to confirm if it works.

## Optional: Create desktop shortcuts (AppImages)

AppImages do not install system-wide.

1. Recommended approach: Create an Applications folder
2. Move AppImages to that folder
3. Right-click desktop **→** Create New **→** Link to Application
4. Set name, path, and optional icon

This works for WowUp, CurseForge, and other AppImages.

## Prefer video?

Watch the full step-by-step video guide here:
[link](https://youtu.be/KbhPr72LmpA)
