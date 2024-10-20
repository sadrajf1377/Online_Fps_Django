import json
from time import sleep

from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from psycopg2._json import Json
from user_moudle.models import User_Sessions
from utils.my_functions import Add_Or_Remove_Online_User,Check_If_Online,Add_Or_Remove_From_Room,Get_Group_Users,Get_user_channel,check_deads,Update_User_Json
from utils.my_functions import Get_Group_Json,online_users,join_leave_squad,squads,whats_my_color,current_rooms
from user_moudle.models import custom_user
class Private_Socket(WebsocketConsumer):
     def connect(self):
        self.squad_name=None
        self.accept()

     def disconnect(self, code):
         Add_Or_Remove_Online_User(self.username, 'remove')
         join_leave_squad(self.squad_name,self.username,'leave')
         self.accept()
     def receive(self, text_data=None, bytes_data=None):
         json_resp=json.loads(text_data)
         function_type=json_resp['func_type']
         func=self.__getattribute__(function_type)
         func(json_resp)

     def invite(self,data):
         target=data['target']
         data['type']='receive_invite'
         data['squad_name']=self.username
         join_leave_squad(self.username,self.username,'join')
         self.squad_name=self.username
         async_to_sync(self.channel_layer.send)(online_users[target],data)


     def receive_invite(self,event):
         self.send(text_data=json.dumps({'function':'receive_invite','squad_name':event['squad_name'],
                                         'message':f'{event["squad_name"]} invited you to their party'}))

     def resolve_username(self,event_data):
         try:

           username=User_Sessions.objects.get(key=event_data['session_id']).user.username
           Add_Or_Remove_Online_User(username,'add',self.channel_name)
           self.username=username
         except:
             Add_Or_Remove_Online_User(username, 'remove', self.channel_name)
             self.disconnect()
     def join_squad(self,event):
         squad_name=event["squad_name"]

         join_leave_squad(squad_name,self.username,'join')
         self.squad_name=squad_name
         for user in squads[self.squad_name]:
             async_to_sync(self.channel_layer.send)(online_users[user],{'type':'update_squad_list'})


     def add_squad_to_room(self,event):
         if not self.username in squads:
             return

         room_name=event['room_name']

         Add_Or_Remove_From_Room(room_name, 'add', self.username)
         my_color = whats_my_color(self.username,room_name)

         for user in squads[self.username]:
                 Add_Or_Remove_From_Room(room_name, 'add', user, my_color)

         for user in squads[self.username]:
             async_to_sync(self.channel_layer.send)(online_users[user],({'type':'join_room','room_name':room_name}))
         del squads[self.username]


     def join_room(self,event):
         event['function']='join_room'
         print(self.username,'was joined room',event['room_name'])
         self.send(text_data=json.dumps(event))

     def update_squad_list(self,event):

         users=str(squads[self.squad_name])
         self.send(text_data=json.dumps({'function':'update_squad','users':users}))



class Room_Socket(WebsocketConsumer):
    def connect(self):
        self.room_name=self.scope["url_route"]["kwargs"]["room_name"]
        self.group_name="chat_%s" % self.room_name

        async_to_sync(self.channel_layer.group_add)(self.group_name,self.channel_name)

        self.accept()


    def receive(self, text_data=None, bytes_data=None):
        data=json.loads(text_data)
        func=self.__getattribute__(data['to_do'])
        func(data)
        
    def disconnect(self, code):
        Add_Or_Remove_From_Room(self.group_name, 'remove',self.username)

        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)

    def announce_joining(self,data):

        session_id = data['session_id']
        user = User_Sessions.objects.get(key=session_id).user
        self.username=user.username

        start=Add_Or_Remove_From_Room(self.group_name, 'add', self.username)
        data['type']='update_users_list'

        async_to_sync(self.channel_layer.group_send)(self.group_name, data)
        if start:
            async_to_sync(self.channel_layer.group_send)(self.group_name, {'type':'start_game'})

    def update_users_list(self,data):
        #print(json.dumps({'groups_users': Get_Group_Users(self.group_name)}))
        print('update users list was called for',self.username)
        self.send(text_data=json.dumps({'groups_users': Get_Group_Users(self.group_name)}))


    def send_stats(self,data):
        Update_User_Json(data,self.username,self.group_name)
        to_do={'type':'update_stats'}

        async_to_sync(self.channel_layer.send)(self.channel_name,to_do)
    def start_game(self,event):
        self.send(text_data=json.dumps({'function':'start_game'}))

    def die(self,event):
        print('update score was called for',event['username'])
        Add_Or_Remove_From_Room(self.group_name, 'remove', self.username)
        async_to_sync(self.channel_layer.group_send)(self.group_name,({'type':'update_score','username':event['username']}))

    def update_score(self,event):
        target=event['username']
        if target != self.username:
            return
        self.send(text_data=json.dumps({'function':'increase_my_score'}))

    def update_stats(self,data):
        #print(f'{data["username"]} asked for data update and mine is {self.username}')

        self.send(text_data=json.dumps(Get_Group_Json(self.group_name)))


class Web_Consumer(WebsocketConsumer):
    def connect(self):

        Add_Or_Remove_Online_User(self.scope['user'].username,'add',self.channel_name)
        self.accept()
    def disconnect(self, code):

        Add_Or_Remove_Online_User(self.scope['user'].username, 'remove', self.channel_name)
        self.accept()
    def receive(self, text_data=None, bytes_data=None):

        decoded_data=json.loads(text_data)
        func=self.__getattribute__(decoded_data['to_do'])
        func(decoded_data)
    def send_notif(self,data):
        target_user=Get_user_channel(data['target_user'])

        async_to_sync(self.channel_layer.send)(target_user,({'type':'recieve_notif','message':f'{self.scope["user"].username} sent you a friend request'}))
    def recieve_notif(self,data):

        self.send(text_data=json.dumps(data))

class Group_Socket(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.group_name = "chat_%s" % self.room_name
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.accept()
    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)
        self.accept()
    def receive(self, text_data=None, bytes_data=None):
        encoded=json.loads(text_data)
        func=self.__getattribute__(encoded['to_do'])
        func(encoded)
    def send_message(self,data):
        data['type']='receive_message'
        async_to_sync(self.channel_layer.group_send)(self.group_name,data)
    def receive_message(self,data):
        data['function']='add_message'
        self.send(json.dumps(data))



