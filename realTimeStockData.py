from realTimeStockData.stock import Stock

def lambda_handler(event, context):
    print("event.session.application.applicationId=" + event['session']['application']['applicationId'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])

def on_launch(launch_request, session):
	return get_stock_info_response()

def on_intent(intent_request, session):
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    if intent_name == "StockInfoIntent":
        return get_stock_info_response()
    elif intent_name == "StockPriceIntent":
        return get_stock_price_response(intent_request)
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    print("on_session_ended requestId=" + session_ended_request['requestId'] +", sessionId=" + session['sessionId'])

def get_stock_info_response():
	session_attributes = {}
    	card_title = "Welcome"
    	speech_output = "Welcome to the Stock Master. We can provide you with real time prices of stocks"
    	reprompt_text = speech_output
    	should_end_session = False
    	return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


def get_stock_price_response(intent_request):	
	session_attributes = {}
    	card_title = "Stock Master"
    	speech_output = ""
	stock = intent_request['intent']['slots']['stocks']['value']
	if stock == "apple":
		stock_price = get_stock_price('AAPL')
		speech_output = "The price of Apple is "+str(stock_price)
	else:
	    speech_output = "We cannot find what you are looking for,please try again."
	reprompt_text = speech_output
   	should_end_session = False
    	return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))	

def get_stock_price(stock_code):
	stock = Stock(stock_code)
	return stock.get_latest_price().LastTradePriceOnly

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
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
