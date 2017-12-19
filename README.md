# Pro Chess League Player Combination Calculator
Optimize your team's average rating!

## Usage
Use `$ python main.py` to run the program. Hopefully the program is pretty intuitive to use.
### Demo
~~~~
Type 'load' to load player data from the Internet.
Type 'manual' to enter player data manually.
>> load
Please enter url.
>> https://www.prochessleague.com/san-jose-hackers.html
Please enter desired minimum average rating.
>> 2400
~~~~
### Explanation
The user has two options to choose from:
* `>> load` the data will be automatically loaded from the prochessleague website provided
* `>> manual` the user will be able to manually enter the data of each player on the team

The desired minimum average rating is a control mechanism for the user to limit the number of possible teams outputted. Only combinations with team average rating between the inputted value and 2500 are outputted.

### Optional Feature
The data can also be written to a Excel file if the user has XlsxWriter module installed. The module can be found here: http://xlsxwriter.readthedocs.io/getting_started.html

## Current Limitations
* The program's ability to detect a player's name in the list depends on the player having a chess.com account. If the player doesn't have one, the program will skip over that player and the ratings will be misaligned.
* The regex used seems to easy to trick overall. Please be nice!
