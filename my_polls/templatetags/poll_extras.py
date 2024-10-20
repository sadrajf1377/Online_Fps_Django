
from user_moudle.models import User_Friends_List,Friends_List
from django import template

register = template.Library()

@register.filter
def get_friends_list(user,output):
    friends_list, ff = User_Friends_List.objects.get_or_create(parent_user_id=user.id)
    if friends_list.user_list == None:
        fr_list = Friends_List.objects.create()
        friends_list.user_list = fr_list
        friends_list.save()
    else:
        fr_list = friends_list.user_list
    names = fr_list.users.all()
    if output == 'count':
        names=names.count()
    elif output =='list':
        names=names
    return names
