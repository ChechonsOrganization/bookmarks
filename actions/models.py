from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
class Action(models.Model):
    user = models.ForeignKey('auth.User',
                            related_name='actions',
                            db_index=True,
                            on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)
    """
        target_ct: A ForeignKey field that points to the ContentType model
        target_id: A PositiveIntegerField for storing the primary key of the related object
        target: A GenericForeignKey field to the related object based on the combination of the
        two previous fields

        Django does not create any field in the db for GenericForeignKey fields.
        the only fields that are mapped to db fields are target_ct and target_id.
        Both fields have blank=True and null=True attributes, so that a target object
        is not required when saving Actions objects.

        YOU CAN MAKE YOUR APPS MORE FLEXIBLE BY USING GENERIC RELATIONS INSTEAD OF FOREIGN KEYS    
    """
    target_ct = models.ForeignKey(ContentType,
                                 blank=True,
                                 null=True,
                                 related_name='target_obj',
                                 on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField(null=True,
                                            blank=True,
                                            db_index=True)
    target = GenericForeignKey('target_ct', 'target_id')
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

