# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from serializers import TaskSerializer
from todo.models import Task, Action
from todo.resources import IsOwnerOrReadOnly
from todo.serializers import ActionSerializer, UserSerializer

#TODO User is hardcoded and permissions are commented as login is not implemented completely yet

'''
All Task CRUD api are handled here.
'''
class TodoTaskView(viewsets.ModelViewSet):
    #We do not delete any task. So filter tasks that are deleted for user.
    queryset = Task.objects.exclude(status='DELETED')
    serializer_class = TaskSerializer
    # permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    '''
    It takes request user as owner of task. **User is hardcoded as login not completed.**
    '''
    def perform_create(self, serializer):
        owner = self.request.user
        owner = User.objects.all()[0]
        serializer.save(owner=owner)

    '''
    Delete just updates status field as DELETE.
    **We are not deleting any data as data is precious. Also people ask for old data backup many times.
    '''
    def perform_destroy(self, instance):
        instance.status = 'DELETED'
        instance.save()

'''
This handles task done action as a post api
'''
class ActionView(APIView):
    # permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        actor = request.user
        #User hardcoded as login not implemented yet
        actor  = User.objects.all()[0].id
        task_id = request.data['task']

        action_data = {'actor':actor,
                       'task':task_id,
                       'action':'MARKDONE'}

        serializer = ActionSerializer(data=action_data)

        if serializer.is_valid():
            serializer.save()

            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


'''
This will be used once login is implemented for user CRUD operations.
'''
class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
