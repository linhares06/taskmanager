from django.db import models
from django.contrib.auth.models import User
from django.db import models

class Status(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Statuses'

    def __str__(self):
        return self.name

class Priority(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Priorities'

    def __str__(self):
        return self.name

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignee')
    priority = models.ForeignKey(Priority, on_delete=models.PROTECT)
    completed = models.BooleanField(default=False)
    completed_at = models.DateField(null=True, blank=True)
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title

class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.task.title}"

class Tag(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
