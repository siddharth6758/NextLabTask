from django.db import models
from django.contrib.auth.models import User
from user_profile.models import UserPoints

class Category(models.Model):
    category = models.CharField('Category', max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return f'{self.category}'

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    sub_category = models.CharField('Sub Category', max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'SubCategory'
        verbose_name_plural = 'SubCategories'
    
    def __str__(self):
        return f'{self.sub_category}'

class Apps(models.Model):
    name = models.CharField('App Name', max_length=255, null=True, blank=True)
    app_logo = models.ImageField('App Logo', upload_to='app_logos/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True)
    points = models.BigIntegerField('Points',default=0)

    class Meta:
        verbose_name = 'App'
        verbose_name_plural = 'Apps'
    
    def __str__(self):
        return f'{self.name} - {self.points}'


class UserAppInstall(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    app = models.ForeignKey(Apps, on_delete=models.CASCADE, null=True, blank=True)
    screenshot = models.ImageField('Proof', upload_to='screenshots/', null=True, blank=True)

    class Meta:
        verbose_name = 'Apps Install'
        verbose_name_plural = 'Apps Install'
    
    def __str__(self):
        return f'{self.user.username} - {self.app.name}'

    def save(self, *args, **kwargs):
        user = self.user
        points = self.app.points
        userpoints = UserPoints.objects.filter(user=user)
        if userpoints.exists():
            userpoint_obj = userpoints.first()
            userpoint_obj.points += points
            userpoint_obj.save()
        else:
            UserPoints.objects.create(
                user=user,
                points=points
            )
        super(UserAppInstall, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        user = self.user
        points = self.app.points
        userpoints = UserPoints.objects.filter(user=user)
        if userpoints.exists():
            userpoint_obj = userpoints.first()
            userpoint_obj.points -= points
            userpoint_obj.save()
        super(UserAppInstall, self).delete(*args, **kwargs)