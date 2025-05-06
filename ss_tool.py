import os
import time
import datetime
import psutil
import winreg
from colorama import init, Fore

init(autoreset=True)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def format_time(timestamp):
    return time.strftime("%d/%m/%Y %H:%M", time.localtime(timestamp))

def print_header():
    header = (
        Fore.RED + "╔" + "═"*48 + "╗\n" +
        "║{:^48}║\n".format("SS TOOL for Widow Network") +
        "║{:^48}║\n".format("by 7Str1les") +
        "╚" + "═"*48 + "╝"
    )
    print(header)

def show_menu():
    clear()
    print_header()
    options = [
        "All", "Recent .exe Files", "Resource Packs", "Mods",
        "Recycle Bin Modification Date", "Recording", "Recent USB Devices",
        "Active Windows Processes", "Macros Software"
    ]
    for i, option in enumerate(options):
        print(Fore.MAGENTA + f"[{i}] {option}")
    print(Fore.RED + "[00] Exit\n")

def handle_choice(choice):
    actions = {
        '0': all_categories,
        '1': check_recent_exe_files,
        '2': check_resource_packs,
        '3': check_mods,
        '4': lambda: print(Fore.GREEN + f"Recycle Bin last modified on: {get_recycle_bin_modification_date()}"),
        '5': check_recording_apps,
        '6': check_recent_usb_devices,
        '7': check_active_processes,
        '8': check_macros_software
    }

    if choice == '00':
        print(Fore.RED + "\n[+] Exiting...")
        time.sleep(1.5)
        exit()
    elif choice in actions:
        print(f"\n[+] Executing option {choice}...\n")
        actions[choice]()
    else:
        print(Fore.RED + "\n[!] Invalid option.")

    input(Fore.CYAN + "\nPress Enter to return to menu...")

def main():
    while True:
        show_menu()
        choice = input(Fore.YELLOW + "Select an option: ")
        handle_choice(choice)

def check_recent_exe_files():
    print(Fore.CYAN + "\n[+] Checking recent .exe files...\n")
    user_home = os.path.expanduser("~")
    now = time.time()
    recent = []

    for root, _, files in os.walk(user_home):
        for file in files:
            if file.endswith(".exe"):
                path = os.path.join(root, file)
                try:
                    if now - os.path.getmtime(path) < 86400:
                        recent.append(path)
                        print(Fore.GREEN + f"[EXE] {path}")
                except:
                    continue
    if not recent:
        print(Fore.YELLOW + "No recent .exe files found.")

def check_resource_packs():
    print(Fore.CYAN + "\n[+] Checking resource packs...\n")
    path = os.path.join(os.getenv('APPDATA'), '.minecraft', 'resourcepacks')

    if not os.path.exists(path):
        print(Fore.YELLOW + "Resource packs folder not found.")
        return

    for file in os.listdir(path):
        tag = Fore.RED + "[ SUS ]" if 'xray' in file.lower() else Fore.GREEN + "[ LEGIT ]"
        print(f"{tag} {file}")

def check_mods():
    print(Fore.CYAN + "\n[+] Checking mods...\n")
    path = os.path.join(os.getenv('APPDATA'), '.minecraft', 'mods')

    if not os.path.exists(path):
        print(Fore.YELLOW + "Mods folder not found.")
        return

    for file in os.listdir(path):
        tag = Fore.RED + "[ SUS ]" if 'xray' in file.lower() else Fore.GREEN + "[ LEGIT ]"
        print(f"{tag} {file}")

def get_recycle_bin_modification_date():
    path = "C:\\$Recycle.Bin"
    if not os.path.exists(path):
        return "Recycle Bin folder not found."

    try:
        dt = datetime.datetime.fromtimestamp(os.path.getmtime(path))
        dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
        meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio",
                  "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        return dt.strftime(f"%d/%m/%Y ({dias[dt.weekday()]} {dt.day} de {meses[dt.month-1]}) %H:%M")
    except Exception as e:
        return f"Error: {e}"

def check_recording_apps():
    print(Fore.CYAN + "\n[+] Checking for recording applications...\n")

    recorders = [
        "obs64.exe", "action.exe", "itopvpnrecorder.exe", "nvcplui.exe",  # OBS, Action!, iTop VPN Recorder, NVIDIA Control Panel
        "bandicam.exe", "fraps.exe", "camtasia.exe", "xsplit.exe",         # Bandicam, Fraps, Camtasia, XSplit
        "shadowplay.exe", "dxtory.exe", "playclaw.exe", "gamecapture.exe",  # ShadowPlay, Dxtory, PlayClaw, Game Capture
        "movavi.exe", "screenrecorder.exe"    # Movavi
    ]
    found = [p.info['name'] for p in psutil.process_iter(['name']) if p.info['name'].lower() in recorders]
    if found:
        print(Fore.RED + f"Recording apps running: {', '.join(found)}")
    else:
        print(Fore.GREEN + "No recording apps running.")

