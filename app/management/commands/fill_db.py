from django.core.management.base import BaseCommand, CommandError
from app import models
import random

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('number', type=int)

    """CREATE PROFILES"""
    def create_profiles(self, num: int):
        profiles = [
            models.Profile(
                user=models.User.objects.create_user(
                    username=f"new_user_{i}",
                    password=f"blabla_{hash(f'new_user[i]') % 100}"
                )
            )
            for i in range(num)
        ]
        models.Profile.objects.bulk_create(profiles)
        self.stdout.write(self.style.SUCCESS(f'Successfully created {num} profiles'))

    """CREATE TAGS"""
    def create_tags(self, num: int):
        tags = [
            models.Tag(
                tag_name = f"New_tag_{i}"
            ) for i in range(num)
        ]
        models.Tag.objects.bulk_create(tags)
        self.stdout.write(self.style.SUCCESS(f'Successfullu create {num} tags'))

    """CREATE QUESTIONS"""
    def create_questions(self, num: int):
        questions = []
        for i in range(num * 10):
            rand_profile_id = random.randint(0, num - 1)
            try:
                profile = models.Profile.objects.get(id=rand_profile_id)
            except Exception:
                continue
            question = models.Question(
                title=f"New_title_{i}",
                text=f"text_question_{i} " * 10,
                profile=profile,
            )
            questions.append(question)
            if (i % 10 == 0):
                print(f"Success: {i}")
        print("Questions formed")
        models.Question.objects.bulk_create(questions)

        print("Add tags")
        created_questions = models.Question.objects.filter(
            title__startswith="New_title_"
        ).order_by("id")[:num * 10]

        for question in created_questions:
            rand_tags_num = random.randint(1, 6)
            tags = models.Tag.objects.order_by("?")[:rand_tags_num]
            print(question.id)
            question.tags.set(tags)

        self.stdout.write(self.style.SUCCESS(f'Successfully created {num * 10} questions with tags'))

    """CREATE ANSWERS"""
    def create_answers(self, num: int):
        answers = []
        for i in range(num * 100):
            rand_question_id = random.randint(1, (num * 10) - 1)
            rand_profile_id = random.randint(1, num - 1)
            try:
                question = models.Question.objects.get(id=rand_question_id)
            except models.Question.DoesNotExist:
                continue
            profile = models.Profile.objects.get(id = rand_profile_id)
            answer_text = f"Answer text {i} for question {question.id}"
            is_correct = random.choice(['c', 'p'])
            answer = models.Answer(
                text=answer_text,
                is_correct=is_correct,
                question=question,
                profile=profile
            )
            answers.append(answer)
        models.Answer.objects.bulk_create(answers)
        self.stdout.write(self.style.SUCCESS(f'Successfully created {num * 100} answers'))

    """CREATE QUESTION LIKES AND DISLIKES"""
    def create_question_likes_dislikes(self, num):
        question_likes = []
        question_dislikes = []
        for _ in range(num * 50):
            question_id = random.randint(1, (num * 10) - 1)
            profile_id = random.randint(1, num - 1)

            try:
                question = models.Question.objects.get(id=question_id)
                profile = models.Profile.objects.get(id=profile_id)
            except (models.Question.DoesNotExist, models.Profile.DoesNotExist):
                continue  # Skip if the question or profile doesn't exist

            # Randomly determine the number of likes and dislikes for this question
            num_likes = random.randint(1, 5)  # Example: Random number of likes (1 to 5)
            num_dislikes = random.randint(1, 5)  # Example: Random number of dislikes (1 to 5)

            # Ensure likes and dislikes are not equal
            while num_likes == num_dislikes:
                num_dislikes = random.randint(1, 5)

            # Add likes and dislikes for the question
            for _ in range(num_likes):
                if not any(like.question_id == question_id and like.profile_id == profile_id for like in question_likes):
                    question_like = models.QuestionLike(question=question, profile=profile)
                    question_likes.append(question_like)

            for _ in range(num_dislikes):
                if not any(dislike.question_id == question_id and dislike.profile_id == profile_id for dislike in question_dislikes):
                    question_dislike = models.QuestionDislike(question=question, profile=profile)
                    question_dislikes.append(question_dislike)

        # Add the entries, ignoring conflicts for duplicates
        models.QuestionLike.objects.bulk_create(question_likes, ignore_conflicts=True)
        models.QuestionDislike.objects.bulk_create(question_dislikes, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(question_likes)} question likes and {len(question_dislikes)} question dislikes'))


    """CREATE ANSWERS LIKES AND DISLIKES"""
    def create_answer_likes_dislikes(self, num):
        answer_likes = []
        answer_dislikes = []
        for _ in range(num * 50):
            answer_id = random.randint(1, (num * 100) - 1)
            profile_id = random.randint(1, num - 1)
            
            # Fetch the Answer and Profile instances
            try:
                answer = models.Answer.objects.get(id=answer_id)
                profile = models.Profile.objects.get(id=profile_id)
            except (models.Answer.DoesNotExist, models.Profile.DoesNotExist):
                continue  # Skip this iteration if the answer or profile does not exist

            # Randomly determine the number of likes and dislikes for this answer
            num_likes = random.randint(1, 5)  # Example: Random number of likes (1 to 5)
            num_dislikes = random.randint(1, 5)  # Example: Random number of dislikes (1 to 5)

            # Ensure likes and dislikes are not equal
            while num_likes == num_dislikes:
                num_dislikes = random.randint(1, 5)

            # Add likes and dislikes for the answer
            for _ in range(num_likes):
                if not any(like.answer_id == answer_id and like.profile_id == profile_id for like in answer_likes):
                    answer_like = models.AnswerLike(answer=answer, profile=profile)
                    answer_likes.append(answer_like)

            for _ in range(num_dislikes):
                if not any(dislike.answer_id == answer_id and dislike.profile_id == profile_id for dislike in answer_dislikes):
                    answer_dislike = models.AnswerDislike(answer=answer, profile=profile)
                    answer_dislikes.append(answer_dislike)

        # Add the entries, ignoring conflicts for duplicates
        models.AnswerLike.objects.bulk_create(answer_likes, ignore_conflicts=True)
        models.AnswerDislike.objects.bulk_create(answer_dislikes, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(answer_likes)} answer likes and {len(answer_dislikes)} answer dislikes'))

    def handle(self, *args, **options):
        number = options['number']
        self.create_profiles(number)
        self.create_tags(number)
        self.create_questions(number)
        self.create_answers(number)
        self.create_question_likes_dislikes(number)
        self.create_answer_likes_dislikes(number)
    
        
