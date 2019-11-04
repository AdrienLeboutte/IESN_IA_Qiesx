from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.


class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    board = models.CharField(max_length=50, null=True)
    size_x = models.IntegerField(default=8)
    size_y = models.IntegerField(default=8)
    game_state = models.IntegerField(default=0)
    player_1 = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="player_1")
    player_2 = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="player_2")
