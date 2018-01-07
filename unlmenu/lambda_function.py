"""
This is a simple Alexa Skill that reads the menu for Cather/Pound/Neihardt.
"""
from __future__ import print_function
import requests
from bs4 import BeautifulSoup


def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    if (event['session']['application']['applicationId'] != "amzn1.ask.skill.66216d4e-38c6-4a1d-ab33-c2ad798c2f2b"):
        raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "GetMenuIntent":
        return get_menu(intent, session)
    elif intent_name == "GetMenuMealIntent":
        return get_menu(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response(intent, session)
    elif intent_name == "AMAZON.CancelIntent":
        return get_cancel_response(intent, session)
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    session_attributes = {}
    card_title = "Menu"
    speech_output = "Hello, I can read you the menu. " \
                    "For example, you can say, " \
                    "what's on the menu.  " \
                    "Or you can tell me the specific meal you want. " \
                    "For example, you can say, " \
                    "what's on the menu for breakfast"

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me what menu you want. " \
                    "For example, you can say, " \
                    "what's on the menu.  " \
                    "Or you can tell me the specific meal you want. " \
                    "For example, you can say, " \
                    "what's on the menu for breakfast"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_help_response(intent, session):
    session_attributes = session.get('attributes', {})
    card_title = "Help"
    speech_output = "I can read you the menu. Just say, " \
                    "what's on the menu. Or you can tell me the specific " \
                    "meal you want. For example, you can say, " \
                    "what's on the menu for breakfast.  Please tell me what menu you want."
    reprompt_text = "I'm sorry, I didn't hear what you said. " \
                    "Please tell me what menu you want."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_cancel_response(intent, session):
    session_attributes = {}
    card_title = "Goodbye"
    speech_output = "OK, goodbye"
    reprompt_text = None
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_url(meal):
    """
    Returns the URL for the RSS feed based on the menu
    """
    if meal is None:
        # Default to US & Canada
        return "http://menu.unl.edu/services/dailymenu.aspx?action=getdailymenuforentireday&complexId=24&mealdate=11-14-2016"
    elif meal == 'breakfast':
        return "http://menu.unl.edu/services/dailymenu.aspx?action=getdailymenuwithmealtime&mealdate=11-14-2016&mealname=breakfast&complexid=24"
    elif meal == 'lunch':
        return "http://menu.unl.edu/services/dailymenu.aspx?action=getdailymenuwithmealtime&mealdate=11-14-2016&mealname=lunch&complexid=24"
    elif meal == 'dinner':
        return "http://menu.unl.edu/services/dailymenu.aspx?action=getdailymenuwithmealtime&mealdate=11-14-2016&mealname=dinner&complexid=24"
    else:
        # Fallback to default
        print("Meal {} is not supported. Defaulting to menu".format(meal))
        return "http://www.omaha.com/search/?mode=article&q=&t=article&l=30&d=&d1=1+week+ago&d2=&s=priority&sd=desc&k=%23homepage&f=atom"


def get_menu(intent, session):
    """ Gets the news headlines"""
    card_title = "Menu"
    session_attributes = session.get('attributes', {})
    meal = None

    try:
        menu = intent['slots']['Meal']['value']
    except KeyError:
        pass

    if not meal:
        meal = "breakfast"

    url = get_url(meal)
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')
    menuitems = soup.find_all('MealItemNameTrimmed')

    speech_output = "Here's the menu."
    for menuitem in menuitems:
        speech_output += "<break> " + menuitem

    reprompt_text = None
    should_end_session = True

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
