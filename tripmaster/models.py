from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class TripDb(models.Model):
  title = models.CharField(max_length = 100)
  start_date = models.DateField()
  destination = models.CharField(max_length = 100)
  created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name= 'created_trips')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now = True)

  def __str__(self):
    return self.title


  

class TripMemberDb(models.Model):
  trip = models.ForeignKey(TripDb, on_delete=models.CASCADE, related_name='trip_members')
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_trips')
  joined_date = models.DateTimeField(auto_now_add=True)

  class Meta:
    constraints = [
      models.UniqueConstraint(fields=['trip','user'], name='unique_trip_member')
    ]  


# this means the combination of trip and user must be unique
# it does not mean that trip alone or user alone must be unique. A user can joinn multiple trips,
# and a trip can have multiple users, but the same user cannot join the same trip more than once

  def __str__(self):
    return f"{self.user.username} - {self.trip.title}"
