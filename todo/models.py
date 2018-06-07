# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import fields
from django.contrib.auth.models import User
from django.utils import timezone

'''
Abstract model to populate created_by and last_updated_by for other models.
'''
class ModelBase(models.Model):
    created_at = fields.DateTimeField(editable=False)
    last_updated_at = fields.DateTimeField(editable=False)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        if not self.id:
            self.created_at = timezone.now()

        self.last_updated_at = timezone.now()
        super(ModelBase, self).save(force_insert, force_update, using,
                                    update_fields)

    class Meta:
        abstract = True

'''
Inherits ModelBase.
All task and their current status are stored here.
'''
class Task(ModelBase):
    STATUS_LIST = [('DONE', 'DONE'), ('NOTDONE', 'NOTDONE'), ('DELETED', 'DELETED')]

    owner = models.ForeignKey(User)
    name = fields.CharField(max_length=127)
    status = fields.CharField(max_length=127, choices=STATUS_LIST, default=STATUS_LIST[1][0])
    description = fields.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name

'''
Inherits ModelBase.
Any action performed on a task is recorded.
'''
class Action(ModelBase):
    action_list = [('MARKDONE', 'MARKDONE'), ('MARKNOTDONE', 'MARKNOTDONE')]

    task = models.ForeignKey(Task)
    actor = models.ForeignKey(User)
    action = fields.CharField(max_length=127, choices=action_list)


@receiver(post_save, sender=Action)
def create_component_group_link(sender, instance, created, **kwargs):
    if created:
        affected_task = instance.task
        affected_task.status='DONE'
        affected_task.save()