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

class ActionRank(Action):
    def name(self) -> Text:
        return "action_rank"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        ciao = []
        team = []
        url = "https://www.legaseriea.it/it/serie-a/classifica"
        re = requests.get(url)

        try:
            soup = BeautifulSoup(re.content, 'html.parser')
            squad = soup.find_all("img", {'height':"30"})
            for b in soup.find_all("td", {'class':"blue"}):
                ciao.append(b.get_text().strip())
            for a in squad:
                team.append(a['title'])
            output = "Pos: Team Points"
            dispatcher.utter_message(text=output)
            output_cls = []
            for i in range(0,20):
                output_cls.append("{}: {} {}".format(i+1, team[i], ciao[i]))
            joined_string = "\n".join(output_cls)
            dispatcher.utter_message(text=joined_string)    
        except:
            output = "Scrivi in modo corretto"
            dispatcher.utter_message(text=output)

        return []

class ActionTopScorer(Action):
    def name(self) -> Text:
        return "action_top_scorer"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        scorer = []
        goals = []
        url = "https://www.legaseriea.it/it/serie-a/statistiche"
        re = requests.get(url)

        try:
            soup = BeautifulSoup(re.content, 'html.parser')
            table = soup.find("tbody")
            goal = table.find_all("td")
            for b in table.find_all("a"):
                scorer.append(b.get_text().strip())
            for a in table.find_all("td"):
                goals.append(a.get_text().strip())
            list = [goals[x:x+6] for x in range(0, len(goals), 6)]
            list = [x[0:4] for x in list]
            for x in list:
                x.pop(1)
            output = ["Position", "Player", "Goals"]
            output_cls = []
            length_list = [len(element) for row in list for element in row]
            column_width = max(length_list)
            output = "".join(element.ljust(column_width +2) for element in output)
            for row in list:
                row = "".join(element.ljust(column_width + 2) for element in row)
                output_cls.append("{}".format(row))
            joined_string = "\n".join(output_cls)
            dispatcher.utter_message(text=output)
            dispatcher.utter_message(text=joined_string)    
        except:
            output = "Write Correctly"
            dispatcher.utter_message(text=output)

        return []



     
    