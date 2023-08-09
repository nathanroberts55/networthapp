import pytest
import requests
import subprocess
import time


def server():
    # Start the server as a separate process and redirect its output to a file
    with open("server.log", "w") as f:
        subprocess.Popen(["python", "main.py"], stdout=f, stderr=subprocess.STDOUT)


@pytest.fixture(autouse=True, scope="session")
def start_server():
    # Start the server before running tests
    server()
    # Wait for the server to start
    time.sleep(5)
    # Check if the server is running
    try:
        response = requests.get("http://localhost:8000")
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        pytest.exit(f"Failed to start server: {e}")
    yield
