from django.shortcuts import render, redirect
from .models import QuestionsSet, QuickTriviaLeaderboard
import random
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils import timezone
from django.forms.models import model_to_dict
from urlparams.redirect import param_redirect
from django.utils.safestring import mark_safe
import json

# Create your views here.


def home(request):
    question_set = QuestionsSet()
    # QuestionsSet.load_data()
    return render(request, "home.html")


def register_page(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for '+ user)
            return redirect('login')

    context = {'form': form}
    return render(request, 'register.html', context)


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Username OR Password is Incorrect')

    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('/')


class SingleGame:
    @staticmethod
    def user_request(request):
        nums = [10, 20, 30, 40]
        categories = list(QuestionsSet.objects.all().values_list('category', flat=True).distinct())
        categories.append('Any Category')
        user_request = {'nums': nums, 'categories': categories}
        if request.method == 'POST':
            num = int(request.POST.get('input1'))
            category = request.POST.get('input2')
            questions_chosen = []
            print(num, category)
            if category == 'Any Category':
                questions = QuestionsSet.objects.all().values()
            else:
                questions = QuestionsSet.objects.filter(category=category).values()
            index_list = [i for i in range(len(questions))]
            for i in range(num):
                question_index = random.randint(0, len(index_list)-1)
                questions_chosen.append(questions[index_list.pop(question_index)])
                questions_chosen[i]['index'] = str(i)
            request.session['questions'] = questions_chosen
            request.session['category'] = category
            return redirect('gameview')
        return render(request, 'user_request.html', user_request)

    @staticmethod
    def single_game_view(request):
        if not request.session['questions']:
            return redirect('/')
        questions = request.session['questions']
        score = 0
        if request.method == 'POST':
            for i in range(len(questions)):
                answer = request.POST.get(str(i))
                if answer == questions[i]['correct_answer'].lower():
                    score += 1

            request.session['result'] = score
            return redirect('result')
        return render(request, 'single_game_page.html', {'questions': questions, 'length': len(questions)})

    @staticmethod
    def single_game_result(request):
        current_user = request.user
        length = len(request.session.pop('questions', None))
        result = request.session.pop('result', None)
        category = request.session.pop('category', None)
        if QuickTriviaLeaderboard.objects.filter(player_id=current_user.id).exists() and \
                result > QuickTriviaLeaderboard.objects.filter(player_id=current_user.id).values('score')[0]['score']:
            QuickTriviaLeaderboard.objects.filter(player_id=current_user.id).delete()
            QuickTriviaLeaderboard.objects.create(score=result, attempt=length, category=category,
                                                  completed=timezone.now(), player_id=current_user.id)
        elif not QuickTriviaLeaderboard.objects.filter(player_id=current_user.id).exists():
            QuickTriviaLeaderboard.objects.create(score=result, attempt=length, category=category,
                                                  completed=timezone.now(), player_id=current_user.id)
        leader = QuickTriviaLeaderboard.objects.order_by('-score')[:15]
        leader_set = []
        index = 1
        for dataset in leader:
            dict_leader = model_to_dict(dataset)
            dict_leader['player'] = User.objects.filter(id=dict_leader['player']).values('username')[0]['username']
            dict_leader['rank'] = index
            index += 1
            leader_set.append(dict_leader)
        return render(request, 'single_game_result.html', {'leader': leader_set, 'result': result})

