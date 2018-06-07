from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from todo.models import Task, Action


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()

    def get_owner(self, instance):
        username = instance.owner.username
        user_id = instance.owner.id
        return {'id': user_id, 'name': username}

    class Meta:
        model = Task
        fields = ('id', 'owner', 'name', 'status', 'description', 'created_at')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email')

    def validate_password(self, password):
        return make_password(password)


class ActionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Action
        fields = ('id', 'task', 'actor', 'action', 'created_at')