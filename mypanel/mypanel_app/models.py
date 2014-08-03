from django.db import models

# Create your models here.
class Event(models.Model):
    
    name = models.CharField(max_length=50)
    time = models.CharField(max_length=100)
    event_id = models.AutoField(primary_key=True)

    def __unicode__(self):
        return self.name


