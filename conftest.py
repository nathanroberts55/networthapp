import pytest
import requests
import subprocess
import time
import os
import sys


def server():
    # Setting the Python Path
    venv_path = "venv"
    if os.path.exists(venv_path):
        if sys.platform == "win32":
            python_path = os.path.join(venv_path, "Scripts", "python.exe")
        else:
            python_path = os.path.join(venv_path, "bin", "python")
    else:
        python_path = "python"

    # Start the server as a separate process and redirect its output to a file
    with open("server.log", "w") as f:
        subprocess.Popen([python_path, "main.py"], stdout=f, stderr=subprocess.STDOUT)


@pytest.fixture(autouse=True, scope="session")
def start_server():
    # Start the server before running tests
    server()
    # Wait for the server to start
    time.sleep(5)
    # Check if the server is running
    try:
        response = requests.get("http://localhost:8080")
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        pytest.exit(f"Failed to start server: {e}")
    yield
