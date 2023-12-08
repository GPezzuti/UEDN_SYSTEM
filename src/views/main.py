from prompt_toolkit import prompt
from rich.console import Console
from rich.align import Align
from rich.columns import Columns
from rich.panel import Panel
from src.views.students import students_menu
from src.utils.helpers import clear_console
import time

console = Console()


def display_welcome():
    ascii_logo = """
                       ██          ██                                  ██ ═════════
██╗   ██╗   ███████╗    ██████╗ ██╗██╗   ██╗██╗███╗   ██╗ ██████╗     ███╗   ██╗██╗███╗   ██╗ ██████╗ 
██║   ██║   ██╔════╝    ██╔══██╗██║██║   ██║██║████╗  ██║██╔═══██╗    ████╗  ██║██║████╗  ██║██╔═══██╗
██║   ██║   █████╗      ██║  ██║██║██║   ██║██║██╔██╗ ██║██║   ██║    ██╔██╗ ██║██║██╔██╗ ██║██║   ██║
██║   ██║   ██╔══╝      ██║  ██║██║╚██╗ ██╔╝██║██║╚██╗██║██║   ██║    ██║╚██╗██║██║██║╚██╗██║██║   ██║
╚██████╔╝██╗███████╗    ██████╔╝██║ ╚████╔╝ ██║██║ ╚████║╚██████╔╝    ██║ ╚████║██║██║ ╚████║╚██████╔╝
 ╚═════╝ ╚═╝╚══════╝    ╚═════╝ ╚═╝  ╚═══╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝     ╚═╝  ╚═══╝╚═╝╚═╝  ╚═══╝ ╚═════╝ 

"""

    centered_logo = Align.center(ascii_logo)
    console.print(Panel(centered_logo, style="bold green"), justify="center")
    console.print("Bienvenido al Sistema de Facturación Escolar\n", style="bold yellow", justify="center")


def main_menu():
    while True:
        clear_console()
        display_welcome()

        menu_items = [
            "[1] Estudiantes",
            "[2] Facturación",
            "[3] Reportes",
            "[4] Notificaciones",
            "[5] Salir"
        ]

        # Create Panels that wrap closely around the text
        panels = [Panel(Align.center(item, vertical="middle"), style="bold cyan", padding=(1, 2)) for item in menu_items]

        # Align the panels in a horizontal layout
        console.print(Align.center(Columns(panels)))

        choice = prompt("\nElige una opción: ")
        if choice == "1":
            students_menu()
        elif choice == "2":
            pass
        elif choice == "3":
            pass
        elif choice == "4":
            pass
        elif choice == "5":
            clear_console()
            console.print("OK")
            break
        else:
            console.print("Opción Incorrecta\n", style="bold red", justify="center")
            time.sleep(1)
        # ... handle other choices ...
