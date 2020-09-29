# Discord bot which does some simple tasks and Toonify.

'''
Toonify links - 
https://toonify.justinpinkney.com/
https://deepai.org/machine-learning-model/toonify
'''

import os
import random
import discord
from dotenv import load_dotenv
import requests

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    #print(f'{client.user} has connected to Discord!')
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    '''
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')
    '''

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print(message.content)
    print(type(message.content))
    
    if message.content == '-toonify':
        if message.attachments:
            print(message.attachments[0].url)
            r = requests.post(
            "https://api.deepai.org/api/toonify",
            data={
                'image': message.attachments[0].url,
            },
            headers={'api-key': os.getenv('TOONIFY_API_KEY')}
            )

            print(r.json()['output_url'])
            await message.channel.send(r.json()['output_url'])
            r.json()
            print(r.output_url)
        else:
            await message.channel.send("No image")

    
    #with open('donut.jpeg', 'rb') as fp:
        #await message.channel.send(file=discord.File(fp, 'donut.jpeg'))


    friends_quotes = ['We were on a break!',
    'Joey doesn’t share food!',
    'Hi, I’m Chandler. I make jokes when I’m uncomfortable.',
    'I wish I could, but I don’t want to.',
    'This is all a moo point.',
    'You can’t just give up. Is that what a dinosaur would do?',
    'They don’t know that we know they know we know.',
    'I don’t even have a ‘pla.',
    "How you doin'?",
    'I am not good at advice, Can i interest you in a sarcastic comment?'
    ]

    words = ['friends', 'Friends', 'FRIENDS', 'F.R.I.E.N.D.S']

    #if 'friends' in message.content:
    if any(x in message.content for x in words):
        response = random.choice(friends_quotes)
        await message.channel.send(response)
        print(response)
    #elif message.content == 'raise-exception':
        #raise discord.DiscordException

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

client.run(TOKEN)