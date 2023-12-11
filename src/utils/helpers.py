import os
import platform
import time
from rich.console import Console
from rich.table import Table
from pathlib import Path

console = Console()


def get_desktop_path():
    # Get the home directory
    home = Path.home()

    # Append the Desktop folder depending on the OS
    if os.name == 'nt':  # Windows
        desktop = home / 'Desktop'
    elif os.name == 'posix':  # macOS and Linux
        # On macOS, it's also in the home directory
        # On Linux, this might vary, but usually it's in the home directory
        desktop = home / 'Desktop'
    else:
        raise OSError('Unsupported operating system.')

    return desktop


def clear_console():
    # For Windows
    if platform.system() == "Windows":
        os.system('cls')
    # For macOS and Linux
    else:
        os.system('clear')


def paginate_dataframe(df, title, selected_columns, max_width=10, page_size=10):

    df_sliced = df[selected_columns].copy()

    total_pages = (len(df_sliced) + page_size - 1) // page_size
    current_page = 0

    while True:
        console.clear()
        table = Table(title=f"{title} - Página {current_page + 1} de {total_pages}",
                      show_header=True, header_style="bold magenta")

        # Define the columns of the table
        for col in selected_columns:
            table.add_column(col)

        # Display rows for the current page
        start_index = current_page * page_size
        end_index = start_index + page_size

        for row in df_sliced.iloc[start_index:end_index].itertuples():
            table.add_row(*[str(getattr(row, col))[:max_width] for col in selected_columns])

        console.print(table, style="bold blue", justify="center")

        # Pagination controls
        user_input = input("'f' filtros, 's' siguiente, 'a' atrás, 'q' salir, 'r' resetear: ").strip().lower()

        if user_input == 'f':
            df_sliced = filter_dataframe(df_sliced)
            total_pages = (len(df_sliced) + page_size - 1) // page_size
            current_page = 0
        elif user_input == 's' and current_page < total_pages - 1:
            current_page += 1
        elif user_input == 'a' and current_page > 0:
            current_page -= 1
        elif user_input == 'q':
            console.clear()
            break
        elif user_input == 'r':
            df_sliced = df[selected_columns].copy()  # Reset DataFrame to the original data
            total_pages = (len(df_sliced) + page_size - 1) // page_size
            current_page = 0  # Reset to the first page
        elif user_input not in ['f', 's', 'a', 'q']:
            console.print("Opción Incorrecta\n", style="bold red", justify="center")
            time.sleep(1)


def filter_dataframe(df):
    console.print("\nOpciones de Filtro", style="bold magenta")

    # Display column names
    for i, col in enumerate(df.columns):
        console.print(f"[{i}] {col}", style="bold cyan")

    while True:
        col_input = input("\nSelecciona el índice de la columna para filtrar o 'q' para salir: ")

        if col_input.strip().lower() == 'q':
            return df  # Return the original DataFrame if the user chooses to go back

        try:
            col_index = int(col_input)
            if col_index not in range(len(df.columns)):
                raise ValueError
            filter_col = df.columns[col_index]
            break
        except ValueError:
            console.print("\nÍndice inválido. Por favor, intenta de nuevo.", style="bold red")

    filter_value = input(f"\nIngresa el valor para filtrar en '{filter_col}' o 'q' para salir: ").strip().lower()

    if filter_value == 'q':
        return df  # Return the original DataFrame if the user chooses to go back

    # Apply filter with case-insensitive partial match
    filtered_df = df[df[filter_col].astype(str).str.lower().str.startswith(filter_value)]
    return filtered_df


def remove_duplicated_columns(df):
    seen = set()
    return df.loc[:, ~df.columns.duplicated()]

