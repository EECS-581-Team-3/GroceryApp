Python 3.11.9 required

Quick Windows setup:
- Create venv py -3.11 -m venv venv
- Activate venv (PowerShell) .\venv\Scripts\activate.ps1 If PowerShell blocks scripts, run: Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass then repeat the activate command.
- Upgrade pip python.exe -m pip install --upgrade pip
- Install dependencies pip install -r requirements.txt
- Run the app (adjust entrypoint if needed) python -m src.main or python user_interface.py

Quick macOS / Linux setup:
- Create venv python3 -m venv .venv (or: pyenv/asdf install 3.11.9 && pyenv local 3.11.9)
- Activate venv macOS / Linux: source .venv/bin/activate
- Upgrade pip python -m pip install --upgrade pip
- Install dependencies pip install -r requirements.txt
- Run the app (adjust entrypoint if needed) python -m src.main or python user_interface.py
