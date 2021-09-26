# use Flask as web server

from flask import Flask
from threading import Thread # server run on separate thread than bot
# to both run at same time 

app=Flask('')

@app.route('/')

def home():
  return "Hello. I am alive!"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
  t=Thread(target=run)
  t.start()


