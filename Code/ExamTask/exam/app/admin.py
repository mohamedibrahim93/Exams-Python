from django.contrib import admin


# Register your models here.
from .models import Teacher, Course, Chapter, Question, Exam

# Register your models here.


class TeacherAdmin(admin.ModelAdmin):
    class Meta:
        model = Teacher


admin.site.register(Teacher, TeacherAdmin)


class CourseAdmin(admin.ModelAdmin):
    class Meta:
        model = Course


admin.site.register(Course, CourseAdmin)


class ChapterAdmin(admin.ModelAdmin):
    class Meta:
        model = Chapter


admin.site.register(Chapter, ChapterAdmin)


class QuestionAdmin(admin.ModelAdmin):
    class Meta:
        model = Question


admin.site.register(Question, QuestionAdmin)


class ExamAdmin(admin.ModelAdmin):
    class Meta:
        model = Exam


admin.site.register(Exam, ExamAdmin)


# class ExamQuestionAdmin(admin.ModelAdmin):
#    class Meta:
#        model = ExamQuestion

# admin.site.register(ExamQuestion,ExamQuestionAdmin)
