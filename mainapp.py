import configparser
import json
from distutils.command.config import config
import tweepy
from flask import (Flask, render_template, request)
from auth import (access_token, access_token_secret, api_key, api_key_secret,
                  bearer_token)

app = Flask(__name__, template_folder="template", static_folder="static")

def client_cred():
  #get the credentials 
  client = tweepy.Client(bearer_token=bearer_token, consumer_key=api_key, consumer_secret=api_key_secret, access_token=access_token, access_token_secret=access_token_secret)
  return client

@app.route("/", methods=['GET','POST'])
def index():
  if request.method == 'POST':
    query = request.form.get('query')
    
    spaces = client_cred().search_spaces(query, expansions="speaker_ids", max_results=None, space_fields = "title,participant_count", state="all", user_fields="username")
    
    return render_template("index.html", spaces = spaces.data)
  return render_template("index.html")

if __name__ == "__main__":
  app.run(host = "127.0.0.1", debug = True)

