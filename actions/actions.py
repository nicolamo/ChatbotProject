# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import imp
import time
from matplotlib.pyplot import get
from sqlalchemy import true
import urllib3
import lxml
import selenium
from typing import Any, Text, Dict, List, Optional, Any
import urllib.request
from bs4 import BeautifulSoup
import json
from pathlib import Path
import requests
import asyncio
from selenium import webdriver
from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.knowledge_base.storage import InMemoryKnowledgeBase
from rasa_sdk.knowledge_base.actions import ActionQueryKnowledgeBase
from rasa_sdk.events import SlotSet

from rasa_sdk import FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
#


class ActionHelloWorld(Action):
    def name(self) -> Text:
        return "action_hello_world"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Hello World!")
        return []

class ActionUtterProva(Action):
    def name(self) -> Text:
        return "action_utter_prova"
        
    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = str(tracker.get_slot('choice'))
        global name_global
        name_global = name
        output="Great Choice! Are you interested in a particular {} or would you like to see top trends?".format(name)
    
        dispatcher.utter_message(text=output)
        return []
    
class ActionParticular(Action):
    def name(self) -> Text:
        return "action_particular"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        link = []
        title = []
        particular = str(tracker.get_slot('squadra'))
        output="you chose {}".format(particular)
        url = "https://www.sportmediaset.mediaset.it/calcio/{}/".format(particular.lower())
        try:
            re = requests.get(url)
            soup = BeautifulSoup(re.content, 'html.parser')
        
            paging = soup.find_all("h2", {'class':"article-heading"})
            for a in soup.find_all("a", {'data-urltype':"alltitle", 'href' : True}):
                link.append(a['href'])
        
            for tag in paging:
                title.append(tag.get_text().strip())
            link = link[1:11]
            title = title[1:11]
            for i in range(0,10):
                output1 = "News: {}, Link: {}".format(title[i], link[i])
                dispatcher.utter_message(text=output1)
        except:
            output = "Write team name correctly"
            dispatcher.utter_message(text=output)
        return []

class ActionParticularTopNewsFootball(Action):
    def name(self) -> Text:
        return "action_particular_football_topnews"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        link = []
        title = []
        particular = str(tracker.get_slot('squadra'))
        output="you chose {}".format(particular)
        url = "https://www.sportmediaset.mediaset.it/calcio/".format(particular.lower())
        re = requests.get(url)
        soup = BeautifulSoup(re.content, 'html.parser')
        paging = soup.find_all("h2", {'class':"article-heading"})
        for a in soup.find_all("a", {'data-urltype':"alltitle", 'href' : True}):
            link.append(a['href'])
        
        for tag in paging:
            title.append(tag.get_text().strip())
        link = link[1:11]
        title = title[1:11]
        for i in range(0,10):
            output1 = "News: {}, Link: {}".format(title[i], link[i])
            dispatcher.utter_message(text=output1)
        return []

class ActionParticularTopNews(Action):
    def name(self) -> Text:
        return "action_particular_topnews"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        link = []
        title = []
        particular = str(tracker.get_slot('choice'))
        url = "https://www.sportmediaset.mediaset.it/{}/".format(particular.lower())
        re = requests.get(url)
        try:
            soup = BeautifulSoup(re.content, 'html.parser')
            paging = soup.find_all("h2", {'class':"article-heading"})
            for a in soup.find_all("a", {'data-urltype':"alltitle", 'href' : True}):
                link.append(a['href'])
        
            for tag in paging:
                title.append(tag.get_text().strip())
            link = link[1:11]
            title = title[1:11]
            for i in range(0,10):
                output1 = "News: {}, Link: {}".format(title[i], link[i])
                dispatcher.utter_message(text=output1)
        except:
            output = "Write sport name correctly"
            dispatcher.utter_message(text=output)
        return []




     
    