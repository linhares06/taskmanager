from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from django.contrib.auth.models import User
from .models import Status, Priority, Tag

@receiver(post_save, sender=User)
def set_default_status(sender, instance, created, **kwargs):
    """
    Set default status choices for a new user upon creation.

    Args:
    - sender: The sender of the signal.
    - instance: The User instance being saved.
    - created: A boolean indicating whether the instance is being created.
    - **kwargs: Additional keyword arguments.

    Notes:
    - Creates default status entries ('To Do', 'In Progress', 'On Hold', 'Archived')
      for a newly created user.
    - If an exception occurs during the creation process, the user instance is deleted.

    Example:
    >>> @receiver(post_save, sender=User)
    >>> def my_callback(sender, instance, created, **kwargs):
    >>>     set_default_status(sender, instance, created, **kwargs)
    """
    if created:
        try:
            with transaction.atomic():
                #Task ready
                Status.objects.create(user=instance, name='To Do')
                #The assigned user or team is actively working on the task
                Status.objects.create(user=instance, name='In Progress')
                #The task is temporarily paused or on hold due to some reason.
                Status.objects.create(user=instance, name='On Hold')
                #The task has been archived and is no longer active.
                Status.objects.create(user=instance, name='Archived')
        except Exception as e:
            instance.delete()

@receiver(post_save, sender=User)
def set_default_priority(sender, instance, created, **kwargs):
    """
    Set default priority choices for a new user upon creation.

    Args:
    - sender: The sender of the signal.
    - instance: The User instance being saved.
    - created: A boolean indicating whether the instance is being created.
    - **kwargs: Additional keyword arguments.

    Notes:
    - Creates default priority entries ('Low', 'Medium', 'High') for a newly created user.
    - If an exception occurs during the creation process, the user instance is deleted.

    Example:
    >>> @receiver(post_save, sender=User)
    >>> def my_callback(sender, instance, created, **kwargs):
    >>>     set_default_priority(sender, instance, created, **kwargs)
    """
    if created:
        try:
            with transaction.atomic():
                Priority.objects.create(user=instance, name='Low')
                Priority.objects.create(user=instance, name='Medium')
                Priority.objects.create(user=instance, name='High')
        except Exception as e:
            instance.delete()

@receiver(post_save, sender=User)
def set_default_tag(sender, instance, created, **kwargs):
    """
    Set default tag choices for a new user upon creation.

    Args:
    - sender: The sender of the signal.
    - instance: The User instance being saved.
    - created: A boolean indicating whether the instance is being created.
    - **kwargs: Additional keyword arguments.

    Notes:
    - Creates a default tag entry ('Home Task') for a newly created user.
    - If an exception occurs during the creation process, the user instance is deleted.

    Example:
    >>> @receiver(post_save, sender=User)
    >>> def my_callback(sender, instance, created, **kwargs):
    >>>     set_default_tag(sender, instance, created, **kwargs)
    """
    if created:
        try:
            with transaction.atomic():
                Tag.objects.create(user=instance, name='Home Task')
        except Exception as e:
            instance.delete()