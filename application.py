import configparser
from email.mime import application
import json
from distutils.command.config import config
import tweepy
from flask import (Flask, render_template, request)
from auth import (access_token, access_token_secret, api_key, api_key_secret,
                  bearer_token)

application = Flask(__name__, template_folder="template", static_folder="static")

columns = ['id', 'title' , 'state', 'participant count', 'url', 'username']
data = []

def client_cred():
  #get the credentials 
  client = tweepy.Client(bearer_token=bearer_token, consumer_key=api_key, consumer_secret=api_key_secret, access_token=access_token, access_token_secret=access_token_secret)
  return client

@application.route("/", methods=['GET','POST'])
def index():
  if request.method == 'POST':
    query = request.form.get('query')
    
    spaces = client_cred().search_spaces(query, expansions="creator_id", max_results=100, space_fields = "title,participant_count,subscriber_count,scheduled_start,creator_id", state="all", user_fields="name,id")

    if spaces.meta["result_count"] == 0:
      print("There are no spaces matching your query")
      return render_template("index.html", count = "There are no spaces matching your search")

    else:
      return render_template("index.html", spaces = spaces.data, host = spaces.includes["users"][0] , query = query)
  return render_template("index.html")


if __name__ == "__main__":
  application.run(host = "127.0.0.1", debug = True)
