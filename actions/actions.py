# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from typing import Dict, Text, Any, List, Union, Type, Optional

import typing
import logging
import requests
import json
import re
import csv
import random

# from . import otel
import actions.tracing

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, AllSlotsReset, EventType
from rasa_sdk.forms import FormAction, REQUESTED_SLOT
from rasa_sdk.executor import CollectingDispatcher

# from rasa_core.trackers import (
#    DialogueStateTracker, ActionExecuted,
#    EventVerbosity)
# from rasa_core.policies.fallback import FallbackPolicy
# from rasa_core.domain import Domain
from datetime import datetime, date, time, timedelta

# from rasa_core.utils import AvailableEndpoints
# from rasa_core.tracker_store import TrackerStore

logger = logging.getLogger(__name__)
vers = "Vers: 0.8.0, Date: Dec 30, 2020"

# otel.init_tracer("action_server")
tracer = actions.tracing.init_tracer("action_server")


def get_last_event_for(
    tracker, event_type: Text, action_names_to_exclude: List[Text] = None, skip: int = 0
) -> Optional[Any]:
    def filter_function(e):
        has_instance = e
        if e["event"] == event_type:
            has_instance = e
        excluded = e["event"] != event_type or (
            (
                e["event"] == event_type
                and (
                    (e["parse_data"]["intent"]["name"] == "domicile")
                    or (e["parse_data"]["intent"]["name"] == "customertype")
                )
            )
        )
        return has_instance and not excluded

    filtered = filter(filter_function, reversed(tracker.events))
    for i in range(skip):
        next(filtered, None)

    return next(filtered, None)


def log_slots(tracker):
    # import copy
    # Log currently set slots
    logger.debug("tracker now has {} events".format(len(tracker.events)))
    prev_user_event = get_last_event_for(tracker, "user", skip=1)
    logger.debug(
        "event.text: {}, intent: {}, confidence: {}".format(
            prev_user_event["text"],
            prev_user_event["parse_data"]["intent"]["name"],
            prev_user_event["parse_data"]["intent"]["confidence"],
        )
    )
    feedback_answer = tracker.get_slot("feedback")
    logger.debug("feedback: {}".format(feedback_answer))


class ActionKanye(Action):
    def name(self):
        # define the name of the action which can then be included in training stories
        return "action_kanye"

    def run(self, dispatcher, tracker, domain):
        with actions.tracing.extract_start_span(tracer, domain["headers"], self.name()):
            # r = requests.get("https://api.kanye.rest")
            request = json.loads(requests.get("https://api.kanye.rest").text)
            joke = request["quote"]  # extract a joke from returned json response
            dispatcher.utter_message(joke)  # send the message back to the user
            return []


class ActionRandom(Action):
    def name(self):
        # define the name of the action which can then be included in training stories
        return "action_random"

    def run(self, dispatcher, tracker, domain):
        with actions.tracing.extract_start_span(tracer, domain["headers"], self.name()):
            request = json.loads(requests.get("http://api.icndb.com/jokes/random").text)
            joke = request["value"][
                "joke"
            ]  # extract a joke from returned json response
            dispatcher.utter_message(joke)  # send the message back to the user
            return []


class ActionChuck(Action):
    def name(self):
        # define the name of the action which can then be included in training stories
        return "action_chuck"

    def run(self, dispatcher, tracker, domain):
        with actions.tracing.extract_start_span(tracer, domain["headers"], self.name()):
            request = json.loads(
                requests.get("https://api.chucknorris.io/jokes/random").text
            )  # make an apie call
            joke = request["value"]  # extract a joke from returned json response
            dispatcher.utter_message(joke)  # send the message back to the user
            return []


class ActionRon(Action):
    def name(self):
        # define the name of the action which can then be included in training stories
        return "action_ron"

    def run(self, dispatcher, tracker, domain):
        with actions.tracing.extract_start_span(tracer, domain["headers"], self.name()):
            # what your action should do
            request = json.loads(
                requests.get("https://ron-swanson-quotes.herokuapp.com/v2/quotes").text
            )  # make an apie call
            logger.debug("request: {}".format(request))
            joke = request[0] + " - Ron Swanson"
            logger.debug("joke: {}".format(joke))
            dispatcher.utter_message(joke)  # send the message back to the user
            return []


