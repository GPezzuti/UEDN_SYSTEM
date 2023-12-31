import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from src.views.main import main_menu
from src.controllers.login_controller import login

if __name__ == "__main__":
    logged_in_user = login()
    main_menu()
