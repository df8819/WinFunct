# WinFunct App

Custom utility app for Windows to speed up functions, scripts and options which have annoyed me to search/execute every damn time I need them 👀

## Description / Features

This app combines a lot of useful functions or scripts for managing Windows. I consider it kinda useful after v1.6xx:

- Extracting Wifi passwords, disk speedtest or release/renew DNS
- Executing ChrisTitusTech WinUtils, MAS activation or a checksum verifier with all encryption algos predefined
- Link opener for a bunch of useful links, Win godmode settings, system info extraction/comparison or checking what apps have an active internet connection
- Options Tab is a settings dump for stuff that's usually annoying to find in Win
- Apps has some fun stuff like my old ChatGPT python interface, a hash cracker or a password/passphrase generator. That one is actually useful


## Requirements

- [Python 3.x](https://www.python.org/downloads/)
- [Git for Desktop](https://git-scm.com/downloads/)

## Auto Installation

1. Navigate to the directory of your choice, click into the address bar, type **"cmd"** and hit Enter.

2. Clone the repository with the command: `git clone https://github.com/df8819/WinFunct.git` in the **CMD** Window.

3. Double click: **"Update.bat"**. This will install all dependencies and update the cloned repository. Use this occasionally.

4. Double click: **"Run.bat"**. _(The typical ```python *.py``` cmd command will not work, as the app demands elevated rights via temporary VBS script.)_

5. It may be required to add an exclusion for this app in the Windows Virus settings, as many scripts in the app will auto-flag it as malicious🤐

## Known Issues

- _The "Update" function is a little weird when executed from the downloaded .exe and needs further testing. I implemented a logic that should recognize if the app runs from the .exe or venv, but it's still a little random_ 😐

- _The "Kill Bloatware" function needs some love and may don't work as intended_ 🤷‍♂️

- _Screenshots may not show the latest version of the app. (Theme-Selector with ttkbootstrap in the making)_ 👀

![Image](1701505001.png)

![Image](1701505091.png)

![Image](1709048179.png)