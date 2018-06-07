# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from todo import models as todo_models

admin.site.register(todo_models.Task)
admin.site.register(todo_models.Action)