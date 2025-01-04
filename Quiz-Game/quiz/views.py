from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from .models import Quiz, Question, Answer, Score
from django.contrib.auth.forms import UserCreationForm

def home(request):
    quizzes = Quiz.objects.all()
    return render(request, 'home.html', {'quizzes': quizzes})

def register(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def take_quiz(request, id):
    quiz = get_object_or_404(Quiz, id=id)
    if request.method == 'POST':
        score = 0
        for question in quiz.question_set.all():
            correct_answer = question.answer_set.filter(is_correct=True).first()
            selected_answer_id = request.POST.get(str(question.id))
            if selected_answer_id and int(selected_answer_id) == correct_answer.id:
                score += 1
        score_obj, created = Score.objects.update_or_create(
            user=request.user, quiz=quiz,
            defaults={'score': score}
        )
        return redirect('scoreboard')
    return render(request, 'take_quiz.html', {'quiz': quiz})

@login_required
def scoreboard(request):
    scores = Score.objects.order_by('-date')[:10] 
    return render(request, 'scoreboard.html', {'scores': scores})

@login_required
def logout(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('home')