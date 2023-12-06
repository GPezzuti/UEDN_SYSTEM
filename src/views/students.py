# views/students.py

from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich.align import Align
from prompt_toolkit import prompt
from src.utils.helpers import clear_console

console = Console()


def students_menu():
    clear_console()

    console.print("Menu de Estudiantes\n", style="bold blue", justify="center")

    student_menu_items = [
        "[1] Search",
        "[2] New Register"
    ]
    student_panels = [Panel(Align.center(item, vertical="middle"), style="bold cyan", padding=(1, 2)) for item in
                      student_menu_items]
    console.print(Align.center(Columns(student_panels)))
    display_student_dashboard()

    choice = prompt("\nSelect an option: ")
    if choice == "1":  # TODO: Add logic
        print("Search")
    elif choice == "2":
        print("New Register")


def display_student_dashboard():
    console.print("\n[Dashboard]", style="bold magenta", justify="center")
