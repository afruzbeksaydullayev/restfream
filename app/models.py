from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    slug = models.SlugField( blank=True)
    group = models.ForeignKey('Group', on_delete=models.CASCADE, related_name='products')
    is_liked = models.ManyToManyField(User, related_name='liked_products', blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField( blank=True)
    image = models.ImageField(upload_to='media/images/category/')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'

class Group(models.Model):
    name = models.CharField(max_length=25)
    slug = models.SlugField( blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='groups')
    image = models.ImageField(upload_to='media/images/group/')    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        
        super(Group, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Image(models.Model):
    is_primary = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/')
    product = models.ForeignKey('Product',on_delete=models.CASCADE, related_name='images')
    

class Comment(models.Model):
    class RatingChoice(models.TextChoices):
        Zero = '0'
        One = 'One'
        Two = 'Two'
        Three = 'Three'
        Four = 'Four'
        Five = 'Five'

    rating = models.CharField(max_length=100, choices=RatingChoice.choices, default=RatingChoice.One.value )
    message = models.TextField()
    file = models.FileField(upload_to='media/comments', null=True, blank=True)
    product = models.ForeignKey('Product', on_delete = models.CASCADE, related_name = 'comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments' )


class Attribute_Key(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Attribute_Value(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Attribute(models.Model):
    key = models.ForeignKey('Attribute_Key', on_delete=models.CASCADE)
    value= models.ForeignKey('Attribute_Value', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='attributes')

