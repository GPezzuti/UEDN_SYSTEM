import time
from rich.panel import Panel
from rich.columns import Columns
from rich.align import Align
from prompt_toolkit import prompt
from src.utils.helpers import clear_console, get_students_data, sort_students_by_last_name
from rich.console import Console
from rich.table import Table
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
            students_table()
        elif choice == "2":
            print("Nuevo Ingreso")
        elif choice == "3":
            break
        else:
            console.print("Opción Incorrecta\n", style="bold red", justify="center")
            time.sleep(1)


def display_student_dashboard():
    console.print("\n[Dashboard]", style="bold magenta", justify="center")


def students_table():
    conn = sqlite3.connect('../src/database/school_management_system.db')
    students_data = get_students_data(conn)
    sorted_students = sort_students_by_last_name(students_data)

    table = Table(title="Students List")

    table.add_column("ID", justify="right")
    table.add_column("First Name")
    table.add_column("Last Name")
    table.add_column("Date of Birth")

    for student in sorted_students:
        table.add_row(
            str(student[0]),  # student_id
            student[1],       # first_name
            student[2],       # last_name
            student[3]        # date_of_birth
        )

    console.print(table, style="bold blue", justify="center")
    input("Enter para volver...")