class ActionBreakingBad(Action):
    def name(self):
        # define the name of the action which can then be included in training stories
        return "action_breaking"

    def run(self, dispatcher, tracker, domain):
        with actions.tracing.extract_start_span(tracer, domain["headers"], self.name()):
            # what your action should do
            request = json.loads(
                requests.get("https://breaking-bad-quotes.herokuapp.com/v1/quotes").text
            )  # make an apie call
            author = request[0]["author"]
            quote = request[0]["quote"]
            message = quote + " - " + author
            # message = quote + ' - [' + author + '](' + permalink + ')'
            dispatcher.utter_message(message)  # send the message back to the user
            return []


class ActionCorny(Action):
    def name(self):
        # define the name of the action which can then be included in training stories
        return "action_corny"

    def run(self, dispatcher, tracker, domain):
        # what your action should do
        request = json.loads(
            requests.get("https://official-joke-api.appspot.com/random_joke").text
        )  # make an apie call
        author = request["punchline"]
        quote = request["setup"]
        message = quote + " - " + author
        # message = quote + ' - [' + author + '](' + permalink + ')'
        dispatcher.utter_message(message)  # send the message back to the user
        return []


class ActionInspiring(Action):
    def name(self):
        # define the name of the action which can then be included in training stories
        return "action_inspiring"

    def run(self, dispatcher, tracker, domain):
        with actions.tracing.extract_start_span(tracer, domain["headers"], self.name()):
            # what your action should do
            request = requests.get(
                "https://api.forismatic.com/api/1.0/?method=getQuote&lang=en&format=json"
            )
            if request.status_code == 200:
                logger.info("request.text: {}".format(request.text))
                fixed = re.sub(
                    r'(?<!\\)\\(?!["\\/bfnrt]|u[0-9a-fA-F]{4})', r"", request.text
                )
                resp = json.loads(fixed)
                author = resp["quoteAuthor"]
                quote = resp["quoteText"]
                permalink = resp["quoteLink"]
                # message = quote + ' - ' + author + ' ' + permalink
                message = quote + " - [" + author + "](" + permalink + ")"
            else:
                message = (
                    "quote service error (exceeded max free quotes?), error: "
                    + str(request.status_code)
                )
            # dispatcher.utter_message(message) #send the message back to the user
            dispatcher.utter_message(message)  # send the message back to the user
            return []


class ActionGeek(Action):
    def name(self):
        # define the name of the action which can then be included in training stories
        return "action_geek"

    def run(self, dispatcher, tracker, domain):
        with actions.tracing.extract_start_span(tracer, domain["headers"], self.name()):
            # what your action should do
            request = json.loads(
                requests.get("http://quotes.stormconsultancy.co.uk/random.json").text
            )  # make an apie call
            author = request["author"]
            quote = request["quote"]
            permalink = request["permalink"]
            # message = quote + ' - ' + author + ' ' + permalink
            message = quote + " - [" + author + "](" + permalink + ")"
            dispatcher.utter_message(message)  # send the message back to the user
            return []


class ActionTrump(Action):
    def name(self):
        # define the name of the action which can then be included in training stories
        return "action_trump"

    def run(self, dispatcher, tracker, domain):
        # what your action should do
        request = json.loads(
            requests.get("https://api.whatdoestrumpthink.com/api/v1/quotes/random").text
        )  # make an apie call
        joke = request["message"] + " - Donald Trump"
        dispatcher.utter_message(joke)  # send the message back to the user
        return []


class ActionCreed(Action):
    def __init__(self):
        self.quotes = [
            "I wanna do a cartwheel. But real casual like. Not enough to make a big deal out of it, but I know everyone saw it. One stunning, gorgeous cartwheel",
            "I've been involved in a number of cults, both a leader and a follower. You have more fun as a follower, but you make more money as a leader.",
            "Just pretend like we're talking until the cops leave.",
            "I already won the lottery. I was born in the US of A baby. And as backup I have a Swiss passport.",
            "The Taliban's the worst. Great heroin though.",
            "I run a small fake-ID company from my car with a laminating machine that I swiped from the Sheriff's station.",
            "Ryan, you told Toby that Creed has a distinct old man smell",
            "I know exactly what he's talking about, I sprout mung beans on a damp paper towel in my desk drawer, very nutritious but they smell like death",
            "Nobody steals from Creed Bratton and gets away with it. The last person to do this disappeared. His name: Creed Bratton.",
            "The only difference between me and a homeless man is this job. I will do whatever it takes to survive… like I did when I was a homeless man.",
            "I am not offended by homosexuality, in the sixties I made love to many, many women, often outdoors in the mud & rain. It's possible a man could've slipped in there. There'd be no way of knowing.",
            "You ever notice you can only ooze two things? Sexuality and pus.",
        ]

    def name(self):
        return "action_creed"

    def run(self, dispatcher, tracker, domain):
        n = random.randint(0, len(self.quotes) - 1)
        dispatcher.utter_message(self.quotes[n])  # send the message back to the user
        return []


