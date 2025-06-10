from importlib.resources import path

# Common utilities.

from datetime import datetime, timezone
import json, os, pathlib, psutil, re, shutil, sys

def today() -> str:
    "Return the current YYYY-MM-DD"
    return datetime.today().strftime("%Y-%m-%d")

def make_directories(path: str, delete_first: bool=False, verbose: bool=False):
    """
    Make a directory path, including parents as required.
    Args:
    path (str) The directory path
    deleteFirst
    """
    new_dir_path = pathlib.Path(path)
    if delete_first and new_dir_path.exists():
        shutil.rmtree(path)

    try:
        new_dir_path.mkdir(parents=True)
        if verbose > 0:
            print(f"Directory '{new_dir_path}' created successfully.")
    except FileExistsError:
        if verbose > 1:
            print(f"Directory '{new_dir_path}' already exists.")
    except OSError as e:
        print(f"Error creating directory: {e}")
        sys.exit(1)

def load_json(filename: str):
    with open(filename) as f_in:
        return json.load(f_in)

def error(message: str, file=sys.stdout):
    print(f"ERROR! {message}", file=file)
    sys.exit(1)

def warning(message: str, file=sys.stdout):
    print(f"WARN:  {message}", file=file)

def info(message: str, file=sys.stdout):
    print(f"INFO:  {message}", file=file)

def beep():
    print("\a")  # "beep"
    
def is_process_running(process_name: str) -> bool:
    """
    Checks if there is a running process that contains the given name.
    Args:
      process_name (str) name of the process
    
    Return:
      True or False if a process containing `process_name` is found.
    
    Adapted from https://btechgeeks.com/python-check-if-a-process-is-running-by-name-and-find-its-process-id-pid/
    """

    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if process_name.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;

def make_var_name(str: str) -> str:
    """
    Make a valid variable name out of the string by converting any
    runs of `-\\s,./|'` to `_`.
    """
    return re.sub("""[-\\s,./|'"()]+""", '_', str)

def list_to_str(strs: list[str] | None, delim: str=' ') -> str:
    """
    Return a `delim`-delimited string from the input `strs` array or
    return '' if the array is empty or `None`.
    """
    if alt_keywords and len(alt_keywords):
        return delim.join([k['keyword'] for k in alt_keywords])
    else:
        return ''

def make_md_link(dict, mid_path, css_class="", use_hash=False):
    hash=''
    if use_hash:
        hash='#'
    css_class_str = ''
    if len(css_class) > 0:
        css_class_str=f'{{:class="{css_class}"}}'
    cleaned_keyword = make_var_name(dict["keyword"])
    return f'[{make_title(dict)}]({{{{site.baseurl}}}}/{mid_path}/{hash}{cleaned_keyword}){css_class_str}'
