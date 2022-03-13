# bot.py
import os
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands
import data
import rps
import json
import pathlib
import datetime
import copy


hws = data.assdata()

JLOC = pathlib.Path('ass.json')            

def write_data():
    counter = 0
    assign = copy.deepcopy(hws.curass)
    tw = {}
    for ass in assign:
        ass['duedate'] = str(ass.get('duedate'))
        tw.update({counter: ass})
        ass['currdate'] = str(ass.get('currdate'))
        tw.update({counter: ass})
        counter += 1
    with open(JLOC, 'w') as outfile:
        json.dump(tw, outfile, indent = 4)

def load_data():
    if pathlib.Path.is_file(JLOC):
        with open(JLOC, 'r') as infile:
            tr = json.load(infile)
            for vals in list(tr.values()):
                hws.curass.append(vals)
        print('Loading db succesfull')
    else:
        print('No DB to load')


bot = commands.Bot(command_prefix='$')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

dict = {}

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    print('Attempting to load db')
    load_data()


COURSE_DICT = {
    '1515': 'ACIT 1515',
    '1420': 'ACIT 1420',
    '1620': 'ACIT 1620',
    '1630': 'ACIT 1630',
    '1310': 'MATH 1310',
    '1100': 'ORGB 1100',
    '1116': 'COMM 1116',
    'acit1515': 'ACIT 1515',
    'acit1420': 'ACIT 1420',
    'acit1620': 'ACIT 1620',
    'acit1630': 'ACIT 1630',
    'math1310': 'MATH 1310',
    'orgb1100': 'ORGB 1100',
    'comm1116': 'COMM 1116'
}


def parse_printall_output(ass_list) -> str:
    assignments = ass_list
    out_msg = ''
    for ass in assignments:
        out_msg += f'**For SET {ass["set"].upper()} - {COURSE_DICT[ass["course"]]}**\nAssignment: {ass["name"]}\nDue date: {ass["duedate"]}'
        out_msg += '\n\n'
    return out_msg
        
def parse_printallfor_set(set_name) -> str:
    assignments = hws.curass
    out_msg = ''
    for ass in assignments:
        if ass['set'] == set_name:
            out_msg += f'**{COURSE_DICT[ass["course"]]}**\nAssignment: {ass["name"]}\nDue date: {ass["duedate"]}'
            out_msg += '\n\n'
        # else:
        #     out_msg = 'Please check if that set exists!'
    return out_msg

def parse_printallfor_course(course_num) -> str:
    assignments = hws.curass
    out_msg = ''
    for ass in assignments:
        print(ass['course'] == str(course_num))
        if ass['course'] == str(course_num):
            out_msg += f'**For SET {ass["set"].upper()} - {COURSE_DICT[ass["course"]]}**\nAssignment: {ass["name"]}\nDue date: {ass["duedate"]}'
            out_msg += '\n\n'
        # else:
        #     out_msg = f'No homework currently assigned for {COURSE_DICT[str(course_num)]}'
    return out_msg
        
    
@client.event
async def on_message(message):
    msg = message.content

    if message.author == client.user:
        return

# Sasha's Section!!!111!!!!111!!!!11!!!!!!
# syntax $hw add set course name duedate(yyyy-mm-dd) reminder(optional)
    if message.content.startswith('$hw'):
        #ToDo: Check for arg length -- COMPLETED
        response = message.content.split()
        if len(response) < 2 or len(response) > 7:
            await message.channel.send('Usage: $hw [Set] [4 digit course num] [assignment] [duedate: yyyy-mm-dd] [reminder: optional]')
            return
        arggg = response[1]
        if arggg == 'add':
            hws.addass(response[2], response[3], response[4], response[5])
            write_data()
            await message.channel.send('Homework added successfully!')
        elif arggg == 'printall':
            output_all = parse_printall_output(hws.curass)
            await message.channel.send(output_all)
            #hws.curass
        elif arggg == 'duetoday':
            output_today = parse_printall_output(hws.duetoday())
            await message.channel.send(output_today)
        elif arggg == 'duetomorrow':
            output_tom = parse_printall_output(hws.duetomorrow())
            await message.channel.send(output_tom)
        # elif arggg == 'listcourse': REPLACED WITH COURSE BELOW
        #     await message.channel.send(hws.listcourse(response[2]))
        # elif arggg == 'listset':   REPLACED WITH SET BELOW
        #     await message.channel.send(hws.listset(response[2]))
        elif arggg == 'del':
            hws.delass(response[2], response[3], response[4], response[5])
            write_data()
        elif arggg == 'set': #for printing hw for each set
            output_set = parse_printallfor_set(response[2])
            await message.channel.send(output_set)
        elif arggg == 'course':
            output_course = parse_printallfor_course(response[2])
            await message.channel.send(output_course)
        elif arggg == 'help':
            await message.channel.send('Usage: $hw [Set] [4 digit course num] [assignment] [duedate: yyyy-mm-dd] [reminder: optional]')
            
# PLAYING ROCK PAPER SCISSORS WITH THE BOT UDAY'S SECTION   
    if msg.startswith('$rps'):
        message_list = msg.split()
        if(len(message_list) == 1):
            await message.channel.send("Usage: $rps [Choice]")
        else:
            user_choice = message_list[1][0].upper()
            winner = play_rps(user_choice, message)
            await message.channel.send(winner)


RPS_DICT = {
    'R': 'Rock',
    'P': 'Paper',
    'S': 'Scissor'
}

def play_rps(user_choice, message):
    bot_choice = rps.get_bot_choice()
    winner = rps.get_winner(user_choice, bot_choice)
    if winner == 'draw':
        return f"I chose {RPS_DICT[bot_choice]}. It's a tie."
    elif winner == 'p1':
        return f"I chose {RPS_DICT[bot_choice]}. You win!"
    else:
        return f"I chose {RPS_DICT[bot_choice]}. You lose!"


client.run(TOKEN)