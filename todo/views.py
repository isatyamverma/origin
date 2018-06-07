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


class TodoTaskView(viewsets.ModelViewSet):
    queryset = Task.objects.exclude(status='DELETED')
    serializer_class = TaskSerializer
    # permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        owner = self.request.user
        owner = User.objects.all()[0]
        serializer.save(owner=owner)

    def perform_destroy(self, instance):
        instance.status = 'DELETED'
        instance.save()

class ActionView(APIView):
    # permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        actor = request.user
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


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
