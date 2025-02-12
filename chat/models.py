from django.db import models
from core.models import TradeRequest, User
# Create your models here.

class Message(models.Model):
    trade_request = models.ForeignKey(TradeRequest, related_name = "messages",
    on_delete = models.SET_NULL, null = True)
    sender = models.ForeignKey(
        User,
        related_name = "sender",
        on_delete = models.CASCADE
    )
    receiver = models.ForeignKey(
        User,
        related_name = "receiver",
        on_delete = models.CASCADE
    )
    text = models.TextField()
    created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.sender.username + '->' + self.receiver.username + ': ' + self.text