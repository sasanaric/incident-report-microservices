from django.db import models
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
# Create your models here.

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


class Type(SoftDeleteObject,models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

class Incident(SoftDeleteObject,models.Model):
    description = models.TextField(blank=True, null=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, null=True)
    location_id = models.IntegerField(null=True)
    image_url = models.URLField(blank=True, null=True)
    approved = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True, null=True)
    cluster_label = models.IntegerField(null=True, blank=True)


    def __str__(self):
        return f"Incident #{self.id}: {self.type}"
