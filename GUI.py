import time
from rich.live import Live
from rich.panel import Panel
from rich.layout import Layout

def run_app():
    console.clear()
    layout = Layout()
    
    # Tworzymy prosty Dashboard
    layout.split_column(
        Layout(name="header", size=5),
        Layout(name="body")
    )
    
    header_content = Panel("WiFi CRACKER v1.0 - ULTIMATE EDITION", style="bold white on red")
    layout["header"].update(header_content)
    
    console.print(layout)
    
    # Tutaj logika wyboru modułów...
    console.print("\n[1] RECON  [2] DUMPER  [3] CAPTURE  [4] CRACK  [5] EXIT")
    choice = console.input("\n[bold yellow]Wybierz opcję: [/bold yellow]")
    
    if choice == "2":
        get_windows_saved_passwords()
        input("\nNaciśnij Enter, aby wrócić...")
        run_app() # Powrót do menu