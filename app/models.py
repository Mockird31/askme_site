from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField, SearchVector

from datetime import timedelta
from django.utils.timezone import now

# Create your models here.

# Table questions {
#   id int [primary key, increment]
#   title varchar
#   text text
#   profile_id int
#   created_at datetime 
#   updated_at datetime
# }

class AnswerManager(models.Manager):
    def get_answers_with_counts(self, question_id):
        return self.filter(question_id=question_id).annotate(
            like_count=Count('answerlike'),
            dislike_count=Count('answerdislike')
        ).order_by('-created_at')

class QuestionManager(models.Manager):
    def get_questions_with_counts(self):
        return self.annotate(
            like_count=Count('likes'),
            dislike_count=Count('questiondislike')
        ).order_by('-created_at')

    def get_question_with_answers(self, question_id):
        question = self.get_questions_with_counts().get(id=question_id)
        answers = Answer.objects.get_answers_with_counts(question_id=question_id)
        return question, answers

    def get_hot_questions(self):
        return self.annotate(
            like_count=Count('likes'),
            dislike_count=Count('questiondislike')
        ).order_by("-like_count", "-created_at")
    
    def get_by_tag(self, tag_name):
        return self.filter(tags__tag_name__iexact=tag_name).annotate(
            like_count=Count('likes'),
            dislike_count=Count('questiondislike')
        )

    def get_new_questions(self):
        return self.order_by("-created_at")
    
class ProfileManager(models.Manager):
    def get_top_profiles(self):
        return self.annotate(answer_count=Count('answer')).order_by('-answer_count')[:5]
    def get_profile_by_user(self, username):
        return self.get(user__username=username)  
    def get_top_profiles_last_week(self):
        one_week_ago = now() - timedelta(days=7)
        return self.filter(
            question__created_at__gte=one_week_ago  
        ).annotate(
            total_likes=Sum('question__likes__id')  
        ).order_by('-total_likes')[:10]

class TagManager(models.Manager):
    def get_popular_tags(self):
        return self.annotate(question_count=Count('question')).order_by('-question_count')[:5]
    
    def get_popular_tags_last_3_months(self):
        three_months_ago = now() - timedelta(days=90)
        return self.filter(
            question__created_at__gte=three_months_ago  
        ).annotate(
            question_count=Count('question')  
        ).order_by('-question_count')[:10] 

class Tag(models.Model):
    tag_name = models.CharField(max_length=25, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TagManager()

    def __str__(self):
        return self.tag_name

class Profile(models.Model):
    image_path = models.ImageField(upload_to='avatars/', null = True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ProfileManager()

    def get_avatar_url(self):
        if self.image_path:
            return self.image_path.url
        return '/img/common_member.png'

    def __str__(self):
        return self.user.username

class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    search_vector = SearchVectorField(null=True)

    objects = QuestionManager()

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        self.search_vector = (
            SearchVector('title', weight='A') +
            SearchVector('text', weight='B')
        )
        Question.objects.filter(id=self.id).update(search_vector=self.search_vector)

    class Meta:
        indexes = [
            GinIndex(fields=['search_vector']),
        ]

class Answer(models.Model):
    ANSWER_CHOICES = [
        ('c', 'Correct'),
        ('p', 'Pass')
    ]
    text = models.TextField()
    is_correct = models.CharField(max_length=10, choices=ANSWER_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    
    objects = AnswerManager()

    def __str__(self):
        return self.question.title + " ANSWER"

class QuestionLike(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="likes")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('question', 'profile') 

class QuestionDislike(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('question', 'profile')  

class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('answer', 'profile') 

class AnswerDislike(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('answer', 'profile')  

