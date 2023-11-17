import subprocess

def get_tree_output():
    result = subprocess.run(['tree'], capture_output=True, text=True)
    return result.stdout
