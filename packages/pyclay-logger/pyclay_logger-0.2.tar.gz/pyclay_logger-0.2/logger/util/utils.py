import os, subprocess, inspect

def get_script_dir() -> str:
    caller_script_path = os.path.abspath((inspect.stack()[1])[1])
    caller_script_dir = os.path.dirname(caller_script_path)
    return caller_script_dir

def link_exists(url: str):
    return os.path.islink(url)

def delete_file(url: str):
    os.unlink(url)

def create_softlink(src_path: str, dst_path: str):
    if link_exists(dst_path):
        delete_file(dst_path)
    subprocess.run(f"ln -s {src_path} {dst_path}", shell=True)

def rel_to_abs_path(rel_path: str) -> str:
    return os.path.abspath(rel_path)