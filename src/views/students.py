import time
from rich.panel import Panel
from rich.columns import Columns
from rich.align import Align
from prompt_toolkit import prompt
from src.utils.helpers import *
from src.config import *
from rich.console import Console
from rich.table import Table
import pandas as pd
import sqlite3

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
        display_student_dashboard()

        choice = prompt("\nElige una opción: ")
        if choice == "1":  # TODO: Add logic
            paginate_dataframe()
        elif choice == "2":
            print("Nuevo Ingreso")
        elif choice == "3":
            break
        else:
            console.print("Opción Incorrecta\n", style="bold red", justify="center")
            time.sleep(1)


def display_student_dashboard():
    console.print("\n[Dashboard]", style="bold magenta", justify="center")
