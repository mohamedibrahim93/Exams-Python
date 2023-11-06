from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from ..models import Course, Chapter, Question
from ..forms import ChapterForm
from django.db.models import Count
from django.template.loader import render_to_string

# Create your views here.


def index(request):
    courses = Course.objects.all()
    context = {'courses': courses, 'title': "Courses List With Chapters"}
    return render(request, 'chapters/index.html', context)


def getchapters(request, id):
    course = Course.objects.get(id=id)
    chapters = list(Chapter.objects.filter(Course=course))
    context = {'chapters': chapters, 'title': course.Name}
    if is_ajax(request):
        html = render_to_string('chapters/_ajax.html', context)
        return HttpResponse(html)
   # return HttpResponse("<h1>"+id+"</h1>")
    return redirect("/chapters/")


def getquestions(request, id):
    chapter = Chapter.objects.get(id=id)
    questions = Question.objects.filter(Chapter=chapter)
    context = {'questions': questions, 'title': chapter.Name}
    if is_ajax(request):
        html = render_to_string('chapters/_ajaxQuestions.html', context)
        return HttpResponse(html)
   # return HttpResponse("<h1>"+id+"</h1>")
    return redirect("/chapters/")


def create(request):
    form = ChapterForm(request.POST or None)
    if form.is_valid():
        chapter = Chapter(Name=request.POST["Name"], Course=Course.objects.get(
            id=request.POST["Courses"]))
        chapter.save()
        return redirect("/chapters/")

    context = {'title': "Create New Chapter", 'form': form}
    return render(request, 'chapters/create.html', context)


def edit(request, id):
    chapter = Chapter.objects.get(id=id)
    form = ChapterForm()
    context = {'title': "Edit Chapter : " +
               chapter.Name, 'chapter': chapter, 'form': form}
    return render(request, 'chapters/edit.html', context)


def update(request, id):
    form = ChapterForm(request.POST or None)
    if form.is_valid():
        chapter = Chapter.objects.get(id=id)
        chapter.Name = request.POST["Name"]
        chapter.Course = Course.objects.get(id=request.POST["Courses"])
        chapter.save()
        return redirect("/chapters/")

    context = {'title': "Edit Chapter : " +
               chapter.Name, 'chapter': chapter, 'form': form}
    return render(request, 'chapters/edit.html', context)


def delete(request, id):
    chapter = Chapter.objects.get(id=id)
    chapter.delete()
    data = {
        'is_del': True
    }
    return JsonResponse(data)

    # return redirect('/chapters/')


def validate_name(request):
    name = request.GET.get('name', None)
    course = request.GET.get('course', None)

    data = {
        'is_taken': Chapter.objects.filter(Name=name, Course=Course.objects.get(id=course)).exists()
    }
    return JsonResponse(data)

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'