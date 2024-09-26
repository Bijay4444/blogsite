from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator
from django.conf import settings
from taggit.managers import TaggableManager
from django.utils.text import slugify

class PublishedManager(models.Manager):
    def get_queryset(self):
        return (super().get_queryset().filter(status=Post.Status.PUBLISHED))

# Create your models here.
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    
    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(2, "Title must be greater than 2 characters")]
    )
    content = models.TextField()
    slug = models.SlugField(max_length=250)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tags = TaggableManager()
    picture = models.ImageField(upload_to='uploads/post_pictures', blank=True, null=True)
    publish = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status,
        default=Status.DRAFT
    )
    objects = models.Manager()#the default manager
    published = PublishedManager()#the custom manager
    
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]
    
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    comment = models.TextField(
        validators=[MinLengthValidator(3, "Comment must be greater than 3 characters")]
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if len(self.comment) < 15:
            return self.comment
        return self.comment[:11] + ' ...'
    
class Interactions(models.Model):
    INTERACTION_CHOICES = [
        ('like', 'Like'),
        ('bookmark', 'Bookmark'),
        ('share', 'Share')
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=10, choices=INTERACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'post', 'interaction_type']
        ordering = ['-timestamp']
        
    def __str__(self):
        return f'{self.user.username} {self.interaction_type}d {self.post.title}'