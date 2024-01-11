from django.db import models
from django.contrib.auth.models import User
from django.db import models

class Status(models.Model):
    """
    Represents the status of a task for a specific user.

    Fields:
    - user: ForeignKey to the User model representing the owner of the status.
    - name: CharField representing the name of the status.

    Meta:
    - verbose_name_plural: Display name for the model in the Django admin.

    Methods:
    - __str__(): Returns the string representation of the status, which is its name.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Statuses'

    def __str__(self):
        """
        Returns the string representation of the status, which is its name.

        Returns:
        - String: The name of the status.
        """
        return self.name

class Priority(models.Model):
    """
    Represents the priority of a task for a specific user.

    Fields:
    - user: ForeignKey to the User model representing the owner of the priority.
    - name: CharField representing the name of the priority.

    Meta:
    - verbose_name_plural: Display name for the model in the Django admin.

    Methods:
    - __str__(): Returns the string representation of the priority, which is its name.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Priorities'

    def __str__(self):
        """
        Returns the string representation of the priority, which is its name.

        Returns:
        - String: The name of the priority.
        """
        return self.name

class Task(models.Model):
    """
    Represents a task assigned to a user.

    Fields:
    - user: ForeignKey to the User model representing the owner of the task.
    - title: CharField representing the title of the task.
    - description: TextField representing the optional description of the task.
    - created_at: DateField representing the date when the task was created.
    - due_date: DateField representing the due date of the task.
    - status: ForeignKey to the Status model representing the status of the task.
    - assignee: ForeignKey to the User model representing the user assigned to the task.
    - priority: ForeignKey to the Priority model representing the priority of the task.
    - completed: BooleanField indicating whether the task is completed.
    - completed_at: DateField representing the date when the task was completed (if completed).
    - tags: ManyToManyField to the Tag model representing tags associated with the task.

    Methods:
    - __str__(): Returns the string representation of the task, which is its title.
    """
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
        """
        Returns the string representation of the task, which is its title.

        Returns:
        - String: The title of the task.
        """
        return self.title

class Comment(models.Model):
    """
    Represents a comment on a task.

    Fields:
    - task: ForeignKey to the Task model representing the task the comment belongs to.
    - author: ForeignKey to the User model representing the author of the comment.
    - content: TextField representing the content of the comment.
    - created_at: DateTimeField representing the date and time when the comment was created.

    Methods:
    - __str__(): Returns the string representation of the comment, including the author's username
                 and the title of the associated task.
    """
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns the string representation of the comment.

        Returns:
        - String: A formatted string including the author's username and the title of the associated task.
        """
        return f"Comment by {self.author.username} on {self.task.title}"

class Tag(models.Model):
    """
    Represents a tag associated with a user.

    Fields:
    - name: CharField representing the name of the tag.
    - user: ForeignKey to the User model representing the user associated with the tag.

    Methods:
    - __str__(): Returns the string representation of the tag, which is its name.
    """
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """
        Returns the string representation of the tag.

        Returns:
        - String: The name of the tag.
        """
        return self.name
