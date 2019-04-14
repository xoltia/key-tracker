# key-tracker
This script allows you to keep track of how many times you press each key/mouse button,
just because I like knowing stupid statisitcs like that.

## Setup
#### Requirements
* Python
* Pip

If you do not have python you can download it [here](https://www.python.org/). Python now by default
comes with pip.

#### Installation with git
Simply clone this repository (or download it if you don't have git) and install the requirements
```
git clone https://github.com/xoltia/key-tracker.git
cd key-tracker
pip install -r requirements.txt
```

#### Installation without git
Just download it as a zip, unzip it, and install the requirements as show above without the cloning


## Usage
You run either the scripts like this
```
python (main.py/plot.py) [argument] (value) [argument] (value) ...
```
Example
```
python main.py --backup 10 -l
```
_For help use the -h argument_

### Main.py

The main script (main.py) has two optional arguments:

Args | Value | Description | Example
-----|--------|-------------|--------
-b, --backup | int | Creates a backup every [value] minutes | -b 10
-l, --log | None | Log events to the console | -l

It also has 2 keybindings:

Keybind | Action
--------|-------
CTRL+SHIFT+A | Starts a seperate recording of your key presses that will be logged to a text file. Press again to stop and save
CTRL+SHIFT+O | Show the last recording

### Plot.py

The plot script (plot.py) has 4 optional args that change the plotting behaviour:

Args | Value | Description | Default | Example
-----|-------|-------------|---------| -------
-l, --limit | int | Max amount to plot | 10 | -l 15
-m, --mouse | None | Plots mouse data instead of key data | None | -m
-o, --order | string (DESC or ASC) | What order to sort by | DESC | -o ASC
-r, --range | (int, int) | Start and end indices of plotted data | Plots from 0 until limit | -r 10,15