class ActionVersion(Action):
    def name(self):
        logger.info("ActionVersion self called")
        # define the name of the action which can then be included in training stories
        return "action_version"

    def run(self, dispatcher, tracker, domain):
        with actions.tracing.extract_start_span(tracer, domain["headers"], self.name()):
            # logger.info(">>> responding with version: {}".format(vers))
            # dispatcher.utter_message(vers) #send the message back to the user
            try:
                request = json.loads(
                    requests.get("http://rasa-x:5002/api/version").text
                )
            except requests.exceptions.RequestException as e:
                logger.error(f"Rasa X version API failure, e: {e}")
                request = {"rasa-x": "", "rasa": {"production": ""}}
            logger.info(">> rasa x version response: {}".format(request["rasa-x"]))
            logger.info(
                ">> rasa version response: {}".format(request["rasa"]["production"])
            )
            dispatcher.utter_message(
                f"Rasa X: {request['rasa-x']}\nRasa:  {request['rasa']['production']}\nActions: {vers}"
            )
            return []


class ActionShowSlots(Action):
    def name(self):
        logger.info("ActionVersion self called")
        # define the name of the action which can then be included in training stories
        return "action_show_slots"

    def run(self, dispatcher, tracker, domain):
        with actions.tracing.extract_start_span(tracer, domain["headers"], self.name()):
            msg = "Slots:\n"
            for k, v in tracker.slots.items():
                msg += f" {k} | {v}\n"
            dispatcher.utter_message(msg)
            return []


def intentHistoryStr(tracker, skip, past):
    msg = ""
    prev_user_event = get_last_event_for(tracker, "user", skip=skip)
    if not prev_user_event:
        return "No prev msg"
    logger.info(
        "event.text: {}, intent: {}, confidence: {}".format(
            prev_user_event["text"],
            prev_user_event["parse_data"]["intent"]["name"],
            prev_user_event["parse_data"]["intent"]["confidence"],
        )
    )
    msg = "Ranked F1 scores:\n"
    msg += (
        "* "
        + prev_user_event["parse_data"]["intent"]["name"]
        + " ("
        + "{:.4f}".format(prev_user_event["parse_data"]["intent"]["confidence"])
        + ")\n"
    )
    for i in range(past - 1):
        msg += (
            "* "
            + prev_user_event["parse_data"]["intent_ranking"][i + 1]["name"]
            + " ("
            + "{:.4f}".format(
                prev_user_event["parse_data"]["intent_ranking"][i + 1]["confidence"]
            )
            + ")\n"
        )
    return msg
    # msg += "* " + prev_user_event["parse_data"]["intent_ranking"][2]["name"] + " (" + "{:.4f}".format(prev_user_event["parse_data"]["intent_ranking"][2]["confidence"]) + ")\n"
    # msg += "* " + prev_user_event["parse_data"]["intent_ranking"][3]["name"] + " (" + "{:.4f}".format(prev_user_event["parse_data"]["intent_ranking"][3]["confidence"]) + ")"


class ActionLastIntent(Action):
    def name(self):
        print("ActionLastIntent self called")
        # define the name of the action which can then be included in training stories
        return "action_f1_score"

    def run(self, dispatcher, tracker, domain):
        with actions.tracing.extract_start_span(tracer, domain["headers"], self.name()):
            # what your action should do
            msg = intentHistoryStr(tracker, 1, 4)
            dispatcher.utter_message(msg)  # send the message back to the user
            return []


"""
DynamicForm is currently used to determine:
  - Should the user be asked for survey feedback
  - Should debug output be provided to the user
"""


