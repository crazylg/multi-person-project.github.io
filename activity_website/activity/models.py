from django.db import models

# Create your models here.


class User(models.Model):
    account = models.CharField(max_length = 30)
    password = models.CharField(max_length = 30)
    nickname = models.CharField(max_length = 20)
    sex = models.CharField(max_length = 10) #male/female
    age = models.PositiveIntegerField()
    email = models.EmailField()
    phone = models.CharField(max_length = 20)
    interest = models.CharField(max_length = 200)
    headImg = models.FileField(upload_to = './templates/static/headimg/')
    friends = models.ManyToManyField("self")

    def __unicode__(self):
        return self.nickname


class Activity(models.Model):
    type = models.CharField(max_length = 20)
    name = models.CharField(max_length = 20)
    explanation = models.CharField(max_length = 400)
    organizer = models.ForeignKey(User, related_name = "activity_organizer")
    members = models.ManyToManyField(User, related_name = "activity_member")
    post_time = models.DateTimeField()
    applyend_time = models.DateTimeField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    place = models.CharField(max_length = 100)
    min_age = models.PositiveIntegerField()
    max_age = models.PositiveIntegerField()
    sex_requirement = models.CharField(max_length = 10) #male/female/both
    status = models.CharField(max_length = 100)
    current_size = models.PositiveIntegerField()
    max_size = models.PositiveIntegerField()
    picture = models.FileField(upload_to = './templates/static/act_picture/', null = True)


class Group(models.Model):
    name = models.CharField(max_length = 20)
    owner = models.ForeignKey(User, related_name = 'group_owner')
    members = models.ManyToManyField(User, related_name = 'group_member')
    explanation = models.CharField(max_length = 400)
    activities = models.ManyToManyField(Activity)
    found_time = models.DateTimeField()
    current_size = models.PositiveIntegerField()
    max_size = models.PositiveIntegerField()


class UserMessage(models.Model):
    user1 = models.ForeignKey(User, related_name = 'usermessage_user1')
    user2 = models.ForeignKey(User, related_name = 'usermessage_user2')
    time = models.DateTimeField()
    content = models.CharField(max_length = 500)


class GroupMessage(models.Model):
    group = models.ForeignKey(Group, related_name = 'groupmessage_group')
    user = models.ForeignKey(User, related_name = 'groupmessage_user')
    time = models.DateTimeField()
    content = models.CharField(max_length = 500)


class Request(models.Model):
    type = models.CharField(max_length = 40) #group_invitation/group_application/friend_application/activity_invitation/activity_application/notice
    title = models.CharField(max_length = 40)
    content = models.CharField(max_length = 500)
    poster = models.ForeignKey(User, related_name = 'request_poster')
    receiver = models.ForeignKey(User, related_name = 'request_receiver')
    status = models.CharField(max_length = 100) #unread/accept/reject
    goal = models.CharField(max_length = 20)
    target = models.CharField(max_length = 100, null = True)
    time = models.DateTimeField(null = True)

class Comment(models.Model):
    poster = models.ForeignKey(User, related_name = 'comment_poster'),
    act = models.ForeignKey(Activity, related_name = 'comment_act'),
    content = models.CharField(max_length = 400),
    time = models.DateTimeField(null = True),

