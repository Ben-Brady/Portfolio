import os
import time
import json
import requests
import datetime

from dotenv import load_dotenv
load_dotenv()

AUTH = requests.auth.HTTPBasicAuth(os.getenv('GUSER'), os.getenv('GTOKEN'))

EventList = []
HeartBeat = 0.0

class Commit:
    def __init__(self,JSON):
        self.type = 'Commit'
        self.id =  JSON['id']
        self.repo = JSON['repo']['name']
        self.message= JSON['payload']['commits'][0]['message']
        self.public= (JSON['public'] == 'true')
        self.date= datetime.datetime.strptime(JSON['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        self.url= f"https://github.com/{JSON['repo']['name']}/commit/{JSON['payload']['commits'][0]['sha']}"
        self.avatar= JSON['actor']['avatar_url']

class Create:
    def __init__(self,JSON):
        self.type = 'Create'
        self.id =  JSON['id']
        self.repo = JSON['repo']['name']
        self.public= (JSON['public'] == 'true')
        self.date= datetime.datetime.strptime(JSON['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        self.url= f"https://github.com/{JSON['repo']['name']}"
        self.avatar= JSON['actor']['avatar_url']

def GenerateClass(JSON:dict):
    if JSON['type'] == 'PushEvent':
        return Commit(JSON)
    elif JSON['type'] == 'CreateEvent':
        return Create(JSON)
        
def GenerateCommits():
    r = requests.get('https://api.github.com/users/ThatGayKid/events',auth=AUTH)
    JSON = json.loads(r.text)
    
    for Event in JSON:
        Event = GenerateClass(Event)
        if Event:
            if not (Event.id in EventList or Event.public):
                EventList.append(Event)
    
    return sorted(EventList,reverse=True, key=lambda x: x.date)




def GetCommits():
    global HeartBeat
    global EventList
    Time = time.time()
    if (Time - HeartBeat) > 3600:
        HeartBeat = Time
        EventList = GenerateCommits()
                    
    return EventList[:10]