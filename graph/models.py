from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.template.defaultfilters import truncatewords


class Message(models.Model):
    id = models.CharField(max_length=40, primary_key=True)
    updated_time = models.DateTimeField()
    from_data = JSONField(null=True)
    to_data = JSONField()
    message = models.TextField()
    unread = models.IntegerField()
    unseen = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        message = truncatewords(self.message, 10)
        return '%s: %s (%s - %s)' % (self.user, message, self.updated_time, self.id)


class Post(models.Model):
    id = models.CharField(max_length=40, primary_key=True)
    created_time = models.DateTimeField()
    story = models.TextField()
    message = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def has_attachment(self):
        return self.attachment is not None

    def __str__(self):
        message = truncatewords(self.message, 10)
        return '%s: %s (%s - %s)' % (self.user, message, self.created_time, self.id)


class Attachment(models.Model):
    post = models.OneToOneField(Post)
    url = models.TextField()
    title = models.TextField()
    type = models.CharField(max_length=40)
    description = models.TextField()
    media = JSONField(null=True, blank=True)
    target = JSONField(null=True, blank=True)
    description_tags = JSONField(null=True, blank=True)
    subattachments = JSONField(null=True, blank=True)

    class Meta:
        unique_together = ('post', 'title')

    def __str__(self):
        title = truncatewords(self.title, 10)
        return '%s: %s (%s)' % (self.post.user, title, self.url)


class Comment(models.Model):
    post = models.ForeignKey(Post)
    # Only set for comments on comments
    comment = models.ForeignKey("Comment", null=True, blank=True, related_name='comment_set')
    id = models.TextField(primary_key=True)
    from_json = JSONField()
    created_time = models.DateTimeField()
    message = models.TextField()

    def __str__(self):
        message = truncatewords(self.message, 10)
        return '%s: %s (%s - %s)' % (self.post.user, message, self.created_time, self.id)
