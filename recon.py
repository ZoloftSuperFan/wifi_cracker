import sys
from scapy.all import *
from rich.console import Console
from rich.table import Table
from rich.live import Live
import threading
import os

console = Console()
networks = {} # Słownik do przechowywania unikalnych sieci

def packet_handler(pkt):
    if pkt.haslayer(Dot11Beacon):
        # Wyciąganie podstawowych informacji z ramki Beacon
        bssid = pkt[Dot11].addr2
        ssid = pkt[Dot11Elt].info.decode() if pkt[Dot11Elt].info else "Ukryte"
        
        # Obliczanie mocy sygnału (dBm)
        stats = pkt[Dot11Beacon].network_stats()
        channel = stats.get("channel")
        crypto = "/".join(stats.get("crypto"))
        signal = pkt.dBm_AntSignal if hasattr(pkt, 'dBm_AntSignal') else "N/A"

        networks[bssid] = [ssid, channel, str(signal), crypto]

def generate_table():
    """Tworzy dynamiczną tabelę w terminalu."""
    table = Table(title="🔍 WiFi RECON - Skoncentrowane Cele", title_style="bold magenta")
    table.add_column("SSID", style="cyan")
    table.add_column("BSSID (MAC)", style="green")
    table.add_column("Kanał", justify="center")
    table.add_column("Sygnał (dBm)", justify="center")
    table.add_column("Zabezpieczenia", style="yellow")

    for bssid, info in networks.items():
        table.add_row(info[0], bssid, str(info[1]), str(info[2]), info[3])
    return table

def channel_hopper(interface):
    """Zmienia kanały karty sieciowej, aby widzieć wszystkie sieci."""
    ch = 1
    while True:
        os.system(f"iwconfig {interface} channel {ch}")
        ch = ch % 14 + 1 # Przełączaj kanały 1-14
        time.sleep(0.5)

def main():
    if len(sys.argv) < 2:
        console.print("[red][!] Użycie: sudo python recon.py <interfejs>[/red]")
        sys.exit(1)

    interface = sys.argv[1]

    # 1. Aktywacja karty (Wymaga Twojego TP-Linka w trybie monitor)
    console.print(f"[*] Aktywacja [bold blue]{interface}[/bold blue] w trybie monitor...")
    os.system(f"ip link set {interface} down")
    os.system(f"iw {interface} set monitor none")
    os.system(f"ip link set {interface} up")

    # 2. Uruchomienie skakania po kanałach w tle
    hop_thread = threading.Thread(target=channel_hopper, args=(interface,), daemon=True)
    hop_thread.start()

    # 3. Wyświetlanie tabeli w czasie rzeczywistym
    with Live(generate_table(), refresh_per_second=4) as live:
        console.print(f"[*] Rozpoczęto skanowanie na {interface}. Naciśnij Ctrl+C, aby zatrzymać.")
        sniff(iface=interface, prn=packet_handler, store=0)

if __name__ == "__main__":
    main()