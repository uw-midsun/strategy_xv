# Strategy XV

Midnight Sun's strategy repository for the MSXV iteration and cycle.

## Setup

### Python install

Install Python 3 on your system. To test, open a command prompt or a terminal and write `python3` or `py`.

If uninstalled, try downloading Python from [here](https://www.python.org/downloads/), which will give you a simple install.

Note that your system (MacOS, Windows, or even Linux) may have multiple ways of installing and managing Python. It's up to you if you'd like to try any of these, but in our case a simple install is good enough. If you are on Windows, setting up Windows Subsystem for Linux (WSL) is often recommended, however the simple install above works fine as well.

### Pip install

To manage dependencies, this repository uses the pip package manager. pip can also manage Python virtual-environments -- this means all the packages that you will install for strategy will be isolated from other Python projects you may work on.

Command to install on MacOS (see another option below) or through Windows Subsystem for Linux (WSL) or just plain Linux:

```shell
python3 get-pip.py
```

Here's a good tutorial to learn how to manage packages using python and pip [here](https://packaging.python.org/en/latest/tutorials/installing-packages/)

### Project setup

Once the above is all completed, clone this repository using git. If you do not have Git installed, download it [here](https://git-scm.com/).

If you've never used git before, don't worry! It's not all that scary... mostly... here's a [nice tutorial](https://githowto.com/) you can refer to.

Cloning the repository will create a new folder named `strategy_xv` with all the code -- you will have 'cloned' the repository!

Once cloned, run `cd strategy_xv` to go into the new folder.

First, set up a virtual environment using `python3 -m vevn`. This will create a `venv/` folder in your directory and isolate all of the porpject dependencies from other projects.

To source this environment run `source venv/bin/activate`.

Then, to install the project dependencies, run `pip install -r requirements.txt` -- this will install all the libraries listed in the `requirements.txt` file.

If you run code from your code editor (e.g. VS Code, PyCharm, etc), there should be some documentation from the relevant sources on how to connect the editor to the pip virtual environment to run your code.

### Contributing

Please add the ticket number to your commit and include some sort of tests based on `pytest` in the `tests` folder of the related project. If the folder is not created, please create it and then add the tests. Check that those pass by running `pytest`.

Please put the issue key in the commits and branches for pull request to connect the pull request to the related ticket on JIRA.
