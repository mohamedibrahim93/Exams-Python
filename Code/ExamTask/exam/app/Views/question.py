from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from ..models import Course, Chapter, Question, Difficulty, Objective
from ..forms import QuestionForm
from django.db.models import Count
from django.template.loader import render_to_string

# Create your views here.


def index(request):
    courses = Course.objects.all()
    context = {'courses': courses, 'title': "Questions List"}
    return render(request, 'questions/index.html', context)


def getchapters(request, id):
    course = Course.objects.get(id=id)
    chapters = list(Chapter.objects.filter(Course=course).values('id', 'Name'))
    if is_ajax(request):
        return JsonResponse(chapters, safe=False)
   # return HttpResponse("<h1>"+id+"</h1>")
    return redirect("/chapters/")


def getquestions(request, id):
    course = Course.objects.get(id=id)
    chapters = (Chapter.objects.filter(Course=course).values('id'))
    questions = Question.objects.filter(Chapter_id__in=chapters)
    context = {'questions': questions, 'title': course.Name}
    if is_ajax(request):
        html = render_to_string('questions/_ajax.html', context)
        return HttpResponse(html)
   # return HttpResponse("<h1>"+id+"</h1>")
    return redirect("/questions/")


def getquestionsData(request, id):
    question = Question.objects.get(id=id)
    crAns = ""
    if question.CorrectAns == question.Ans3:
        crAns = question.Ans3
    elif question.CorrectAns == question.Ans2:
        crAns = question.Ans2
    else:
        crAns = question.Ans1
    context = {'question': question,
               'crn': question.Chapter.Course.Name, 'cra': crAns}
    if is_ajax(request):
        html = render_to_string('questions/_ajaxData.html', context)
        return HttpResponse(html)
   # return HttpResponse("<h1>"+id+"</h1>")
    return redirect("/questions/")


def create(request):
    courses = Course.objects.all()
    form = QuestionForm(request.POST or None)
    if form.is_valid():
        chapter = Chapter.objects.get(id=request.POST["Chapter"])
        diff = request.POST["Difficulty"]
        objv = request.POST["Objective"]
        simpleCount = Question.objects.filter(
            Difficulty='Simple', Chapter=chapter).count()

        if simpleCount+1 > 6 and diff == "Simple":
            form.add_error(
                'Difficulty', "Not Allowed More Than 6 Question From One Type")
            context = {'courses': courses,
                       'title': "Create New Question", 'form': form}
            return render(request, 'questions/create.html', context)

        difficultCount = Question.objects.filter(
            Difficulty='Difficult', Chapter=chapter).count()
        if difficultCount+1 > 6 and diff == "Difficult":
            form.add_error(
                'Difficulty', "Not Allowed More Than 6 Question From One Type")
            context = {'courses': courses,
                       'title': "Create New Question", 'form': form}
            return render(request, 'questions/create.html', context)

        objCount = Question.objects.filter(
            Objective='Reminding', Chapter=chapter).count()
        if objCount+1 > 4 and objv == "Reminding":
            form.add_error(
                'Objective', "Not Allowed More Than 4 Question From One Type")
            context = {'courses': courses,
                       'title': "Create New Question", 'form': form}
            return render(request, 'questions/create.html', context)

        remCount = Question.objects.filter(
            Objective='Understanding', Chapter=chapter).count()
        if remCount+1 > 4 and objv == "Understanding":
            form.add_error(
                'Objective', "Not Allowed More Than 4 Question From One Type")
            context = {'courses': courses,
                       'title': "Create New Question", 'form': form}
            return render(request, 'questions/create.html', context)

        undCount = Question.objects.filter(
            Objective='Creativity', Chapter=chapter).count()
        if undCount+1 > 4 and objv == "Creativity":
            form.add_error(
                'Objective', "Not Allowed More Than 4 Question From One Type")
            context = {'courses': courses,
                       'title': "Create New Question", 'form': form}
            return render(request, 'questions/create.html', context)

        correctAns = ""
        if request.POST["CorrectAns"] == "1":
            correctAns = request.POST["Ans1"]
        elif request.POST["CorrectAns"] == "2":
            correctAns = request.POST["Ans2"]
        else:
            correctAns = request.POST["Ans3"]

        qs = Question(Header=request.POST["Header"], Difficulty=request.POST["Difficulty"],
                      Objective=request.POST["Objective"], Ans1=request.POST["Ans1"],
                      Ans2=request.POST["Ans2"], Ans3=request.POST["Ans3"],
                      CorrectAns=correctAns, Chapter=chapter)
        qs.save()

        return redirect("/questions/")

    context = {'courses': courses,
               'title': "Create New Question", 'form': form}
    return render(request, 'questions/create.html', context)


