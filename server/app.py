#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

# Load .env file and overwrite existing environment vars if they exist
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

# Your Account Sid and Auth Token from twilio.com/console
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
# Twilio number to send SMS from and make calls from (CallerId and SenderId).
# Purchase a number that supports both SMS and Voice from https://www.twilio.com/console/phone-numbers/search
TWILIO_NUMBER = os.getenv('TWILIO_NUMBER')
# Number to send WhatsApp messages from.
# For WhatsApp Sandbox use +14155238886. To receive messages, recipent must join Sandbox as instructed on https://www.twilio.com/console/sms/whatsapp/learn
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')
# Twilio Studio Flow Sid from https://www.twilio.com/console/studio/dashboard
TWILIO_FLOW_SID = os.getenv('TWILIO_FLOW_SID')

# Construct a Flow REST API URL
flowRestUrl = 'https://studio.twilio.com/v1/Flows/' + TWILIO_FLOW_SID + '/Engagements'

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)


def outbound_studio_flow(to_sms,
                         to_voice,
                         to_whatsapp,
                         to_email,
                         message_body):
    """Send a Twilio Studio POST request.

    Keyword arguments:
    to_sms -- phone number to send SMS to (E.164) 
    to_voice -- phone number to place voice call to (E.164)
    to_whatsapp -- phone number to send WhatsApp to (E.164)
    to_email -- email address to send email to (E.164)
    message_body -- message body (will be spoken out as text-to-speech when placing voice call)
    """
    data = {
        'To': to_voice,
        'From': TWILIO_NUMBER,
        'Parameters': json.dumps({
            'sms': to_sms,
            'voice': to_voice,
            'email': to_email,
            'whatsapp': to_whatsapp,
            'whatsapp_from': TWILIO_WHATSAPP_NUMBER,
            'body': message_body,
        })
    }
    # Make a POST request
    try:
        flowResponse = requests.post(url=flowRestUrl,
                                     auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN),
                                     data=data,
                                     verify=True)

        # Output response status code and body
        print(f"Studio Response Code: {flowResponse.status_code}")
        print(f"Studio Response Body: {flowResponse.content}")

    # Catch exception
    except requests.exceptions.RequestException:
            print("HTTP Request failed")


# HTTP endpoint to submit notification to
@app.route('/notifications', methods=['POST'])
def notify():
    response_object = {'status': 'success'}
    post_data = request.get_json()

    print(f"body: {post_data.get('body')}")

    outbound_studio_flow(to_sms=post_data.get('sms'),
                         to_voice=post_data.get('voice'),
                         to_whatsapp=post_data.get('whatsapp'),
                         to_email=post_data.get('email'),
                         message_body=post_data.get('body'))

    response_object['message'] = 'Message sent'

    return jsonify(response_object)


if __name__ == '__main__':
    app.run()
