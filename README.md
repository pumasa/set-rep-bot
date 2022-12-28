# Set Rep Bot

## Description

This is a simple bot that will help students track their homework assignments and due dates. It has been designed to be used in a classroom setting, but can be used for any purpose. 

This bot is currently stores the data on a MongoDB database. It removes the need for a database administrator to manage the database. The bot will automatically create a new database and collection if one does not already exist.

Once the bot is running, it will listen for commands from users. The bot will respond to the commands and display the results in the channel where the command was issued.

Old assignments will be automatically deleted from the database every hour.

## Installation

1. Clone the repository
2. Run `pip install -r requirements.txt`
3. Change the client credentials and Discord token in `bot.py`
4. Run `python bot.py`


## Usage

The bot has a few commands that can be used to interact with it. The prefix for all commands is `$`.

`$hw_help` - Displays a list of commands and their usage

`$hw_add <SET> <COURSE_NUMBER> <ASSIGNMENT_INFO> <DUE_DATE(m/d/y)> <time>` - Adds a new assignment to the list

`$hw_del <SET> <COURSE_NUMBER> <ASSIGNMENT_INFO> <DUE_DATE(m/d/y)> <time>` - Deletes an assignment from the list

`$hw_set <SET>` - Displays the list of assignments by set

`$hw_course <COURSE_NUMBER>` - Displays the list of assignments by course

`$duetoday <SET>` - Displays the list of assignments that are due today

`$duetomorrow` - Displays the list of assignments that are due tomorrow

`$rps_game <SELECTION>` - Play a game of rock, paper, scissors with the bot (selections are R, P, or S)

## Future Plans

- [ ] Update duetoday function to display assignments that due for a specific set

- [ ] Error handling for invalid commands

- [ ] Add a function to display assignments that are due in the next 7 days

- [ ] Update duetomorrow function to display assignments that are due for a specific set and due tomorrow and not just all the days after today

- [x] Make the bot to @ at the group of students who have assignments due

- [ ] Make the bot more interactive

## Created By

Sasha Fey

Uday Chinna

Jack Tam

Mike Picus