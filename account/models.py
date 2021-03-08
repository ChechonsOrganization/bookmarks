from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

# Create your models here.
class Profile(models.Model):
    """ 
        Extends the user model with additional fields and a
        one-to-one relationship with the django user model.
        one to one is similar to FK field with the parameter
        unique=True.

        You will need to instlal the Pillow library to handle images.
        pip install Pillow.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self):
        return f'Profile for user {self.user.username}'


class Contact(models.Model):
    """
    Contact model that you will use for user relationships.
    user_from: A Foreignkey for the user who creates the relationship
    user_to: A ForeignKey for the user being followed
    created: A DateTimeField with auto_now_add=True to store the
    time when the relationship was created
    """
    user_from = models.ForeignKey('auth.User', related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey('auth.User', related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}' 


# Add following field to User dynamically
user_model = get_user_model()
user_model.add_to_class('following',
                        models.ManyToManyField('self',
                        through=Contact,
                        related_name='followers',
                        symmetrical=False))