#!/usr/bin/env python3

import os
import platform
import socket
import psutil
import time
from datetime import datetime

PYTHON_ASCII = """
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░▒░▒▒▒░░░░▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░▒▒▒▒░▒░▒▒░░▒░▒▒▒▒░
░▒▒▒▒▒▒▒▒▒░░░░░░░░░░░▒▒▒▒▒▓▓▒▒███▓░░▒░░░░▒▒░░░▒▒░░▒░▒░▒░
░▒▒▒▒▒▒▒▒▒▒▒▒░░░░░▒▓▓█▓▓▓▓▓▓▓▓▒░░▒░▒▒░░░░░▒▒▒▒▒░░░▒░▒▒░░
░▒▒▒▒▒▒▒▒░░░░░░░▓▓▒▓▓▒▒▓▓█▓▒▓▓▒▒▓▓▓▓▓▒░▒░▒▒▒░▒░▒▒░▒░▒▒▒░
░▒▒▒▒▒░░░░▒▒▒░▒▓▓▓▓▓▒▒░░▒▓█▓▒▓▓▓▓▒▒▒░░░░▒▒░░░▒░░░░░░▒░░░
░▒▒▒▒▓▓▓▓███▓▓▓██████▓██▓▓▓▓▓▒▓▓▒▒▒▓██▓▓▒▒░▒▒░░░░░░░░░░░
▒█▓▓▓▓▓██▓▒▓▓▓▓█████████▓▒▒▒▒▒▒█▓▓███▓█▒▒▓▓▒▒░░░▒▒░░░░░░
▒██████▓▒▓▓▓▓▓▓███▓▓▒░▒▒▒▒▒▒▒░░░▒▒▒▒░▒▒▓▓▒▒▓▓▒▒░░░░▒░▒░░
▓████▓▒▒▓█▓▓▓▓▓▓▓▒▓▓██▓▓██▓███▓▓▒▒▒▒░░░▒▒▓▒▒▒▓▓▒░░▒░░░░░
▓████▓▓██▓▓▓▓▓▓▓▓▓███████████▓█▓▒▓███▓▓▓▒▒▒▒▒▒▒▓▒▒▒▒▒▒▒░
▓███▓▓███▓▓▓▓▓▓▓████▓██████████▓▒▒▒▒▓▓▓▓▓▒▓▓▒▒▒▒▒▒▒▒▒▒▒░
▓███████▓▓▓▓▓▓███▓▓▓██▓▓▓▓▓███▒▒▒▓▓▒▒▓▓█▓▒▒▓▓▒▒▒▒▒▒▒▒▒▒░
▓██████▓▓▓▓▓██▓▓▓▓▓█████████▓▒▓██████▓▒▒▓▒▓▒▓▓▓▒▒▒▒▒▒▒▒░
███████▓▓▓███████████▓▓▒▒▒▒▒▓▓▓▓▓█████▓▒▓▒▒▒▒▓▓▒▒▒▓▓▓▓▓░
███████▓▓▓██▓███████▓█▓▓▒▒▒▒▒▒▒▒▒▒▓████▓▓▒▓▒▒▒▒▒▒▒▓▓▓▓▓▒
███████▓▓▓▓▓▓██████▓█▓▓▓▓▓▓▓▓▒▓▓▓▒▓▓▓██▓▓▒▓▒▒▓▓▓▓▒▓▓▓▓▓░
██████▓▓▓▓▓▓▒▓████████▓▓▓▓▓▓▓▓▓▓███████▓▒▓▓▒▒▓█▓▓▒▓▒▓███
███████▓▒▒▓▓▒▒█▓▓██▓████▓█▓▓▓█▓▓███▓██▓▓▓▓▒▒▒▓▒▒▒▓▓▓▓░░░
▓███████▓▓▓▓▓▒▓▓▒▓████▓██▓▓▓▓▓▓▓██▓██▓▓▓▓░░▒▒▒▒▒▓▓▓▓██▒░
▓███████▓██▓▓▓▓▓▓▒▓███▒▓██▓▓▓▓█▓█▓▓█▓▓▒░▒░▒▓▓▓▓▓▓▓▓▓██▒░
▓███████████████▓▓▒▒▓█▓▒█▓▓▓▓▓█▓▒░░░░░░▒███▓▓▓▓▓▓▓▓▓▓█▒▒
▒▓▓▓███████████▓▓▓▓▓░░▓▒▒▓▓▓▓▓▒░▒▓▓███▓░██▒▓▓▓▓▓▓▓▒▒▒▓▒░
▒▓▓▓▓▓▓▓▓▓▓▓▓██▓▓█▓███▓▓▒▒▒▒▒▓██████░░░░▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒
▒▓▓▓▓▓▓▓▓▓▓▓▓███▓▒▒▓▓▓▓▓█▓░▓██▓▒▒░░░░░░░░▓▓▓▓▓▓▓▓▓▓▓▒▓▓░
░▒▒▒▒▒▒▒▒▒▓▓▒▓▓▓▓░░░░░░▓████▓▓▓▓█▒▓▒▒▒░░░▒▓▓▓▓▓▓▓▓▓▓▓▒▓░
▓███▓▓▓▓▒▒▒▒▒▒▓▓▓▓▓▓▓████▓██▓██▓▒▒█▓░▒▒░▒▒▓▓▒▓▓▓▓▓▓▓▓▓▓░
▒████████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▓▓░░▒▓▓▒▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒░
░▓▓█▓███████████████▓▓▓▓▓▓▓▓▓▓▓▓▓█████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒░
░░░░░░░░░░░░░░░░░░▒▒▒▒▓▒▓▓▓▓▓▒▒▒▒▒▒▒▒░░░░░░░░░░░░░░░░░░░
   Python {version}
""".strip().split('\n')

