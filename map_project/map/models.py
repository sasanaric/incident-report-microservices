from django.contrib.gis.db import models

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super(SoftDeleteManager, self).get_queryset().filter(deleted=False)

class SoftDeleteObject(models.Model):
    deleted = models.BooleanField(default=False)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.save()

    def undelete(self):
        self.deleted = False
        self.save()

    class Meta:
        abstract = True

class Location(SoftDeleteObject, models.Model):
    coordinates = models.PointField()

    def __str__(self):
        return self.id
