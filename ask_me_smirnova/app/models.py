from Tools.demo.sortvisu import distinct
from django.db import models
from django.contrib.auth.models import User
from django.http import Http404

class QuestionManager(models.Manager):
    def get_newest(self):
        return self.prefetch_related('tags').annotate(num_answers=models.Count('answers', distinct=True), num_likes=models.Count('q_likes', distinct=True)).order_by('-id')
    def get_by_tag(self, tag_name):
        try:
            tag = Tag.objects.get(name=tag_name)
            return self.annotate(num_likes=models.Count('q_likes', distinct=True), num_answers=models.Count('answers', distinct=True)).prefetch_related('tags').filter(tags=tag).order_by("-id")
        except Tag.DoesNotExist:
            raise Http404("Страница не найдена")
    def get_hot(self):
        return self.annotate(num_likes=models.Count('q_likes', distinct = True), num_answers=models.Count('answers', distinct=True)).order_by('-num_likes')



class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField(max_length=2047)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = QuestionManager()

    def __str__(self):
        return self.title

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=2047)
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class QuestionLike(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='q_likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        unique_together = [['question', 'user']]

    def __str__(self):
        return self.question.title + self.user.username

class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='a_likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['answer', 'user']]

    def __str__(self):
        return self.answer.title + self.user.username