from django.shortcuts import render, redirect
from .models import QuestionsSet
import random
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
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
            return redirect('/')

    context = {'form': form}
    return render(request, 'register.html', context)


def login_page(request):
    return render(request, 'login.html')


class SingleGame:
    @staticmethod
    def user_request(request):
        nums = [10, 20, 30, 40]
        categories = QuestionsSet.objects.all().values_list('category', flat=True).distinct()
        user_request = {'nums': nums, 'categories': categories}
        if request.method == 'POST':
            num = int(request.POST.get('input1'))
            category = request.POST.get('input2')
            questions_chosen = []
            print(num, category)
            questions = QuestionsSet.objects.filter(category=category).values()
            index_list = [i for i in range(len(questions))]
            for i in range(num):
                question_index = random.randint(0, len(index_list)-1)
                questions_chosen.append(questions[index_list.pop(question_index)])
                questions_chosen[i]['index'] = str(i)
            request.session['questions'] = questions_chosen
            return redirect('gameview')
        return render(request, 'user_request.html', user_request)

    @staticmethod
    def single_game_view(request):
        questions = request.session['questions']
        score = 0
        if request.method == 'POST':
            for i in range(len(questions)):
                answer = request.POST.get(str(i))
                if answer == questions[i]['correct_answer'].lower():
                    score += 1
            request.session.pop('questions', None)
            request.session['result'] = score
            return redirect('result')
        return render(request, 'single_game_page.html', {'questions': questions, 'length': len(questions)})

    @staticmethod
    def single_game_result(request):
        return render(request, 'single_game_result.html', {'result': request.session.pop('result', None)})

