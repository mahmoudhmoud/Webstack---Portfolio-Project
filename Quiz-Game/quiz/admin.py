from django.contrib import admin
from .models import Quiz, Question, Answer, Score

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Score)