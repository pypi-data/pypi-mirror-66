# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rush_cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'click_help_colors>=0.6,<0.7',
 'colorama>=0.4.3,<0.5.0',
 'pygments>=2.5.2,<3.0.0',
 'pyyaml>=5.2,<6.0']

entry_points = \
{'console_scripts': ['rush = rush_cli.cli:entrypoint']}

setup_kwargs = {
    'name': 'rush-cli',
    'version': '0.6.1',
    'description': '♆ Rush: A Minimalistic Bash Utility',
    'long_description': '<div align="center">\n\n# Rush 🏃\n**♆ Rush: A Minimalistic Bash Utility**\n\n\n![img](./img/rush-run.png)\n\n**Run all your task automation **Bash commands** from a single `rushfile.yml` file.**\n</div>\n\n\n## Features\n* Supports all **bash** commands\n* Option to ignore or run specific tasks\n* By default, runs commands in **interactive** mode\n* Option to catch or ignore **command errors**\n* Option to show or supress **command outputs**\n* **Command chaining is supported** (See the example `rushfile.yml` where `task_2` is chained to `task_1`)\n\n## Installation\n\n```\n$ pip3 install rush-cli\n```\n\n## Workflow\n\n### Rushfile\nHere is an example `rushfile.yml`. It needs to reside in the root directory:\n\n``` yml\n# rushfile.yml\n\ntask_1: |\n    echo "task1 is running"\n\ntask_2: |\n    # Task chaining [task_1 is a dependency of task_2]\n    task_1\n    echo "task2 is running"\n\ntask_3: |\n    ls -a\n    sudo apt-get install cowsay | head -n 0\n    cowsay "Around the world in 80 days!"\n\n//task_4: |\n    # Ignoring a task [task_4 will be ignored while execution]\n    ls | grep "ce"\n    ls > he.txt1\n\ntask_5: |\n    # Running a bash script from rush\n    ./script.sh\n```\n\n### Available Options\nTo see all the available options, run:\n```\n$ rush\n```\nor,\n```\n$ rush --help\n```\nThis should show:\n\n```\nUsage: rush [OPTIONS] [FILTER_NAMES]...\n\n  ♆ Rush: A Minimalistic Bash Utility\n\nOptions:\n  -a, --all          Run all tasks\n  --hide-outputs     Option to hide interactive output\n  --ignore-errors    Option to ignore errors\n  -p, --path         Show the absolute path of rushfile.yml\n  --no-deps          Do not run dependent tasks\n  --view-tasks       View task commands\n  -ls, --list-tasks  List task commands with dependencies\n  --no-warns         Do not show warnings\n  -v, --version      Show rush version\n  -h, --help         Show this message and exit.\n```\n\n### Running Tasks\n\n* **Run all the tasks**\n    ```\n    $ rush --all\n    ```\n\n* **Run specific tasks**\n    ```\n    $ rush task_1 task_4\n    ```\n* **Ignore specific tasks**\n\n    See the example `rushfile.yml` where the `\'//\'` before a task name means that the task will be ignored during execution\n\n    ```\n    # rushfile.yml\n\n    //task_4: |\n        echo "This task will be ignored during execution."\n    ```\n    This ignores the task named `//task_4`.\n\n* **Run tasks non interactively** (supress the outputs)\n    ```\n    $ rush --hide-outputs\n    ```\n\n* **Run tasks ignoring errors**\n    ```\n    $ rush --ignore-errors\n    ```\n\n* **Do not run the dependent tasks**\n    ```\n    $ rush task_2 --no-deps\n    ```\n\n### Viewing Tasks\n\n* **View absolute path of rushfile.yml**\n    ```\n    $ rush --path\n    ```\n    output,\n    ```\n    /home/rednafi/code/rush/rushfile.yml\n    ```\n\n* **View task commands**\n    ```\n    $ rush task_5 task_6 task_7 --view-tasks\n    ```\n    ![img](./img/rush-view.png)\n\n* **View task list with dependencies**\n    ```\n    $ rush -ls\n    ```\n\n## Quirks\n\n* Rush runs all the commands using `/usr/bin/bash`. So shell specific syntax with other shebangs might throw error.\n\n* If you are running Bash script from rush, use shebang (`#!/usr/bin/env bash`)\n\n\n## Issues\n* Rush works better with python 3.7 and up\n* If your have installed `Rush` globally and it throws a runtime error, you can try to solve it via adding the following variables to your `~./bashrc`:\n\n```\nexport LC_ALL=C.UTF-8\nexport LANG=C.UTF-8\n```\nYou can find more information about the issue and why it\'s a non-trivial problem [here.](http://click.palletsprojects.com/en/7.x/python3/#python-3-surrogate-handling)\n',
    'author': 'rednafi',
    'author_email': 'redowan.nafi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rednafi/rush',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
