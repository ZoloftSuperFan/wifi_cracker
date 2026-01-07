import os
import sys
from rich.console import Console
from rich.panel import Panel

console = Console()

def setup_monitor_mode(interface):
    console.print(f"[*] Przygotowanie {interface}...", style="yellow")
    # Zabicie procesów blokujących
    os.system("sudo airmon-ng check kill")
    # Start trybu monitor
    os.system(f"sudo airmon-ng start {interface}")
    return f"{interface}mon"

def main():
    os.system("clear")
    console.print(Panel.fit("WiFi CRACKER v1.0 - ULTIMATE EDITION", style="bold red"))
    
    console.print("[1] 🔍 RECON MODULE (Skanuj otoczenie)")
    console.print("[2] 🤝 HANDSHAKE CAPTURE (Deauth Attack)")
    console.print("[3] 🔓 CRACKING ENGINE (Dictionary Attack)")
    console.print("[4] ❌ EXIT")

    choice = input("\n[#] Wybór: ")

    if choice == "1":
        # Tutaj wywołujemy Twój kod z modułu RECON
        # Pamiętaj, aby przekazać interfejs (np. wlan0mon)
        os.system("sudo python3 recon.py wlan0") # recon.py to kod który daliśmy wcześniej
    
    elif choice == "2":
        bssid = input("[?] Podaj BSSID celu: ")
        channel = input("[?] Podaj kanał: ")
        # Tutaj wywołujemy capture.py
        os.system(f"sudo python3 capture.py wlan0mon {bssid} {channel}")

if __name__ == "__main__":
    main()