def get_os_info():
    return f"{platform.system()} {platform.release()}"

def get_hostname():
    return socket.gethostname()

def get_kernel():
    uname = platform.uname()
    if platform.system() == 'Windows':
        return f"Windows {uname.release} {uname.machine}"
    else:
        return f"{uname.system} {uname.release} {uname.machine}"

def get_uptime():
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    now = datetime.now()
    uptime = now - boot_time
    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{days}d {hours}h {minutes}m"

def get_cpu_info():
    cpu_count = psutil.cpu_count(logical=False)
    cpu_percent = psutil.cpu_percent(interval=1)
    return f"{cpu_count} cores @ {cpu_percent:.1f}%"

def get_memory_info():
    memory = psutil.virtual_memory()
    total_gb = memory.total / (1024**3)
    used_gb = memory.used / (1024**3)
    return f"{used_gb:.1f}G / {total_gb:.1f}G ({memory.percent:.1f}%)"

def get_shell():
    return os.environ.get('SHELL', 'Unknown').split('/')[-1]

def display_info():
    py_version = platform.python_version()
    info_lines = [
        ("OS", get_os_info()),
        ("Host", get_hostname()),
        ("Kernel", get_kernel()),
        ("Uptime", get_uptime()),
        ("CPU", get_cpu_info()),
        ("Memory", get_memory_info()),
        ("Shell", get_shell()),
    ]
    
    max_ascii_len = max(len(line) for line in PYTHON_ASCII)
    info_width = max(len(f"{label}: {value}") for label, value in info_lines)
    
    ascii_lines = PYTHON_ASCII[:-1] + [PYTHON_ASCII[-1].format(version=py_version)]
    max_lines = max(len(ascii_lines), len(info_lines))
    
    ascii_lines += [""] * (max_lines - len(ascii_lines))
    info_lines += [("", "")] * (max_lines - len(info_lines))
    
    for ascii_line, (label, value) in zip(ascii_lines, info_lines):
        if label:
            info_text = f"{label}: {value}"
            padding = " " * (max_ascii_len - len(ascii_line) + 2)
            print(f"{ascii_line}{padding}{info_text}")
        else:
            print(ascii_line)

if __name__ == "__main__":
    display_info()
    input("Press Enter to exit...")
