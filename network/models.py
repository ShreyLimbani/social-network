import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

RELATIONSHIP_FOLLOWING = 1
RELATIONSHIP_BLOCKED = 2
RELATIONSHIP_STATUSES = (
    (RELATIONSHIP_FOLLOWING, 'Following'),
    (RELATIONSHIP_BLOCKED, 'Blocked'),
)

class User(AbstractUser):
    
    relationships = models.ManyToManyField("self", symmetrical=False, through="Relationship", related_name="related_to")

    def add_relationship(self, user, status):
        relationship, created = Relationship.objects.get_or_create(from_user=self,to_user=user,status=status)
        return relationship

    def remove_relationship(self, user, status):
        Relationship.objects.filter(from_user=self,to_user=user,status=status).delete()
        return None

    def get_relationships(self, status):
        return self.relationships.filter(to_user__status=status, to_user__from_user=self)

    def get_related_to(self, status):
        return self.related_to.filter(from_user__status=status, from_user__to_user=self)

    def get_following(self):
        return self.get_relationships(RELATIONSHIP_FOLLOWING)

    def get_followers(self):
        return self.get_related_to(RELATIONSHIP_FOLLOWING)

    def add_post(self, content):
        post = Post(poster = self,content = content)
        post.save()
        return post


class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')
    timestamp = models.DateTimeField(default=timezone.now)
    content = models.TextField(max_length=144)
    likes = models.ManyToManyField(User, symmetrical=True, related_query_name="liked_posts", through="Like")

    def like(self, user):
        like, created = Like.objects.get_or_create(post=self, user = user)
        print("Liked")
        return like

class Relationship(models.Model):
    from_user = models.ForeignKey(User, related_name="from_user", on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name="to_user", on_delete=models.CASCADE)
    status = models.IntegerField(choices=RELATIONSHIP_STATUSES)


class Like(models.Model):
    post = models.ForeignKey(Post, related_name="post", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="liked_by", on_delete=models.CASCADE)