class DynamicForm(FormAction):
    def name(self):
        return "dynamic_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        logger.info("DynamicForm.required_slots")
        # lookup survey to see if we need to prompt for survey
        # return ["feedback"]
        return []
        # return ["dynamic_slot"]

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
        after all required slots are filled"""
        survey = tracker.get_slot("survey")
        debug = tracker.get_slot("debug")
        logger.info(
            "DynamicForm.submit, survey: {}, debug: {} (type: {})".format(
                survey, debug, type(debug)
            )
        )

        # if debug, utter debug info
        if debug == "1":
            msg = intentHistoryStr(tracker, 0, 4)
            dispatcher.utter_message(msg)  # send the message back to the user

        # if debug, utter debug info
        if survey == "1":
            logger.info("Survey starting...")
            dispatcher.utter_template("utter_ask_feedback", tracker)
        # - utter_ask_feedback
        # * feedback
        # - action_feedback

        return []


class TimeForm(FormAction):
    """Collects sales information and adds it to the spreadsheet"""

    def name(self) -> Text:
        return "time_form"

    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return [
            "time",
        ]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        logger.info("slot_mappings")
        logger.info(f"time: {self.from_entity(entity='time')}")
        logger.info(f"from_time: {self.from_entity(entity='from_time')}")
        logger.info(f"to_time: {self.from_entity(entity='to_time')}")
        return {
            "from": [
                self.from_entity(entity="time"),
            ],
            "to_time": [
                self.from_entity(entity="time"),
            ],
        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:

        import datetime

        if tracker.active_form:
            logger.info(f"tracker.active_form: {tracker.active_form}")
        else:
            intent_name = tracker.latest_message["intent"].get("name")
            logger.info(f"intent_name: {intent_name}")
            # logger.info(f"tracker.latest_message['intent']: {tracker.latest_message['intent']}

        entities = tracker.latest_message.get("entities", [])
        entities = {e["entity"]: e["value"] for e in entities}
        logger.info(f"entities: {entities}")
        entities_json = json.dumps(entities)
        # date = datetime.datetime.now().strftime("%d/%m/%Y")
        dispatcher.utter_message(text=entities_json)

        return []


class ActionDuckingTimeRange(Action):
    """Calculate time range
    ToDo:
      - Support additional grains (week, month, year)
      - Start date must be before end, when `time_from` is set, could be a later date
      - Fixup future dates
      - Handle null duckling entity, "start last weds"
      - Relative statements - "add a week"
    """

    def name(self) -> Text:
        return "action_time_range"

    def _extractRange(self, duckling_time, grain):
        import re

        range = dict()
        range["from"] = duckling_time
        range["to"] = duckling_time
        if grain == "day":
            # strip timezone because of strptime limitation - https://bugs.python.org/issue22377
            # 2020-02-06T00:00:00.000-08:00
            # duckling_time = re.sub(r'\.000', r' ', duckling_time)
            # duckling_time = duckling_time[:19]
            logger.info(f"time w/o ms: {duckling_time}")
            duckling_dt = datetime.strptime(duckling_time, "%Y-%m-%dT%H:%M:%S")
            # dt = datetime.strptime("2020-03-07T00:00:00 -07:00", "%Y-%m-%dT%H:%M:%S %z")
            logger.info(f"duckling_dt: {duckling_dt}")
            dt_delta = duckling_dt + timedelta(hours=24)
            range["to"] = dt_delta.strftime("%Y-%m-%dT%H:%M:%S%z")

        return range

    def run(self, dispatcher, tracker, domain) -> List[EventType]:
        with actions.tracing.extract_start_span(tracer, domain["headers"], self.name()):
            # existing slot values
            from_time = tracker.get_slot("from_time")
            to_time = tracker.get_slot("to_time")

            # duckling value
            duckling_time = tracker.get_slot("time")

            logger.info(
                f"duckling_time: {type(duckling_time)}, value: {duckling_time}, to_time: {to_time}, from_time: {from_time}"
            )
            # do we have a range
            if type(duckling_time) is dict:
                from_time = tracker.get_slot("time")["from"][:19]
                to_time = tracker.get_slot("time")["to"][:19]
            else:
                logger.info(f"latest_message: {tracker.latest_message}")
                entities = tracker.latest_message.get("entities", [])
                logger.info(f"entities 1: {entities}")
                entities = {e["entity"]: e["value"] for e in entities}
                logger.info(f"entities: {entities}")
                additional_info = tracker.latest_message.get("entities", [])[0][
                    "additional_info"
                ]
                logger.info(f"grain: {additional_info['grain']}")
                state = tracker.current_state()
                intent = state["latest_message"]["intent"]["name"]
                logger.info(f"intent: {intent}")
                if intent == "time_from" and to_time:
                    logger.info(f"setting from_time: {duckling_time[:19]}")
                    from_time = duckling_time[:19]
                else:
                    range = self._extractRange(
                        duckling_time[:19], additional_info["grain"]
                    )
                    from_time = range["from"]
                    to_time = range["to"]

            # entities = {e["entity"]: e["value"] for e in entities}
            # logger.info(f"entities 2: {entities}")
            # entities_json = json.dumps(entities)

            # date = datetime.datetime.now().strftime("%d/%m/%Y")
            # dispatcher.utter_message(text=entities_json)
            logger.info(f"from: {from_time} to: {to_time}")
            dispatcher.utter_message(text=f"from: {from_time}\n  to: {to_time}")

            return [SlotSet("from_time", from_time), SlotSet("to_time", to_time)]
