from prompt_toolkit import prompt
from rich.align import Align
from rich.columns import Columns
from rich.panel import Panel

from src.utils.helpers import *

console = Console()


def students_menu():
    while True:
        clear_console()
        console.print("Menú de Estudiantes\n", style="bold blue", justify="center")

        student_menu_items = [
            "[1] Buscar",
            "[2] Nuevo Ingreso",
            "[3] Volver"
        ]

        student_panels = [Panel(Align.center(item, vertical="middle"), style="bold cyan", padding=(1, 2))
                          for item in student_menu_items]

        console.print(Align.center(Columns(student_panels)))

        choice = prompt("\nElige una opción: ")
        if choice == "1":
            console.clear()
            console.print("test\n", style="green")
            paginate_dataframe("Estudiantes", 10, 10)
        elif choice == "2":
            print("Nuevo Ingreso")
        elif choice == "3":
            break
        else:
            console.print("Opción Incorrecta\n", style="bold red", justify="center")
            time.sleep(1)
