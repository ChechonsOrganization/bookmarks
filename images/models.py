from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.

class Image(models.Model):
    """ 
    This is the models that you will use to store images retrieved from diffrerent sites.

    User: This indicates the User object that bookmarked this image.
    This is a foreign key field because it specifies a one to many relationship:
    a user can post multiple images, but each image is post by a single user.
    you use CASCADE for the on_delete paramter so thar related images are also deleted when a user is deleted

    Title: a title for the image
    
    Slug: a short label that contains only letters, numbers , underscores or hyphens to be used for building beautiful SEO-friendly URLS
    
    URL : the original url for this Image
    
    image: the image file
    
    description: an optional description for the image
    
    created: the date and time that indicate when the object was created in the database.
    Since you use auto_now_add, this datetime is automatically set when the object is created, you use  db_index=True
    so that django creates an index in the database for this field

    users_like: field to store the users who loke an image. many to many relatioship in this case because
    a user might like multiple images and each emage can be liked by multiple users.

    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            related_name='images_created',
                            on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField()
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True, db_index=True)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='images_liked', blank=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        If the user don't write something in the slug, 
        this will do it automatically.
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """ 
        Remember that the common pattern for providing canonical URLs for
        objects is to define a get_absolute_url() method in the model.
        """
        return reverse('images:detail', args=[self.id, self.slug])
    