def edit(request, id):
    courses = Course.objects.all()
    question = Question.objects.get(id=id)
    chapter = Chapter.objects.get(id=question.Chapter.id)

    crAns = 1
    if question.CorrectAns == question.Ans3:
        crAns = 3
    elif question.CorrectAns == question.Ans2:
        crAns = 2
    else:
        crAns = 1

    form = QuestionForm()
    context = {'title': "Edit Question", "question": question, 'courses': courses,
               "chapter": chapter, 'cra': crAns, 'form': form}
    return render(request, 'questions/edit.html', context)


def update(request, id):
    courses = Course.objects.all()
    question = Question.objects.get(id=id)
    chapter = Chapter.objects.get(id=question.Chapter.id)
    crAns = 1
    if question.CorrectAns == question.Ans3:
        crAns = 3
    elif question.CorrectAns == question.Ans2:
        crAns = 2
    else:
        crAns = 1
    form = QuestionForm(request.POST or None)
    if form.is_valid():

        diff = request.POST["Difficulty"]
        objv = request.POST["Objective"]

        simpleCount = Question.objects.filter(
            Difficulty='Simple', Chapter=chapter).count()

        if simpleCount+1 > 6 and diff == "Simple":
            form.add_error(
                'Difficulty', "Not Allowed More Than 6 Question From One Type")
            context = {'title': "Edit Question", "question": question, 'courses': courses,
                       "chapter": chapter, 'cra': crAns, 'form': form}
            return render(request, 'questions/edit.html', context)

        difficultCount = Question.objects.filter(
            Difficulty='Difficult', Chapter=chapter).count()
        if difficultCount+1 > 6 and diff == "Difficult":
            form.add_error(
                'Difficulty', "Not Allowed More Than 6 Question From One Type")
            context = {'title': "Edit Question", "question": question, 'courses': courses,
                       "chapter": chapter, 'cra': crAns, 'form': form}
            return render(request, 'questions/edit.html', context)

        objCount = Question.objects.filter(
            Objective='Reminding', Chapter=chapter).count()
        if objCount+1 > 4 and objv == "Reminding":
            form.add_error(
                'Objective', "Not Allowed More Than 4 Question From One Type")
            context = {'title': "Edit Question", "question": question, 'courses': courses,
                       "chapter": chapter, 'cra': crAns, 'form': form}
            return render(request, 'questions/edit.html', context)

        remCount = Question.objects.filter(
            Objective='Understanding', Chapter=chapter).count()
        if remCount+1 > 4 and objv == "Understanding":
            form.add_error(
                'Objective', "Not Allowed More Than 4 Question From One Type")
            context = {'title': "Edit Question", "question": question, 'courses': courses,
                       "chapter": chapter, 'cra': crAns, 'form': form}
            return render(request, 'questions/edit.html', context)

        undCount = Question.objects.filter(
            Objective='Creativity', Chapter=chapter).count()
        if undCount+1 > 4 and objv == "Creativity":
            form.add_error(
                'Objective', "Not Allowed More Than 4 Question From One Type")
            context = {'title': "Edit Question", "question": question, 'courses': courses,
                       "chapter": chapter, 'cra': crAns, 'form': form}
            return render(request, 'questions/edit.html', context)

        correctAns = ""
        if request.POST["CorrectAns"] == "1":
            correctAns = request.POST["Ans1"]
        elif request.POST["CorrectAns"] == "2":
            correctAns = request.POST["Ans2"]
        else:
            correctAns = request.POST["Ans3"]

        question.Header = request.POST["Header"]
        question.Difficulty = request.POST["Difficulty"]
        question.Objective = request.POST["Objective"]
        question.Ans1 = request.POST["Ans1"]
        question.Ans2 = request.POST["Ans2"]
        question.Ans3 = request.POST["Ans3"]
        question.correctAns = correctAns
        question.Chapter = Chapter(id=request.POST["Chapter"])
        question.save()
        return redirect("/questions/")

    context = {'title': "Edit Question", "question": question, 'courses': courses,
               "chapter": chapter, 'cra': crAns, 'form': form}
    return render(request, 'questions/edit.html', context)


def delete(request, id):
    qs = Question.objects.get(id=id)
    qs.delete()
    data = {
        'is_del': True
    }
    return JsonResponse(data)

    # return redirect('/chapters/')


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'