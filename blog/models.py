from django.db import models


class TagModel(models.Model):
    title = models.CharField(max_length=20, null=False)

    def __str__(self):
        return 'models.TagModel(%s)' % self.title


class Categories(models.Model):
    title = models.CharField(max_length=40, null=False)

    def __str__(self):
        return 'models.Categories(%s)' % self.title


class Entries(models.Model):
    title = models.CharField(max_length=80, null=False)
    content = models.TextField(null=False)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    category = models.ForeignKey(Categories)
    tags = models.ManyToManyField(TagModel)
    comment_num = models.PositiveSmallIntegerField(default=0, null=True)
    IMAGE_DIR = 'sandbox/entry-images'
    image = models.ImageField(upload_to=IMAGE_DIR, null=True, blank=True)


class Comments(models.Model):
    name = models.CharField(max_length=20, null=False)
    password = models.CharField(max_length=32, null=False)
    content = models.TextField(max_length=2000, null=False)
    created = models.DateTimeField(auto_now_add=True, auto_now=True)
    entry = models.ForeignKey(Entries)
