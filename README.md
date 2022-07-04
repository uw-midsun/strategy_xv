# Strategy XV

Midnight Sun's strategy repository for the MSXV iteration and cycle.

## Setup

### Python install
Install Python 3 on your system. To test, open a command prompt or a terminal and write `python3` or `py`.

If uninstalled, try downloading Python from [here](https://www.python.org/downloads/), which will give you a simple install.

Note that your system (MacOS, Windows, or even Linux) may have multiple ways of installing and managing Python. It's up to you if you'd like to try any of these, but in our case a simple install is good enough. If you are on Windows, setting up Windows Subsystem for Linux (WSL) is often recommended, however the simple install above works fine as well.

### Poetry install
To manage dependencies, this repository uses the Poetry package manager. Poetry also automatically manages Python virtual-environments -- this means all the packages that you will install for strategy will be isolated from other Python projects you may work on.

Command to install on MacOS (see another option below) or through Windows Subsystem for Linux (WSL) or just plain Linux:
```shell
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

Or if you are on Windows and do not have WSL set up, run the following command on PowerShell:
```PowerShell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -
```

### Project setup
Once the above is all completed, clone this repository using git. If you do not have Git installed, download it [here](https://git-scm.com/).

If you've never used git before, don't worry! It's not all that scary... mostly...

Here's a [nice tutorial](https://githowto.com/) to go through. 

Cloning the repository will give a new folder named `strategy_xv`, same as the name you see on the repository above.

Once cloned, run `cd strategy_xv` to go into the new folder. 

Then, to install the project dependencies, run `poetry install` -- this will install all the libraries listed in the `pyproject.toml` and `poetry.lock` files. Poetry will install all dependencies into a virtual environment that isolates the project from any other Python projects you may have (or will have).

To 'activate' the new virtual environment -- which you would want to do if you are running your code in your terminal -- run `poetry shell`. You must be in the `strategy_xv` folder to be able to activate it.

If you run code from your code editor (e.g. VS Code, PyCharm, etc), there should be some documentation on how to connect the editor to the Poetry virtual environment to run your code.
