from django.db import models
from django.contrib.auth.models import User

class UserPoints(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    points = models.BigIntegerField('Points',default=0)

    class Meta:
        verbose_name = 'Point'
        verbose_name_plural = 'Points'
    
    def __str__(self):
        return f'{self.user.username} - {self.points}'