def check_recent_usb_devices():
    print(Fore.CYAN + "\n[+] Checking recent USB devices...\n")
    usb_path = r"SYSTEM\\CurrentControlSet\\Enum\\USBSTOR"

    try:
        reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        key = winreg.OpenKey(reg, usb_path)
        for i in range(winreg.QueryInfoKey(key)[0]):
            dev = winreg.EnumKey(key, i)
            print(Fore.GREEN + f"[USB] Device: {dev}")
    except Exception as e:
        print(Fore.RED + f"Registry error: {e}")



def check_active_processes():
    print(Fore.CYAN + "\n[+] Checking active user-level processes...\n")

    system_names = [
        "svchost.exe", "explorer.exe", "csrss.exe", "wininit.exe", "winlogon.exe",
        "services.exe", "lsass.exe", "smss.exe", "System Idle Process", "System",
        "SearchIndexer.exe", "conhost.exe", "RuntimeBroker.exe", "dwm.exe",
        "taskhostw.exe", "sihost.exe", "backgroundTaskHost.exe"
    ]
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        try:
            name, user = proc.info['name'], proc.info['username']
            if name and user and name.lower() not in system_names and 'system' not in user.lower():
                print(Fore.GREEN + f"[PID: {proc.info['pid']}] {name} (User: {user})")
        except:
            continue

# Logitech: AppData\Local\LGHUB | File: settings.db
# Glorious: AppData\Local\BYCOMBO-2 | File: 'Mac' folder
# Razer: ProgramData\Razer\Razer Central\Accounts | File: Emily3
# Corsair: AppData\Corsair\CUE | File: Config.cuecfg
# Asus: Documents\ASUS\ROG\ROG Armoury\common | File: 'Macro' folder
# Motospeed: C:\Program Files (x86)\MotoSpeed Gaming Mouse\V60\modules | File: 'Settings' folder and all .bin files
# Mars Gaming: C:\Program Files (x86)\MARSGAMING\MMGX\modules\macro | File: All files in the folder
# Krom: AppData\Local\VirtualStore\Program Files (x86)\KROM KOLT\Config | File: sequence.dat
def check_macros_software():
    print(Fore.CYAN + "\n[+] Checking macro configuration files...\n")
    paths = [
        ("Logitech", "~\\AppData\\Local\\LGHUB\\settings.db"),
        ("Glorious", "~\\AppData\\Local\\BYCOMBO-2\\Mac"),
        ("Razer", "C:\\ProgramData\\Razer\\Razer Central\\Accounts\\Emily3"),
        ("Corsair", "~\\AppData\\Corsair\\CUE\\Config.cuecfg"),
        ("Asus", "~\\Documents\\ASUS\\ROG\\ROG Armoury\\common\\Macro"),
        ("Motospeed", "C:\\Program Files (x86)\\MotoSpeed Gaming Mouse\\V60\\modules\\Settings"),
        ("Mars Gaming", "C:\\Program Files (x86)\\MARSGAMING\\MMGX\\modules\\macro"),
        ("Krom", "~\\AppData\\Local\\VirtualStore\\Program Files (x86)\\KROM KOLT\\Config\\sequence.dat")
    ]

    found = False
    for brand, raw_path in paths:
        path = os.path.expanduser(raw_path)
        if os.path.exists(path):
            found = True
            if os.path.isfile(path):
                print(Fore.GREEN + f"[{brand}] {path} - Modified: {format_time(os.path.getmtime(path))}")
            else:
                print(Fore.GREEN + f"[{brand}] {path}/")
                for root, _, files in os.walk(path):
                    for file in files:
                        fpath = os.path.join(root, file)
                        print(Fore.GREEN + f"    └─ {file} - Modified: {format_time(os.path.getmtime(fpath))}")
        else:
            print(Fore.YELLOW + f"[{brand}] Path not found: {path}")

    if not found:
        print(Fore.RED + "No macro-related software found.")

def all_categories():
    check_recent_exe_files()
    check_resource_packs()
    check_mods()
    check_recording_apps()
    check_recent_usb_devices()
    check_active_processes()
    print(Fore.GREEN + f"Recycle Bin last modified on: {get_recycle_bin_modification_date()}")

if __name__ == "__main__":
    main()