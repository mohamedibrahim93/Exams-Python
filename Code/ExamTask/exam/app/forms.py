from django import forms
from .models import Course, Chapter, Question, Exam, Teacher, Difficulty, Objective

Correct_ans = (
    ('1', 'Answer Number One'),
    ('2', 'Answer Number Two'),
    ('3', 'Answer Number Three')
)


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = "__all__"


class ChapterForm(forms.Form):
    Name = forms.CharField(max_length=50, min_length=3, required=True,
                           widget=forms.TextInput({
                               'class': 'form-control'
                           }))
    Courses = forms.ModelChoiceField(queryset=Course.objects.all(),
                                     widget=forms.Select({
                                         'class': 'selectpicker', "data-width": "auto",
                                         "data-live-search": "true", "data-live-search-placeholder": "Search",
                                         "data-actions-box": "true", "data-hide-disabled": "true",
                                         "data-selected-text-format": "count>5", "data-size": "7"
                                     }))


class QuestionForm(forms.Form):
    Header = forms.CharField(max_length=500, min_length=7, required=True,
                             widget=forms.Textarea({'cols': 20, 'rows': 3,
                                                    'class': 'form-control'
                                                    }))

    Difficulty = forms.ChoiceField(
        choices=Difficulty, widget=forms.Select(attrs={'class': 'form-control'}))

    Objective = forms.ChoiceField(
        choices=Objective, widget=forms.Select(attrs={'class': 'form-control'}))

    Ans1 = forms.CharField(max_length=500, min_length=1, required=True,
                           widget=forms.Textarea({'cols': 20, 'rows': 1,
                                                  'class': 'form-control'}))

    Ans2 = forms.CharField(max_length=500, min_length=1, required=True,
                           widget=forms.Textarea({'cols': 20, 'rows': 1,
                                                  'class': 'form-control'}))

    Ans3 = forms.CharField(max_length=500, min_length=1, required=True,
                           widget=forms.Textarea({'cols': 20, 'rows': 1,
                                                  'class': 'form-control'}))

    CorrectAns = forms.ChoiceField(choices=Correct_ans, widget=forms.Select(attrs={
        'class': 'form-control'}))

    Chapter = forms.CharField(
        widget=forms.Select({
            'class': 'form-control'
        }))


class examForm(forms.Form):
    Exam_Date = forms.DateField(
        widget=forms.DateTimeInput({
            'class': 'form-control', 'type': 'Date'
        }))
    Time = forms.IntegerField(
        widget=forms.NumberInput({
                                 'class': 'form-control', 'min': 1, 'max': 10, 'value': 1
                                 }))
    Course = forms.ModelChoiceField(queryset=Course.objects.all(),
                                    widget=forms.Select({
                                        'class': 'selectpicker', "data-width": "auto",
                                        "data-live-search": "true", "data-live-search-placeholder": "Search",
                                        "data-actions-box": "true", "data-hide-disabled": "true",
                                        "data-selected-text-format": "count>5", "data-size": "7"
                                    }))


class examGenerateForm(forms.Form):
    NumChapter = forms.IntegerField(
        widget=forms.NumberInput({
            'class': 'form-control', 'min': 1, 'max': 12, 'value': 1
        }))
    NumSimple = forms.IntegerField(
        widget=forms.NumberInput({
            'class': 'form-control', 'min': 0, 'max': 6, 'value': 0
        }))
    NumDifficult = forms.IntegerField(
        widget=forms.NumberInput({
            'class': 'form-control', 'min': 0, 'max': 6, 'value': 0
        }))
    NumRem = forms.IntegerField(
        widget=forms.NumberInput({
            'class': 'form-control', 'min': 0, 'max': 4, 'value': 0
        }))
    NumUnder = forms.IntegerField(
        widget=forms.NumberInput({
            'class': 'form-control', 'min': 0, 'max': 4, 'value': 0
        }))
    NumCrt = forms.IntegerField(
        widget=forms.NumberInput({
            'class': 'form-control', 'min': 0, 'max': 4, 'value': 0
        }))
