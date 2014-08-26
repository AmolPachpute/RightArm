from django.db import models
from django.contrib import admin
from django.forms import ModelForm
from ckeditor.fields import RichTextField
from django import forms
### ****************Models****************

SITE_CHOICES = ( (u'site', u'site'), (u'event', u'event'), (u'ffc', u'ffc'),)
class FAQ_Category(models.Model):
    name = models.CharField(max_length=60)
    is_active = models.BooleanField(default = True)
    added = models.DateTimeField(auto_now_add=True)
    choice = models.CharField(max_length=100,blank=True,null=True,choices=SITE_CHOICES)

    def __unicode__(self):
        return self.name

    def get_questions(self):
        return Question.objects.filter(category__id=self.id,is_active = True)

class Question(models.Model):
    category = models.ForeignKey(FAQ_Category)
    question = models.CharField(max_length=200)
    is_active = models.BooleanField(default = True)
    added = models.DateTimeField(auto_now_add=True)


    def get_answer(self):
        return Answer.objects.filter(question__id=self.id, is_active = True)

    def __unicode__(self):
        return "%s"%(self.question)

class Answer(models.Model):
    question = models.ForeignKey(Question)
    answer = RichTextField(blank=True, null=True)
    is_active = models.BooleanField(default = True)
    added = models.DateTimeField(auto_now_add=True)  

    def __unicode__(self):
        return "%s"%(self.answer)


### ****************Admin****************

class FAQ_CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'added', 'is_active')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'added', 'is_active')

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('answer', 'added', 'is_active')


admin.site.register(FAQ_Category, FAQ_CategoryAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)

### ****************Model Forms****************

class FAQ_CategoryForm(ModelForm):
    class Meta:
        model = FAQ_Category

class QuestionForm(ModelForm):
    question = forms.CharField(label=('Question'),max_length=500,widget=forms.Textarea(attrs={'cols': 30, 'rows': 8}),required=True)
    class Meta:
        model = Question
        exclude = ('category')

class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        exclude = ('question')

