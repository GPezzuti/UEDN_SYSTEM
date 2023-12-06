import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from src.views.students import students_menu, display_student_dashboard
from src.utils.helpers import clear_console
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.columns import Columns
from rich.align import Align
from prompt_toolkit import prompt

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
    display_welcome()

    menu_items = [
        "[1] Estudiantes",
        "[2] Facturación",
        "[3] Reportes",
        "[4] Notificaciones"
    ]

    # Create Panels that wrap closely around the text
    panels = [Panel(Align.center(item, vertical="middle"), style="bold cyan", padding=(1, 2)) for item in menu_items]

    # Align the panels in a horizontal layout
    console.print(Align.center(Columns(panels)))

    choice = prompt("\nElige una opción: ")
    if choice == "1":
        students_menu()
    # ... handle other choices ...


if __name__ == "__main__":
    clear_console()
    main_menu()
