# Pro Chess League Player Combination Calculator
Optimize your team's average rating!
https://www.prochessleague.com/

## Usage
This program has two modes of use: manual and load.
After all necessary player data has been gathered, these two methods converge for output customization.

### Manual Mode
User will manually enter the information for each player.
To start manual mode, run `$ python main.py -manual` (`$ python main.py` will also work).
For each player, `LASTNAME` and `RATING` are required. `ISFREEAGENT` and `ISFEMALE` are optional and will default to Local (`False`) and Male (`False`). Once you have inputted all the players, type `exit` to move onto output customization.
Note: you should enter either `True` or `False` for `ISFREEAGENT` and `ISFEMALE`. Also, if you wish to enter a value for `ISFEMALE`, you must also specify a value for `ISFREEAGENT`.
See Demos for an example.

### Load Mode
The data will be loaded from a specified prochessleague website and chess-db.com.
Run `$ python main.py -load` to launch this mode. There are two ways of supplying the website: either as a commandline argument right after `-load` when running the python file or during runtime.
The program will automatically gather the data and move onto output customization.
See Demos.

### Output Customization
Whether you chose Manual Moder or Load Mode, this is a necessary step where you can limit and customize the output combinations.
First, you have the option to fix players to specific boards. This is especially powerful when you know you want a particular player to be in the line-up.
To fix a player to a board, type his/her name on the corresponding board. Hit Enter for boards that anyone can occupy.
Second, you need to enter the minimum average rating of the possible line-ups. You can choose any value between 2000 (inclusive) and 2500 (exclusive).
The possible combinations are then computed and displayed.

#### Optional Feature
The data can also be written to a Excel file if the user has XlsxWriter module installed. The module can be found here: http://xlsxwriter.readthedocs.io/getting_started.html

### Demos
Sample lines for entering a player manually:
`Carlsen 2843`
`Hou 2654 True True`

Using `-load`:
`$ python main.py -load https://www.prochessleague.com/san-jose-hackers.html`
OR
~~~~
$ python main.py -load
Please enter url.
>> https://www.prochessleague.com/san-jose-hackers.html
~~~~

Output Customization and Optional Feature:
~~~~
Would you like to fix board? (y/n)
>> y
Please enter player's last name.
Hit Enter if no preference for that board.
Board 1: Mamedyarov
Board 2:
Board 3:
Board 4: Ravuri
Please enter desired minimum average rating.
>> 2400
~~~~
The possible combinations are then displayed.
~~~~
Write to Excel? (y/n)
>> y
Please enter file name.
>> san_jose_hackers
~~~~

## Current Limitations
* The program's ability to detect a player's name in the list depends on the player having a chess.com account. If the player doesn't have one, the program will skip over that player and the ratings will be misaligned.
* The regex used seems too easy to trick overall. Please be nice!
