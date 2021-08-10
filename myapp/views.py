import datetime

from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import views
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from .forms import SearchForm, OrderForm, ReviewForm, RegisterForm
from .models import Course, Student, Order, Topic

# Create your views here.
def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    course_list = Course.objects.all().order_by('-title')[:5]
    return render(request, 'myapp/index.html', {'top_list': top_list, 'course_list': course_list})

def dynamic_topic_show(request, topic_id):
    try:
        topic = Topic.objects.get(id=topic_id)
        response = HttpResponse()
        course_list = Course.objects.all()
        topicName = topic.name
        topicLength = topic.length

        return render(request, 'myapp/detail.html', {'topicName': topicName,
                                                     'topicLength': topicLength,
                                                     'course_list': course_list})
    except Topic.DoesNotExist:
        raise Http404("No MyModel matches the given query.")

def about(request):
    visits = request.COOKIES.get('about_visits')
    if visits:
        visits = int(visits) + 1
    else:
        visits = 1
    response = render(request, 'myapp/about.html', {'visits': visits})
    response.set_cookie('about_visits', visits, expires=300)
    return response

def detail(request, topic_id):
    topic = get_object_or_404(Topic, id = topic_id)
    course_list = Course.objects.all()
    return render(request, 'myapp/detail.html', {'topName': topic.name.upper(), 'topLen': str(topic.length), 'cor_list': course_list})

def findcourses(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            price = form.cleaned_data['max_price']
            length = form.cleaned_data['length'] or None
            if length is not None:
                topics = Topic.objects.filter(length=length)
            elif length == None:
                topics = Topic.objects.all()
            courseList = []
            for top in topics:
                courseList = courseList + list(top.courses.filter(price__lte=float(price)))
            return render(request, 'myapp/results.html', {'courselist': courseList, 'name': name, 'length': length})
        else:
            return HttpResponse('Invalid Data')
    else:
        form = SearchForm()
        return render(request, 'myapp/findcourses.html', {'form': form})

def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            courses = form.cleaned_data['courses']
            order = form.save(commit=True)
            student = order.Student
            status = order.order_status
            order.save()
            if status == 1:
                for c in order.courses.all():
                    student.registered_courses.add(c)
                return render(request, 'myapp/order_response.html', {'courses': courses, 'order': order})
        else:
            return render(request, 'myapp/place_order.html', {'form': form})
    else:
        form = OrderForm()
        return render(request, 'myapp/place_order.html', {'form': form})

def review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            course = form.cleaned_data['course']
            if(rating>=1 and rating<=5):
                review = form.save(commit=True)
                review.course.num_reviews += 1
                course.save()
                review.save()
                response = redirect('myapp:index')
                return response
            else:
                return render(request, 'myapp/review.html', {'form': form, 'msg': 'You must enter the rating between 1 and 5!'})
        else:
            return render(request, 'myapp/review.html', {'form': form})
    else:
        form = ReviewForm()
        return render(request, 'myapp/review.html', {'form': form})

def user_login(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        print('Printing....  ' + request.GET.get('next', ''))
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                now = datetime.datetime.now()
                request.session['last_login'] = now.strftime('%m/%d/%Y, %H:%M:%S')
                request.session.set_expiry(3600)
                if request.GET.get('next',''):
                    print('If executed...')
                    return HttpResponseRedirect(request.GET('next'))
                return HttpResponseRedirect(reverse('myapp:myaccount'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid credentials')
    else:
        return render(request, 'myapp/login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('myapp:user_login'))

@login_required
def myaccount(request):
    if request.user.is_authenticated:
        user = request.user
        if len(Student.objects.filter(username=user)) > 0:
            student = Student.objects.get(pk= user.id)
            return render(request, 'myapp/myaccount.html', {'fullname': user.get_full_name(), 'interested_in': student.interested_in.all(), 'registered' : student.registered_courses.all(), 'image': student.image, 'student': True })
        else:
            return render(request, 'myapp/myaccount.html', {'student': False, 'fullname': user.get_full_name()})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            msg = 'Student has been registered successfully'
            top_list = Topic.objects.all().order_by('id')[:10]
            return render(request, 'myapp/login.html', {'top_list': top_list, 'msg': msg})
        else:
            msg = 'Student registration failed. Please provide valid data!'
            form = RegisterForm()
            return render(request, 'myapp/register.html', {'msg': msg, 'form': form})
    else:
        form = RegisterForm()
        return render(request, 'myapp/register.html', {'form': form})