from rest_framework.serializers import Serializer, ModelSerializer
from user_moudle.models import custom_user

class User_Serializer(ModelSerializer):
    class Meta:
        model=custom_user
        fields=['username','user_ranking','user_total_score','kill_per_death','get_friends_list','account_balance']


