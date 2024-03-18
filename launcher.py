import subprocess
import os

script_path = os.path.join(os.path.dirname(__file__), "Rocket widget.py")
subprocess.Popen(["start", "pythonw", script_path], shell=True)