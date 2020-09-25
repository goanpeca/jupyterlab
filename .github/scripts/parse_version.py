# Standard library imports
import sys
import jupyterlab


def get_version():
    sys.stdout.write(f'{jupyterlab.__version__}')


if __name__ == "__main__":
    get_version()
