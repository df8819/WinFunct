# WinFunct App

Random utility app for Windows with functions, scripts and options that have kinda annoyed me to search for or execute separately every damn time I need them 🤭🙈

### ***This is more of a "learning to code" repo that will change at will. It may provide useful features, but there will probably be bugs or some weird behaviours. Would be cool if a random chad would revamp the whole thing and add features I don't even know yet. Cheers*** 🍻

## Description

WinFunct is a Python application that provides various scripts and options to enhance your Windows experience. It offers a user-friendly graphical interface where you can easily access different functions and settings.

## Features

- **Wi-Fi Password Viewer**: View and copy the passwords of saved Wi-Fi networks.
- **IP Address Checker**: Retrieve and display your public IP address.
- **Disk Speedtest**: Test the speed of a specific disk drive on your system.
- **Bloatware Killer**: Uninstall non-essential apps and remove unnecessary PWA shortcuts.
- **Flush DNS**: Release and renew IP configurations and flush DNS cache.
- **User Account Creation**: Create a new Windows user account with admin privileges. _(This is deactivated due to a bug)_
- **Windows Activation**: Activate Microsoft Windows and Office products.
- **System Tools**: Quick access to various Windows system tools and settings.
- **Shutdown, Reboot, UEFI Boot, Sleep**: Perform power-related actions with ease.
- ...

## Requirements

- [Python 3.x](https://www.python.org/downloads/)
- [Git for Desktop](https://git-scm.com/downloads/)

## Auto Installation

1. Navigate to the directory of your choice, click into the address bar, type **"cmd"** and hit Enter.
2. Clone the repository with the command: `git clone https://github.com/df8819/WinFunct.git` in the **CMD** Window.
3. Double click: **"Update.bat"**. This will install all dependencies and update the cloned repository. Use this occasionally.
4. Double click: **"Run.bat"**. The typical ```py filename.py``` cmd command will not work, as the app demands elevated rights.

## Manual Installation

1. Navigate to the directory of your choice, click into the address bar, type **"cmd"** and hit Enter.
2. Clone the repository with the command: `git clone https://github.com/df8819/WinFunct.git` in the **CMD** Window.
3. Navigate to the project directory: `cd WinFunct`
4. Install the required libraries: `pip install -r requirements.txt`
5. Run the app: `python winfunct.py`

## Usage

1. Launch the app by executing `winfunct.py`.
2. Select the desired function or option from the available tabs.
3. Follow the on-screen instructions to perform the selected task.
4. Enjoy the enhanced functionality and convenience provided by WinFunct!

## Known Issues

- _Some features require administrative privileges to function properly. Make sure to run the app with administrator rights._ 🔺 (FIXED)
- _The "Kill Bloatware" script still needs a little love as it tends to be a quite aggressive_ 👀 (FIXED)
- _The "ARP scan" doesn't work when pyinstalled, as it will be shown in the py terminal_ 😐 (FIXED)

![Image](1701505006.png)

![Image](1701505092.png)
