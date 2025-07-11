import subprocess

def install_library_shell(library_name):
    try:
        result = subprocess.run(
            ["bash", "./pypop.sh", library_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return result.stderr.strip()
    except Exception as e:
        return f"Error: {str(e)}"

