import subprocess
import re
from rich.console import Console
from rich.table import Table

console = Console()

def get_windows_saved_passwords():
    """Wyciąga wszystkie zapisane hasła Wi-Fi z systemu Windows."""
    console.print("[*] Uzyskiwanie profili sieciowych...", style="bold cyan")
    
    # Pobieranie listy profili
    meta_data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="ignore")
    data = re.findall("All User Profile\s?:\s?(.*)", meta_data)
    
    table = Table(title="💾 ZAPISANE HASŁA WI-FI (WINDOWS)", title_style="bold green")
    table.add_column("SSID (Nazwa sieci)", style="cyan")
    table.add_column("Hasło", style="yellow")

    for profile in data:
        profile = profile.strip()
        try:
            # Pobieranie hasła dla każdego profilu
            results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear']).decode('utf-8', errors="ignore")
            password_match = re.search("Key Content\s?:\s?(.*)", results)
            
            if password_match:
                password = password_match.group(1).strip()
            else:
                password = "[BRAK HASŁA / OTWARTA]"
                
            table.add_row(profile, password)
        except subprocess.CalledProcessError:
            table.add_row(profile, "[BŁĄD ODCZYTU]")

    console.print(table)

# Integracja z Twoim Menu:
# if choice == "2":
#     get_windows_saved_passwords()