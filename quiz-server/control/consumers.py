# control/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import *
from django.db.models import Count
from django.core import serializers

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
            answers_json = serializers.serialize("json",Answer_option.objects.filter(question__id=question_id), fields=("id", "answer_option_text"))
            question_text = Question.objects.filter(id=question_id)

            await self.channel_layer.group_send(
                self.player_group,
                {
                    'type' : "question",
                    'question' : {
                        'questionId' : question_id,
                        'questionText' : question_text,
                        'answerOptions' : answers_json
                    }
                }
            )

        elif (message_type == "hide"):
            await self.channel_layer.group_send(
                self.player_group,
                {
                    'type' : "hide"
                }
            )

        elif (message_type == "showQuestionResult"):
            
            question_id = message_data_json['questionId']
            answers = Answer_option.objects.filter(question__id=question_id).values("id", "is_correct")
            question_text = Question.objects.filter(id=question_id) 
            answers_list = list(answers)
            json_list_dict = []
            fields=['answerOptionId', 'isCorrect', 'AnswerOptionVotes']
            for a in answers_list:
                numVotos = Vote.objects.filter(answer_option__id=a[0]).count()
                a.append(numVotos)
                json_list_dict.append(dict(zip(fields,a)))

            await self.channel_layer.group_send(
                self.player_group,
                {
                    'type' : "questionResult",
                    'answerOptions' : json_list_dict
                }
            )
            
            



        elif (message_type == "actualScoreBoard"):
            user_correct_votes = User.objects.filter(vote_set__answer_option__question__game__is_active=True, vote_set__answer_option__is_correct=True).values('user').annotate(Count())

        
        elif (message_type == "generalScoreBoard"):
            user_correct_votes = User.objects.filter(vote_set__answer_option__question__game__is_active=True, vote_set__answer_option__is_correct=True).values('user').annotate(Count())
            
        
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