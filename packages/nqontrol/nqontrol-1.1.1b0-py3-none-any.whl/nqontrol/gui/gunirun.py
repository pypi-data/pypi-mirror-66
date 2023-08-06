import logging as log
import os
import subprocess
from platform import system

from nqontrol.gui import run


def main():
    script_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(script_path)
    if "Linux" in system():
        subprocess.run(["gunicorn", "-c", "guniconfig.py", "run:server"], check=True)
    else:
        log.warning(
            f"gunicorn might not run on this machine! Trying normal flask server."
        )
        run.main()


if __name__ == "__main__":
    main()
