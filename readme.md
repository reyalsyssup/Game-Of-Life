### Conway's game of life

## How to use:
When the application is launched, you get the ability to place a pattern. You simply left click to make a cell alive or dead.<br />
If you want to remove all the cells, press the "r" key to reset all cells to the dead state<br />
<br />
Once your pattern is ready, press the enter key. The background shuld turn green and the simulation will play.<br />
You can press enter again to stop the simulation.

## Saving a pattern:
If you would like to save a pattern, simply press the "s" key. This will automatically create a saveN.pickle file<br /> which can be loaded at a later time.

## Loading a pattern:
To load a pattern, you can supply a number, from 0 to the latest save. <br />
This number will load the save with the corresponding number. eg:
```
python3 main.py 4
```
<br />
This will load ```save4.pickle```