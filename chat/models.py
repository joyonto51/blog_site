import uuid

from django.core.exceptions import ValidationError
from django.db import models

from accounts.models import User


def validate_message_content(content):
    if content is None or content == "" or content.isspace():
        raise ValidationError(
            'Content is empty/invalid',
            code='invalid',
            params={'content': content},
        )

class MessageManager(models.Manager):

    def last_50_messages(self):
        return self.get_queryset().order_by('-created_at')[:50]

class Message(models.Model):
    # id = models.UUIDField(primary_key=True, null=False, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, blank=False, null=False, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, blank=False, null=False, related_name='received_messages', on_delete=models.CASCADE)

    content = models.TextField(validators=[validate_message_content])
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    objects = MessageManager()

    def __str__(self):
        return self.sender.full_name
