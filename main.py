import os
import discord
import requests # allows to make http request to get data from api
import json 
import random 

from replit import db # import repl db
from keep_alive import keep_alive

# instance of a client, connection to discord
client=discord.Client()

# list that contains sad word 
sad_words=["sad","depressed","unhappy", "miserable", "depressing"]

starter_encouragements=[
  "Cheer up!",
  "Hang in there.",
  "You are a great person/bot!"
]

if "responding" not in db.keys():
  db["responding"]=True

def get_quote():
  response=requests.get("https://zenquotes.io/api/random")
  json_data=json.loads(response.text)
  quote=json_data[0]['q']+ " - "+json_data[0]['a']
  return(quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements=db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"]=encouragements
  else:
    db["encouragements"]=[encouraging_message]

def delete_encouragements(index):
  encouragements=db["encouragements"]
  if len(encouragements)>index:
    del encouragements[index]
    db["encouragements"]=encouragements


# register an event (asyncronous event, callback)
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

# another event, if bot receive a message
@client.event
async def on_message(message):
  if message.author==client.user:
    return

  msg=message.content

  if msg.startswith('hi'):
    await message.channel.send('Hi There')
  
  if msg.startswith('$inspire'):
    quote=get_quote()
    await message.channel.send(quote)

  if db["responding"]:
    options=starter_encouragements
    if "encouragements" in db.keys():
      #options=options + db["encouragements"] # error can only concat
      options.extend(db["encouragements"])

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

# $new + encouraging_message(by user)
  if msg.startswith("$new"):
    encouraging_message=msg.split("$new ",1)[1] 
    #getting second elem in array after space of new 
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  #delete 
  if msg.startswith("$del"):
    encouragements=[]
    if "encouragements" in db.keys():
      index=int(msg.split("$del",1)[1])
      delete_encouragements(index)
      encouragements=db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("$list"):
    encouragements=[]
    if "encouragements" in db.keys():
      encouragements=db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("$responding"):
    value=msg.split("$responding ",1)[1]

    if value.lower()== "true":
      db["responding"]=True
      await message.channel.send("Responding is on.")
    else:
      db["responding"]=False
      await message.channel.send("Responding is off.")

keep_alive() # this will run web server
# use environment variable to keep token 
my_secret = os.environ['TOKEN']
client.run(my_secret) #client.run(os.getenv('TOKEN'))

  
