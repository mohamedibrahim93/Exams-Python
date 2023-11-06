from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


# class Teacher
class Teacher(models.Model):
    Fname = models.CharField(("First Name"), max_length=50)
    Lname = models.CharField(("Last Name"), max_length=50)
    Email = models.EmailField(("Email"), unique=True)
    Address = models.CharField(("Address"), max_length=150)

    class Meta:
        ordering = ('Email',)
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"

    def __str__(self):
        return self.Email

# class Course


class Course(models.Model):
    # Name = models.CharField(("Course Name"), max_length=50,unique=true)
    Name = models.CharField(("Course Name"), max_length=50)
    Duration = models.PositiveIntegerField("Duration", default=1, validators=[
                                           MinValueValidator(1), MaxValueValidator(100)])
    NumChapters = models.PositiveIntegerField("Number of Chapters", default=1, validators=[
                                              MinValueValidator(1), MaxValueValidator(100)])

    #Teacher = models.ForeignKey(Teacher,null=True ,on_delete=models.SET_NULL)

    class Meta:
        ordering = ('Name',)
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self):
        return self.Name

# class Chapter


class Chapter(models.Model):
    Name = models.CharField(("Chapter Name"), max_length=50)
    Course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        ordering = ('Name',)
        verbose_name = "Chapter"
        verbose_name_plural = "Chapters"

    def __str__(self):
        return self.Name


Difficulty = (
    ('Simple', 'Simple'),
    ('Difficult', 'Difficult')
)
Objective = (
    ('Reminding', 'Reminding'),
    ('Understanding', 'Understanding'),
    ('Creativity', 'Creativity')
)

# class Question


class Question(models.Model):
    Header = models.CharField(("Header"), max_length=500)
    Difficulty = models.CharField(
        ("Difficulty"), max_length=20, choices=Difficulty)
    Objective = models.CharField(
        ("Objective"), max_length=20, choices=Objective)
    Ans1 = models.CharField(("Answer 1"), max_length=500)
    Ans2 = models.CharField(("Answer 2"), max_length=500)
    Ans3 = models.CharField(("Answer 3"), max_length=500)
    CorrectAns = models.CharField(("Correct Answer"), max_length=500)
    Chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    # Course = models.ForeignKey(Course,on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        return self.Header

# class Exam


class Exam(models.Model):
    Exam_Date = models.DateField(("Exam Date"))
    Time = models.PositiveIntegerField(("Time"))
    Questions = models.ManyToManyField(Question)
    Course = models.ForeignKey(Course, null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ('Exam_Date',)
        verbose_name = "Exam"
        verbose_name_plural = "Exams"


# class ExamQuestions
# class ExamQuestion(models.Model):
#    Exam = models.ForeignKey(Exam,on_delete=models.CASCADE)
#    Question = models.ForeignKey(Question,on_delete=models.CASCADE)

#    class Meta:
#        unique_together = [("Exam", "Question"),]
#        verbose_name = "ExamQuestion"
#        verbose_name_plural = "ExamQuestions"
