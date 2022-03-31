# PhoenixBotty
IRC Bot, derived from Pallaber Bot, Architectonic rework

Designed for non-technical channels

## Usage

### Requirements
 - Python 3.5
 - pip
 - wikipedia package (can be installed using pip; tested with version 1.4.0)
 - virtualenv (optional)
 
### Running the Bot
The direct way:
```bash
# Install all dependencies
pip install -r requirements.txt
# First load all needed strings into the database
# Per default german is used. If you want another language you need to 
# add an language file and modify the script.
# Later it will be refactored, so it uses arguments
python ReadInternationalization.py
# Create a configuration file by having a look at config-example.txt
# Start the bot using the given config file.
python Main.py --config ./config.txt
``` 
Using [faust-bot-run.sh](https://github.com/SophieBartmann/Faust-Bot/blob/master/faust-bot-run.sh). This script creates and uses a virtual environment, therefore the optional requirement virtualenv is required
```bash
# Make the script executable
chmod u+x ./faust-bot-run.sh
# To display all possible options
./script -h
> Simple script to manage a single faust-bot instance.
>  -h  displays this help message
>  -s  starts the bot, if it is not running yet
>  -e  exits/stops the bot
>  -r  restarts the bot
>  -u  updates the bots code
# Start the bot.
# The script creates an virtualenv, installs all pip dependencies and starts the Bot in the background
# The pid of the Bot-process is saved in .pid.
# Stdout is redirected to out.txt 
./script -s
```


## Contribution
Have a look into our issues. Some are explizitly marked as `help wanted` or `For Beginners`. If you're new to programming the last one would be a good point to begin with. Of course you're also free to choose your own issue or task to work on.
If you have any question you're also welcome to join us in `#faust-bot` on freenode.

Before creating a pull request please test your code. Untested, obviously buggy code will - of course - be rejected.
Since we're programming in python please hold on [PEP-08](https://www.python.org/dev/peps/pep-0008/).

### Branching
Currently we use the [main-branch](https://github.com/SophieBartmann/Faust-Bot/edit/master/README.md) for development and the stable version is represented with the [stable-branch](https://github.com/SophieBartmann/Faust-Bot/tree/stable). Please create an own feature-branch if you want to contribute. This will make it easier to merge.

## Copyright
```
    Faust-Bot. A simple, extensible IRC bot.
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
```
The `care_icd10_de.csv` was taken from the [CARE2X - Integrated Hospital Info System Project on Sourceforge](https://sourceforge.net/projects/care2002/).
