from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from ..models import Course, Chapter, Question, Difficulty, Objective, Exam
from ..forms import examForm, examGenerateForm
from django.db.models import Count
from django.template.loader import render_to_string
import json
# Create your views here.


def index(request):
    courses = Course.objects.all()
    context = {'courses': courses, 'title': "Exam List"}
    return render(request, 'exams/index.html', context)


def assign(request, id):
    exam = Exam.objects.get(id=id)
    course = exam.Course
    chapters = Chapter.objects.filter(Course=course)
    context = {'chapters': chapters,
               'title': "Question For Course : "+course.Name, "exam": exam}
    return render(request, 'exams/assign.html', context)


def getquestions(request, id):
    examId = request.GET.get('exam', None)
    exam = Exam.objects.get(id=examId)
    chapter = Chapter.objects.get(id=id)
    curr_questions = exam.Questions.values('id')
    questions = Question.objects.filter(
        Chapter=chapter).exclude(id__in=curr_questions)
    context = {'questions': questions, 'exam': exam}
    if is_ajax(request):
        html = render_to_string('exams/_ajaxAssign.html', context)
        return HttpResponse(html)
    return redirect("/exams/")


def getexamquestions(request, id):
    exam = Exam.objects.get(id=id)

    questions = exam.Questions.all()
    context = {'questions': questions, 'exam': exam}
    if is_ajax(request):
        html = render_to_string('exams/_ajaxQuestions.html', context)
        return HttpResponse(html)
    return redirect("/exams/")


def getexams(request, id):
    course = Course.objects.get(id=id)
    exams = Exam.objects.filter(Course=course)
    context = {'exams': exams}
    if is_ajax(request):
        html = render_to_string('exams/_ajax.html', context)
        return HttpResponse(html)
    return redirect("/chapters/")


def printexam(request, id):
    exam = Exam.objects.get(id=id)
    questions = exam.Questions.all()
    context = {'questions': questions, 'exam': exam,
               'title': 'Exam Num : ' + exam.id.__str__()}
    return render(request, 'exams/view.html', context)


def designexam(request, id):
    form = examGenerateForm(request.POST or None)
    if(form.is_valid()):
        NumChapter = int(request.POST["NumChapter"])
        NumSimple = int(request.POST["NumSimple"])
        NumDifficult = int(request.POST["NumDifficult"])
        NumRem = int(request.POST["NumRem"])
        NumUnder = int(request.POST["NumUnder"])
        NumCrt = int(request.POST["NumCrt"])

        if NumSimple+NumDifficult == NumChapter and NumRem+NumCrt+NumUnder == NumChapter:
            exam = Exam.objects.get(id=id)
            course = exam.Course
            allquestions = list()
            chapters = Chapter.objects.filter(Course=course)
            # questions=Question.objects.filter(Chapter = chapters)
            for ch in chapters:
                # questions=Question.objects.filter(Chapter = ch).order_by('?')[:NumChapter]
                questions = Question.objects.filter(Chapter=ch).order_by('?')


                rem = questions.filter(Objective="Reminding")[:NumRem]
                for qs in rem:
                    exam.Questions.add(qs)
                    exam.save()
                    # allquestions.append(qs.id)

                crt = questions.filter(Objective="Rreativity")[:NumCrt]
                for qs in crt:
                    exam.Questions.add(qs)
                    exam.save()
                   
                    # allquestions.append(qs.id)

                und = questions.filter(Objective="Understanding")[:NumUnder]
                for qs in und:
                    exam.Questions.add(qs)                    
                    exam.save()
                    # allquestions.append(qs.id)
                # rem.union(und);
                # rem.difference(und,crt)

                # rem.intersection(und,crt)
                    # for qs in range(0,NumChapter):

                    #     allquestions.append(qs.id)

                    # for qs in questions:
                    #     allquestions.append(qs.id)

                    # if allquestions.__contains__(8):
                    #     return HttpResponse("dfgfsd")

                # allquestions=list(rem.all().values("id","Header","Difficulty","Objective"))

                # return JsonResponse(list(allquestions),safe=False)

                    # sim=questions.filter(Difficulty="Simple")[:NumSimple]

                    # return JsonResponse(list(sim.all().values("id","Header","Difficulty","Objective")),safe=False)

                  #  return JsonResponse(allquestions,safe=False)
                    # return HttpResponse(questions[0].Header.__str__())

            return redirect("/exams/")

        form.add_error("NumChapter", 'Error On Number of Questions')
        return render(request, "exams/design.html", {'title': 'Geneate Exam', 'form': form})

    return render(request, "exams/design.html", {'title': 'Geneate Exam', 'form': form})


def create(request):
    form = examForm(request.POST or None)
    if(form.is_valid()):
        exm = Exam(Exam_Date=request.POST["Exam_Date"], Time=request.POST["Time"],
                   Course=Course.objects.get(id=request.POST["Course"]))
        exm.save()
        return redirect("/exams/")
    return render(request, "exams/create.html", {'title': 'Create New Exam', 'form': form})


def generate(request):
    return HttpResponse("fdsfdsgsd")


def delete(request, id):
    exam = Exam.objects.get(id=id)
    exam.delete()
    data = {
        'is_del': True
    }
    return JsonResponse(data)


def edit(request, id):
    exam = Exam.objects.get(id=id)
    form = examForm()
    context = {'title': "Edit Exam", 'exam': exam, 'form': form}
    return render(request, 'exams/edit.html', context)


def update(request, id):
    exam = Exam.objects.get(id=id)
    form = examForm(request.POST or None)
    if form.is_valid():
        exam.Exam_Date = request.POST["Exam_Date"]
        exam.Time = request.POST["Time"]
        exam.Course = Course.objects.get(id=request.POST["Course"])
        exam.save()
        return redirect("/exams/")

    context = {'title': "Edit Exam", 'exam': exam, 'form': form}
    return render(request, 'exams/edit.html', context)


def addtoexam(request, id, eid):
    exam = Exam.objects.get(id=eid)
    question = Question.objects.get(id=id)

    exam.Questions.add(question)
    exam.save()

    return HttpResponse("ok")

def remvefromexam(request, id, eid):
    exam = Exam.objects.get(id=eid)
    question = Question.objects.get(id=id)

    exam.Questions.remove(question)
    exam.save()
    return HttpResponse("ok")

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'