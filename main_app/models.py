from django.db import models
from account.models import MyUser


class Category(models.Model):
    slug = models.SlugField(max_length=100, primary_key=True)
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created_at', )


class PostImages(models.Model):
    image = models.ImageField(upload_to='posts', blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')


class Comment(models.Model):
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.comment

    class Meta:
        ordering = ('-created', )


class Like(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    like = models.BooleanField(default=False)


class Rating(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='ratings')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveSmallIntegerField(default=0)
