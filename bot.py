import os
import discord
from discord.ext import commands
import pymongo
from datetime import datetime, timedelta
import rps
import threading
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
MONGO_USER = os.getenv('MONGO_USER')
MONGO_PASS = os.getenv('MONGO_PASS')

# Connect to the MongoDB database
client = pymongo.MongoClient("mongodb+srv://"+MONGO_USER+":"+MONGO_PASS+"@agile.d4nez.mongodb.net/?retryWrites=true&w=majority")
db = client.test

# Set up the bot with the command prefix '$'
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$', intents=intents)

# Define the MongoDB collection that will store the homework assignments
homework_collection = db.homework

# Get the current date
current_date = datetime.today().date()


########################################################################################
# Define a command to display usage information
@bot.command()
async def hw_help(self):
    await self.send("""Usage:
                    $hw_add <Set> <Course ID> <Assignment Info> <Due Date (m/d/y)>
                    $hw_del <Set> <Course ID> <Assignment> <Due Date>
                    $hw_set <Set>
                    $hw_course <Course ID>""")


########################################################################################
# Define a command to add homework assignments to the collection
@bot.command()
async def hw_add(self, set_id: str, course: str, assignment: str, due: str, time: str):
    # Convert due date to a datetime object
    due_date = datetime.strptime(due, '%m-%d-%Y')

    # Insert the homework assignment into the collection
    homework_collection.insert_one({
        "set_id": set_id,
        "course": course,
        "assignment": assignment,
        "due": due_date,
        "time": time
    })
    await self.send("Homework assignment added successfully.")


########################################################################################
# Define a command to delete homework assignments from the collection
@bot.command()
async def hw_del(self, set_id: str, course: str, assignment: str, due: str, time: str):
    # Convert due date to a datetime object
    due_date = datetime.strptime(due, '%m-%d-%Y')

    # Delete the homework assignment from the collection
    homework_collection.delete_one({
        "set_id": set_id,
        "course": course,
        "assignment": assignment,
        "due": due_date,
        "time": time
    })
    await self.send("Homework assignment deleted successfully.")


########################################################################################
# Define a command to get homework assignments by set
@bot.command()
async def hw_set(self, set_id: str):
    # Find all homework assignments with the specified set ID
    assignments = list(homework_collection.find({"set_id": set_id}))
    if assignments:
        # Create a dictionary to store the records, using the due date as the key
        records_by_due_date = []

        # Iterate through the records and group them by due date
        for record in homework_collection.find():
            due_date = record['due']
            records_by_due_date[due_date].append(record)

        # Print the records grouped by due date
        for due_date, records in records_by_due_date.items():
            await self.send(f"Testing:{due_date}.")
            print(f'Due date: {due_date}')
            for record in records:
                await self.send(f"{record}")
                print(record)
            print()
        # Format the assignments as a string and send them to the user
        hw_string = "\n".join([f"Due: **{a['due'].strftime('%B %d, %Y')}**\n**ACIT {a['course']}:**\n> •{a['assignment']} @{a['time']}\n\n" for a in assignments])
        await self.send(f"@here Homework assignments for set {set_id}:\n{hw_string}")
    else:
        await self.send(f"No assignments found for set {set_id}.")


########################################################################################
# Define a command to get homework assignments by course
@bot.command()
async def hw_course(self, course: str):
    # Find all homework assignments with the specified course
    assignments = list(homework_collection.find({"course": course}))
    if assignments:
        # Format the assignments as a string and send them to the user
        hw_string = "\n".join([f"{a['assignment']} (Due: {a['due']})" for a in assignments])
        await self.send(f"Homework assignments for course {course}:\n{hw_string}")
    else:
        await self.send(f"No assignments found for course {course}.")


########################################################################################
# Define a command to get homework assignments due today
@bot.command()
async def duetoday(self):
    # tomorrow = today + timedelta(days=1)
    result = homework_collection.find({"due": {"$eq": datetime.strptime(str(current_date), '%Y-%m-%d')}})
    if result:
        homework = "\n".join([f"Set {assignment['set_id']} - Course: {assignment['course']} - {assignment['assignment']}" for assignment in result])
        await self.send(f"Homework due today:\n{homework}")
    else:
        await self.send("No homework due today.")


########################################################################################
# Define a command to get homework assignments due tomorrow
@bot.command()
async def duetomorrow(self):
    tomorrow = current_date + timedelta(days=1)
    result = homework_collection.find({"due": {"$gte": datetime.strptime(str(tomorrow), '%Y-%m-%d')}})
    if result:
        homework = "\n".join([f"Set {assignment['set_id']} - Course: {assignment['course']} - {assignment['assignment']}" for assignment in result])
        await self.send(f"Homework due tomorrow:\n{homework}")
    else:
        await self.send("No homework due tomorrow.")


########################################################################################
def delete_expired_homework():
    result = db.homework.delete_many({"due": {"$lt": datetime.strptime(str(current_date), '%Y-%m-%d')}})
    print(f"{result.deleted_count} documents deleted.")


# Create a timer that runs the delete operation every hour
timer = threading.Timer(3600, delete_expired_homework)
timer.start()


########################################################################################
# PLAYING ROCK PAPER SCISSORS WITH THE BOT UDAY'S SECTION
RPS_DICT = {
    'R': 'Rock',
    'P': 'Paper',
    'S': 'Scissor'
}


@bot.command()
async def rps_game(self, choice: str):
    user_choice = choice[0].upper()
    bot_choice = rps.get_bot_choice()
    winner = rps.get_winner(user_choice, bot_choice)
    if winner == 'draw':
        await self.send(f"I chose {RPS_DICT[bot_choice]}. It's a draw!")
    elif winner == 'user':
        await self.send(f"I chose {RPS_DICT[bot_choice]}. You win!")
    else:
        await self.send(f"I chose {RPS_DICT[bot_choice]}. I win!")

########################################################################################

########################################################################################

# Run the bot
bot.run(DISCORD_TOKEN)
