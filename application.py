#Import relevant modules Tweepy, Flask and auth
import tweepy
from email.mime import application
from flask import (Flask, render_template, request)
from auth import (access_token, access_token_secret, api_key, api_key_secret,
                  bearer_token)

application = Flask(__name__, template_folder="template", static_folder="static")

#function to get the credentials see - https://docs.tweepy.org/en/stable/client.html
def client_cred():
  client = tweepy.Client(bearer_token=bearer_token, consumer_key=api_key, consumer_secret=api_key_secret, access_token=access_token, access_token_secret=access_token_secret)
  return client

#define Flask route
@application.route("/", methods=['GET','POST'])
def index():
  if request.method == 'POST':
    #This helps retrieve the search term which is used in the Twitter API query
    query = request.form.get('query')
    
    #Tweepy's Spaces Lookup see - https://docs.tweepy.org/en/stable/client.html#spaces-lookup, 
    #This calls the Twitter API and returns a result
    spaces = client_cred().search_spaces(query, expansions="creator_id", max_results=100, space_fields = "title,participant_count,subscriber_count,scheduled_start,creator_id", state="all", user_fields="name,id,profile_image_url,description")
    
    #Condition to check if there is a Twitter Space matching the query
    #If there is no match "There are no spaces matching your search" is displayed 
    if spaces.meta["result_count"] == 0:
      return render_template("index.html", count = "There are no spaces matching your search")
    
    #If there are results matching the query, this runs
    else:
      host_deets = spaces.includes["users"] #Get user details of the host 
      merger = {user["id"]: user for user in host_deets } #Converts the user details into a dictionary to be matched to each Space details 
      spaces = spaces.data #This contains the details of all spaces matching the search term
      
      #Pass the relevant data to the html file
      return render_template("index.html", spaces = spaces, merge = merger , query = query)
  return render_template("index.html")


if __name__ == "__main__":
  application.run(host = "127.0.0.1", debug = True)
