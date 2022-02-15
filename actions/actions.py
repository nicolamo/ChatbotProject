# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List, Optional, Any
from urllib import response
import json
from pathlib import Path
import requests

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

class ActionUtterChoice(Action):
    def name(self) -> Text:
        return "action_utter_choice"
        
    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        specific_choice = str(tracker.get_slot('scelta'))
        print(specific_choice)
        if name_global == 'film' or name_global == 'movie' :
            if specific_choice == "particular film" or specific_choice == "particular movie":
                dispatcher.utter_message(response="utter_choice", name=specific_choice)
            elif specific_choice == "top trends" or specific_choice == "top charts":
                specific_choice = specific_choice + 'film'
                dispatcher.utter_message(response="utter_choice", name=specific_choice)
            else:
                dispatcher.utter_message(text="Sorry, I don't understand film")
        elif name_global== 'tv series':
            if specific_choice == "particular tv series":
                dispatcher.utter_message(response="utter_choice", name=specific_choice)
            elif specific_choice == "top trends" or specific_choice == "top charts":
                specific_choice = specific_choice + 'tv series'
                dispatcher.utter_message(response="utter_choice", name=specific_choice)
            else:
                dispatcher.utter_message(text="Sorry, I don't understand tv series")
        else:
            dispatcher.utter_message(text="Errorrrrr")
        return []
    
class ActionParticular(Action):
    def name(self) -> Text:
        return "action_particular"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #particular = str(tracker.get_slot('film'))
        particular = str(tracker.latest_message.get('text'))
        print(particular)
        output="you chose {}".format(particular)
        dispatcher.utter_message(text=output)
        return []


class ValidateFilm(FormValidationAction):
    def name(self) -> Text:
        return "validate_film_form"

    def validate_film (self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate film value."""
        return {"film": slot_value}

    async def extract_film(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        text = tracker.latest_message.get("text")
        print(text + 'ciao')
        return {"film": text}