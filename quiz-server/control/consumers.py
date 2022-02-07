# control/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import *
from django.db.models import Count

class ControlConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.name_group = 'consumer_control'
        self.player_group = 'consumer_player'

        await self.channel_layer.group_add(
            self.name_group,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.name_group,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, message_data):
        message_data_json = json.loads(message_data)
        message_type = message_data_json['type']

        if (message_type == "livePlayerStats"):
            
            live_viewers = message_data_json['liveViewers']
            alive_players = message_data_json['alivePlayers']
            total_players = message_data_json['totalPlayers']
            
            await self.channel_layer.group_send(
                self.player_group,
                {
                    'type' : "livePlayerStats",
                    'alivePlayers' : alive_players,
                    'liveViewers' : live_viewers,
                    'totalPlayers' : total_players
                }
            )
            
        elif (message_type == "nextQuestion"):
            
            question_id = message_data_json['questionId']

        elif (message_type == "showQuestionResult"):
            
            question_id = message_data_json['questionId']

        elif (message_type == "showBoard"):
            user_correct_votes = Vote.objects.filter(answer_option__question__game__is_active=True, answer_option__is_correct=True).values('user').annotate(Count())
            
        
        elif (message_type == "endRequest"):
            
            await self.channel_layer.group_send(
                self.player_group,
                {
                    'type' : "endGame"
                }
            )
        
        elif (message_type == "start"):
            
            await self.channel_layer.group_send(
                self.player_group,
                {
                    'type' : "start"
                }
            )



        
    async def vote(self, event):
        answer_option_id = event['answerOptionId']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': "newVote",
            'answerOptionId' : answer_option_id
        }))