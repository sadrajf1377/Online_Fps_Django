import random

from asgiref.sync import async_to_sync

online_users={}
current_rooms={}
group_alives={}
group_stats={}
squads={}

def join_leave_squad(sq_name,username,join_leave='join'):

    if join_leave == 'join':
        if sq_name in squads:
            squads[sq_name].append(username)
        else:
            squads[sq_name]=[username]


    elif join_leave == 'leave':
        if sq_name in squads and  username in squads[sq_name]:
           squads[sq_name].remove(username)


def Update_User_Json(Json,username,group_name):
    group_stats[group_name][username]=Json


def Get_Group_Json(group_name):
    data=group_stats[group_name]
    return data
def Check_If_Online(username):
    result=username in online_users
    return result

def Add_Or_Remove_Online_User(username,to_do,channel_name=None):
    if to_do == 'add':
        online_users[username]=channel_name
    elif to_do == 'remove':
        del online_users[username]


def Add_Or_Remove_From_Room(group_name,to_do,username,color=None):
    if to_do == 'add':
        start=False
        if group_name in current_rooms:
          if username in current_rooms[group_name]:
              print('return was called for me',username,current_rooms)
              return

        if not color:

                ran=random.randint(0,1)
                print(ran)
                try:
                        red_count=len([x for x in current_rooms[group_name] if current_rooms[group_name][x] == 'red'])
                        blue_count=len([x for x in current_rooms[group_name] if current_rooms[group_name][x] == 'blue'])
                        room_exists=True

                except:
                         red_count=0
                         blue_count=0
                         room_exists = False
                if ran ==0:
                        color='red' if red_count<3 else 'blue'
                else:
                        color='blue' if blue_count<3 else 'red'
                if  room_exists:
                        current_rooms[group_name].update({username:color})
                        group_stats[group_name][username]=''

                else:
                     current_rooms[group_name]={}
                     current_rooms[group_name].update({username:color})
                     group_stats[group_name]={}
                     group_stats[group_name][username] = ''
                     print(current_rooms[group_name])
                try:
                     group_alives[group_name]={}
                     group_alives[group_name][color]=1
                except:
                     group_alives[group_name][color] += 1

        else:
             current_rooms[group_name].update({username:color})
        if len(current_rooms[group_name].keys())>=2:
            #async_to_sync(online_users[username].group_send)(group_name,({'type':'start_game'}))
            start=True
        return start
    elif to_do == 'remove':
           #color = current_rooms[group_name][username]
           del current_rooms[group_name][username]

           #group_alives[group_name][color] -= 1


def Get_Group_Users(group_name):
    result=current_rooms[group_name]
    return result
def Get_user_channel(username):
    channel=online_users[username]

    return channel
def check_deads(Group_Name,username):
    Color=current_rooms[Group_Name][username]
    group_alives[Group_Name][Color]-=1



def whats_my_color(username,group_name):
    return current_rooms[group_name][username]