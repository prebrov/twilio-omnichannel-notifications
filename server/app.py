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
TWILIO_NUMBER = os.getenv('TWILIO_NUMBER')
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')
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
    # Construct data to send
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


# Submit notifications
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
