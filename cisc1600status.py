"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import bs4
import datetime
import re
import urllib2


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


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ Since this is so simple, this function is the main show
    """

    session_attributes = {}
    card_title = "CISC 1600"
    speech_output = parseCisc1600Page()

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = None
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for talk to CISC 1600. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


# --------------- Helpers for crawling page ------------------

def parseCisc1600Page(now=None):
    if now is None:
        now = datetime.datetime.now()
        
    url = "http://mr-pc.org/t/cisc1600/"
    page = urllib2.urlopen(url)
    soup = bs4.BeautifulSoup(page, "html.parser")

    table = soup.body.find('table', attrs={'id' : 'weeks'})
    schedule = parseListOfLists(tableToListOfLists(table))
    return describeNextClassTopic(schedule, now) \
        + " " + describeNextAssignment(schedule, now)


def tableToListOfLists(table):
    data = []
    rows = table.findAll('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        # data.append([ele for ele in cols if ele]) # Get rid of empty values
        data.append(cols)
    return data

def parseListOfLists(lol):
    return [(parseDate(row[0]), row[1], row[2].split('\n '))
            for row in lol if len(row) >= 3]
        
def parseDate(dateStr):
    return datetime.datetime.strptime(dateStr.split(u'\xa0')[0] + " 11:00",
                                      '%Y/%m/%d %H:%M')

def describeNextClassTopic(schedule, now):
    for classStart, topic, due in schedule:
        if classStart > now:
            mainTopic = topic.split('\n')[0]
            dayDiff = (classStart - now).days
            if dayDiff == 0:
                return "Today's topic is %s." % mainTopic
            if dayDiff == 1:
                return "Tomorrow's topic will be %s." % mainTopic
            else:
                return "The next topic will be %s in %s days." % (mainTopic, dayDiff)
            
def describeNextAssignment(schedule, now):
    for classStart, topic, due in schedule:
        if classStart == now and len(due) >= 1 and len(due[0]) >= 1:
            return "For assignments, today %s." % formatDue(due)
        if classStart > now and len(due) >= 1 and len(due[0]) >= 1:
            dayDiff = (classStart - now).days
            if dayDiff == 1:
                return "For assignments, tomorrow %s." % formatDue(due)
            else:
                return "For assignments, %s on %s, which is in %s days." % (
                    formatDue(due), classStart.strftime("%B %d"), dayDiff)

def formatDue(due):
    items = [re.sub("(\w+)$", r"is \1", item)
             for item in due if not re.search("[sS]pec", item)]
    return " and ".join(items)



# --------------- Events ------------------

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
    if intent_name == "GetUpcomingInfo":
        return get_welcome_response()
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

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
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
