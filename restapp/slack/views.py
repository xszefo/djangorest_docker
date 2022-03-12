from django.shortcuts import render
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from datetime import datetime

import subprocess
import random
import os

# Create your views here.
class Events(APIView):
    def post(self, request, *args, **kwargs):
        SLACK_VERIFICATION_TOKEN = settings.ENV('SLACK_VERIFICATION_TOKEN')
        SLACK_BOT_USER_TOKEN = os.environ['SLACK_BOT_USER_TOKEN']
        slack_message = request.data
        
        GREETINGS = ['hi', 'hello', "what's up"]

        if slack_message.get('token') != SLACK_VERIFICATION_TOKEN:
            #print "Error! Wrong token\nOur: {}\nReceived: {}\n".format(SLACK_VERIFICATION_TOKEN, slack_message.get('token'))
            print("Error! Wrong token\nOur: {}\nReceived: {}\n".format(SLACK_VERIFICATION_TOKEN, slack_message.get('token')))
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        # verification challenge
        if slack_message.get('type') == 'url_verification':
            return Response(data=slack_message, status=status.HTTP_200_OK)
        
        client = WebClient(token=SLACK_BOT_USER_TOKEN)

        # greet bot
        if 'event' in slack_message:
            event_message = slack_message.get('event')

            # process user's message
            user = event_message.get('user')                      
            text = event_message.get('text')                      
            channel = event_message.get('channel')       

            print(f'''
            New message
            Time: {datetime.now()}
            User: {user}
            Text: {text}
            Channel: {channel}
            ''')
            # ignore bot's own message
            if event_message.get('subtype') == 'bot_message' or user == 'UU7ERFFNW': 
                return Response(status=status.HTTP_200_OK)        

            if any([True for message in GREETINGS if text.lower() in message]):                              
                greeting = random.choice(GREETINGS)
                bot_text = '{} <@{}> :wave:'.format(greeting, user)           
                client.chat_postMessage(channel=channel, text=bot_text)                    
                return Response(status=status.HTTP_200_OK)
            elif 'uptime' in text.lower():
                bot_text = subprocess.check_output(['uptime'], shell=True)
                client.chat_postMessage(channel=channel, text=bot_text)                    
                return Response(status=status.HTTP_200_OK)
            elif '@UU7ERFFNW' in text:
                client.chat_postMessage(channel=channel, text='<@UU7ERFFNW> at your service, how can I help?')                    
                return Response(status=status.HTTP_200_OK)
            
            #else:
            #    bot_text = '{}? Ale o co kaman?'.format(text)
            #    client.chat_postMessage(method='chat.postMessage', channel=channel, text=bot_text)                    
            #    return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_200_OK)
