import socket
import sys
import subprocess

if __name__ == '__main__':
    ip = socket.gethostbyname(socket.gethostname())
    port = 8000
    is_human = "ai"
    python_path = sys.executable

    p = subprocess.Popen("%s four_in_a_row.py %s %s" % (python_path, "human", port))
    p2 = subprocess.Popen("%s four_in_a_row.py %s %s %s" % (python_path, is_human, port, ip))

