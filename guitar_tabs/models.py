from django.db import models
from accounts.models import User
from .validators import validate_tab_extension


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return '/'.join([instance.user.nick, filename])


class GuitarTab(models.Model):
    tab_text = models.TextField()
    tab_file = models.FileField(upload_to=user_directory_path, validators=[validate_tab_extension])
    band = models.CharField(max_length=200)
    song = models.CharField(max_length=200)
    link = models.CharField(max_length=400)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.song


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tab = models.ForeignKey(GuitarTab, on_delete=models.CASCADE)
    message = models.TextField()
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.tab.song
