import datetime
from prompt_toolkit import prompt
from rich.align import Align
from rich.columns import Columns
from rich.panel import Panel
from src.config import STUDENTS_COLUMNS, DESKTOP_PATH
from src.controllers.students_controller import get_students_data, add_new_student
from src.utils.helpers import *

console = Console()


def students_menu():
    while True:
        clear_console()
        console.print("Menú de Estudiantes\n", style="bold blue", justify="center")

        student_menu_items = [
            "[1] Buscar",
            "[2] Nuevo Ingreso",
            "[3] Exportar Estudiantes",
            "[4] Volver"
        ]

        student_panels = [Panel(Align.center(item, vertical="middle"), style="bold cyan", padding=(1, 2))
                          for item in student_menu_items]

        console.print(Align.center(Columns(student_panels)))

        choice = prompt("\nElige una opción: ")
        if choice == "1":
            console.clear()
            df = get_students_data()
            paginate_dataframe(df, "Estudiantes", STUDENTS_COLUMNS, 10, 10)

        elif choice == "2":
            add_new_student()
            console.print("Registro Exitoso\n", style="bold green", justify="center")
            time.sleep(1)

        elif choice == "3":
            user_input = str(input("¿Desea exportar todos los estudiantes a Excel? (S/N): ").strip().lower())

            if user_input == 's':
                df = get_students_data()

                # Define the filename with a timestamp
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{DESKTOP_PATH}/estudiantes_{timestamp}.csv"
                # Save the DataFrame to a CSV file
                df.to_csv(filename, index=False)
                print(f"Archivo salvado en el escritorio: {filename}")
                time.sleep(2)
            else:
                continue

        elif choice == "4":
            break

        else:
            console.print("Opción Incorrecta\n", style="bold red", justify="center")
            time.sleep(1)
