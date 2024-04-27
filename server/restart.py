import subprocess
import os

server_directory = os.path.join(os.getcwd(), "server")
subprocess.run(["python", "restart_bot.py"])