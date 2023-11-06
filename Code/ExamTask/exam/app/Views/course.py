from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from ..models import Course, Chapter
from ..forms import CourseForm
from django.db.models import Count

# Create your views here.


def index(request):
    courses = Course.objects.all()
    context = {'courses': courses, 'title': "Courses List"}
    return render(request, 'courses/index.html', context)


def create(request):
    form = CourseForm(request.POST or None)
    if form.is_valid():
        save_it = form.save(commit=False)
        save_it.save()
        course = Course.objects.get(Name=request.POST["Name"])
        chapterCount = request.POST["NumChapters"]
        for i in range(int(chapterCount)):
            chapter = Chapter(Name="Chapter "+(i+1).__str__(), Course=course)
            chapter.save()

        return redirect("/courses/")

    context = {'title': "Create New Course", 'form': form}
    return render(request, 'courses/create.html', context)


def edit(request, id):
    course = Course.objects.get(id=id)
    form = CourseForm(instance=course)
    context = {'title': "Edit Course : " +
               course.Name, 'course': course, 'form': form}
    return render(request, 'courses/edit.html', context)


def update(request, id):
    form = CourseForm(request.POST or None)
    if form.is_valid():
        course = Course.objects.get(id=id)
        oldChapterCount = int(course.NumChapters)
        chapterCount = list(Chapter.objects.filter(Course=course))

        newChapterCount = int(request.POST["NumChapters"])

        if newChapterCount > oldChapterCount:
            for i in range(oldChapterCount, newChapterCount):
                chapter = Chapter(
                    Name="Chapter "+(i+1).__str__(), Course=course)
                chapter.save()

        if newChapterCount < oldChapterCount:
            for i in range(len(chapterCount)-1, newChapterCount-1, -1):
                chapterCount[i].delete()

            # for i in range(oldChapterCount,newChapterCount):
            #     chapter=Chapter(Name="Chapter "+(i+1).__str__(),Course=course)
            #     chapter.save()

        course.Name = request.POST["Name"]
        course.Duration = request.POST["Duration"]
        course.NumChapters = request.POST["NumChapters"]
        course.save()

        return redirect("/courses/")

    # course = Course.objects.get(id=id)
    # context = {'title':"Edit Course : "+course.Name,'course': course,'form': form}
    # return render(request, 'courses/edit.html', context)
    return redirect("/courses/edit/"+id)


def delete(request, id):
    course = Course.objects.get(id=id)
    course.delete()
    data = {
        'is_del': True
    }
    return JsonResponse(data)

    # return redirect('/courses/')


def validate_coursename(request):
    coursename = request.GET.get('name', None)
    data = {
        'is_taken': Course.objects.filter(Name=coursename).exists()
    }
    return JsonResponse(data)

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'