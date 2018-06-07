from django.conf.urls import url, include
from rest_framework import routers

from todo.views import TodoTaskView, ActionView

router = routers.DefaultRouter()

router.register(r'^todo/tasks', TodoTaskView)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^todo/action', ActionView.as_view()),

]