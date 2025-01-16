import os
import sys
import shutil
import psutil
import subprocess
import glob
import time
import pip
from typing import Optional

import platform
import os

def run_command(command: str) -> str:
    """Execute a shell command and return the output."""
    try:
        # Use shell=True for Windows to properly handle commands
        use_shell = platform.system() == "Windows"
        
        # Run the command and capture output
        result = subprocess.run(
            command,
            shell=use_shell,
            text=True,
            capture_output=True,
            check=True
        )
        
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        print(f"Error output: {e.stderr}")
        return e.stderr
    except Exception as e:
        print(f"Error executing command: {str(e)}")
        return str(e)

def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def remove_dir(path):
    if os.path.exists(path):
        shutil

def remove_file(path):
    if os.path.exists(path):
        os.remove(path)

def copy_file(src, dst):
    shutil.copyfile(src, dst)

def move_file(src, dst):
    shutil.move(src, dst)

def get_files(path):
    return os.listdir(path)

# create a file (write a new file)
def create_file(path, content):
    with open(path, "w") as f:
        f.write(content)

# read a file
def read_file(path):
    with open(path, "r") as f:
        return f.read()
    
# append to a file
def append_file(path, content):
    with open(path, "a") as f:
        f.write(content)

def get_env_var(key):
    """Get the value of an environment variable."""
    return os.getenv(key)

def set_env_var(key, value):
    """Set an environment variable."""
    os.environ[key] = value

def list_processes():
    """List all running processes."""
    return [proc.info for proc in psutil.process_iter(['pid', 'name'])]

def kill_process(pid):
    """Kill a process by its PID."""
    process = psutil.Process(pid)
    process.terminate()

def find_files(pattern):
    """Find files matching a pattern."""
    return glob.glob(pattern)

def get_file_info(path):
    """Get information about a file."""
    if os.path.exists(path):
        stat = os.stat(path)
        return {
            'size': stat.st_size,
            'last_modified': time.ctime(stat.st_mtime),
            'is_directory': os.path.isdir(path)
        }
    return None

def install_package(package):
    """Install a Python package using pip."""
    pip.main(['install', package])

def uninstall_package(package):
    """Uninstall a Python package using pip."""
    pip.main(['uninstall', package])

def execute_python_code(code):
    """Execute Python code dynamically."""
    exec(code)

def rename_files(directory, pattern, new_name):
    """Rename files in a directory based on a pattern."""
    for filename in os.listdir(directory):
        if pattern in filename:
            new_filename = filename.replace(pattern, new_name)
            os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))


output = run_command("dir")
print(output)
