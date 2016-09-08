from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.template.defaultfilters import truncatewords


class Post(models.Model):
    id = models.CharField(max_length=40, primary_key=True)
    created_time = models.DateTimeField()
    story = models.TextField()
    message = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        message = truncatewords(self.message, 10)
        return '%s: %s (%s - %s)' % (self.user, message, self.created_time, self.id)


class Comment(models.Model):
    post = models.ForeignKey(Post)
    id = models.CharField(max_length=80, primary_key=True)
    from_json = JSONField()
    created_time = models.DateTimeField()
    message = models.TextField()

    def __str__(self):
        message = truncatewords(self.message, 10)
        return '%s: %s (%s - %s)' % (self.post.user, message, self.created_time, self.id)
