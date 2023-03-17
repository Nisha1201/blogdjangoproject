from django.db import models
# from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50,default=None,null=True,blank=True)
    last_name = models.CharField(max_length=50,default=None,null=True,blank=True)
    place = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)
    dob = models.DateField()
    picture = models.ImageField(upload_to='profile_images')

    def __str__(self):
        return self.user.username


class Post(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_pics')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts',blank=True )
    # dislikes = models.ManyToManyField(User, related_name='disliked_posts')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('comment_view', kwargs={'id':self.id})

    # def get_comments(self):
    #     return self.comments.filter(parent_comment=None).filter(active=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_name=models.CharField(max_length=500)
    comment_body = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default= True)
    likes = models.ManyToManyField(User, related_name='LikeComment',blank=True)
    # parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    # def __str__(self):
    #     return f"{self.comment_body} - {self.comment_name}"


    class Meta:
        ordering=['-created_date']

    def __str__(self):
        return str(self.comment_name) + ' comment ' + str(self.comment_body)

    def get_comments(self):
        return Comment.objects.filter(parent_comment=self).filter(active=True)
    
    def comment_count(self):
        return self.comments.count()

class Reply(models.Model):
        comment=models.ForeignKey(Comment, on_delete=models.CASCADE ,related_name='replies')
        # post = models.ForeignKey(Post, on_delete=models.CASCADE)
        reply_body = models.TextField()
        author = models.ForeignKey(User, on_delete=models.CASCADE)
        created_at = models.DateTimeField(auto_now_add=True)
        likes = models.ManyToManyField(User, related_name='liked_reply',blank=True )
        def __str__(self):
            return self.reply_body
    


