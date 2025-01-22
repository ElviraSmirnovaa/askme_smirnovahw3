from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from app.models import Tag, Question, QuestionLike, Answer, AnswerLike, Profile
from ask_me_smirnova.views import question


class Command(BaseCommand):
    help = 'Filling Database'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument("ratio", type=int)

    def handle(self, *args, **options):
        ratio = options['ratio']
        users = self.add_users(ratio)
        self.add_profiles(ratio, users)
        tags = self.add_tags(ratio)
        questions = self.add_questions(ratio, users, tags)
        self.add_answers(ratio, users, questions)
        self.add_likes(ratio, users)

    def add_users(self, ratio):
        names = ['Mr. Kva-Kva', 'Ms. Kva-Kva', 'Kvakusha', 'Mr. Prigun', 'Lyagushka', 'Poprygun', 'Miss Prig-Skok', 'Kvakashka', 'Mister Vodyanoi', 'Kvakli']
        emails = ['mrkvakva@mail.ru', 'mskvakva@mail.ru', 'kvakusha@mail.ru', 'mrprigun@mail.ru', 'lyagushka@mail.ru', 'poprygun@mail.ru', 'missprigskok@mail.ru', 'kvakashka@mail.ru', 'mistervodyanoi@mail.ru', 'kvakli@mail.ru']
        data = [User(username=names[i%10]+str(i//10+1), email=emails[i%10], password='mypassword') for i in range(ratio)]
        for user in data:
            user.set_password(user.password)
        User.objects.bulk_create(data)
        return data

    def add_tags(self, ratio):
        tags = ["Tag" + str(i) for i in range(1, ratio + 1)]
        data = [Tag(name=tags[i]) for i in range(ratio)]
        Tag.objects.bulk_create(data)
        return data

    def add_questions(self, ratio, users, tags):
        data = [Question(title="Question" + str(i+1), text="Question" + str(i+1) + " text", author=users[i//10]) for i in range(ratio * 10)]
        Question.objects.bulk_create(data)
        i = 0
        for question in Question.objects.all():
            question.tags.add(tags[i // 10])
            i += 1
        return Question.objects.all()


    def add_answers(self, ratio, users, questions):
        data = [Answer(author=users[i%10], question=questions[i//10], text="Answer" + str(i+1)) for i in range(ratio*100)]
        Answer.objects.bulk_create(data)

    def add_likes(self, ratio, users):
        questions = Question.objects.all()

        data = []
        for i in range(ratio * 10):
            data.append(QuestionLike(question=questions[i], user=users[0]))
            data.append(QuestionLike(question=questions[i], user=users[1]))
        data.append(QuestionLike(question=questions[int(ratio*10/2)], user=users[2])) #Нужно, чтобы хотя бы один вопрос отличался по количеству лайков от остальных
        QuestionLike.objects.bulk_create(data)
        data = []
        answers = Answer.objects.all()
        for i in range(ratio * 100):
            data.append(AnswerLike(answer=answers[i], user=users[0]))
            data.append(AnswerLike(answer=answers[i], user=users[1]))
        AnswerLike.objects.bulk_create(data)

    def add_profiles(self, ratio, users):
        data = [Profile(user=users[int(i)]) for i in range(ratio)]
        Profile.objects.bulk_create(data)