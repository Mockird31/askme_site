from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

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

class TagManager(models.Manager):
    def get_popular_tags(self):
        return self.annotate(question_count=Count('question')).order_by('-question_count')[:5]

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

    def __str__(self):
        return self.user.username

class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    objects = QuestionManager()

    def __str__(self):
        return self.title

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


# Table users{
#   username varchar
#   email varchar
#   password varchar
#   id int [pk, increment]
#   created_at datetime 
#   updated_at datetime
# }

# Table question_tags {
#   question_id int 
#   tag_id int
# }

# Table likes_questions {
#   question_id int 
#   profile_id int
# }

# Table likes_answers {
#   answer_id int
#   profile_id int
# }

# Table dislikes_questions {
#   question_id int
#   profile_id int 
# }

# Table dislike_answers {
#   answer_id int
#   profile_id int
# }

# Ref: questions.profile_id > profiles.id
# Ref: profiles.user_id > users.id
# Ref: answers.question_id > questions.id

# Ref: "tags"."id" < "question_tags"."tag_id"

# Ref: "questions"."id" < "question_tags"."question_id"

# Ref: "profiles"."id" < "likes_questions"."profile_id"

# Ref: "likes_questions"."question_id" < "questions"."id"

# Ref: "profiles"."id" < "dislikes_questions"."profile_id"

# Ref: "dislikes_questions"."question_id" < "questions"."id"

# Ref: "profiles"."id" < "dislike_answers"."profile_id"

# Ref: "dislike_answers"."answer_id" < "answers"."id"

# Ref: "profiles"."id" < "likes_answers"."profile_id"

# Ref: "likes_answers"."answer_id" < "answers"."id"


