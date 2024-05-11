import subprocess
import os

server_directory = os.path.join(os.getcwd(), "server")
restart_script_path = os.path.join(server_directory, "bot.py")

subprocess.run(["python", restart_script_path])