from django import forms
from django.contrib.auth.models import User
from app import models

class LoginForm(forms.Form):
    username = forms.CharField(min_length=2, widget=forms.TextInput(attrs={
        'class': 'form-control w-50',
        'placeholder': 'Enter username here',
        'maxlength': '50'
    }))
    password = forms.CharField(min_length=2, widget=forms.PasswordInput(attrs={
        'class': 'form-control w-50',
        'placeholder': 'Enter password here',
        'maxlength': '50'
    }))

    def clean_username(self):
        return self.cleaned_data['username'].strip()
    

class RegisterForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ('image_path', )
    image_path = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'class': 'form-control w-50',
        'placeholder': 'Upload an avatar'
    }))
    username = forms.CharField(min_length=8, widget=forms.TextInput(attrs={
        'class': 'form-control w-50',
        'placeholder': 'Enter username here',
        'maxlength': '50'
    }))
    email = forms.CharField(min_length=5, widget=forms.TextInput(attrs={
        'class': 'form-control w-50',
        'placeholder': 'Enter email here',
        'maxlength': '50'
    }))
    password = forms.CharField(min_length=8, widget=forms.PasswordInput(attrs={
        'class': 'form-control w-50',
        'placeholder': 'Enter password here',
        'maxlength': '50'
    }))
    repeat_password = forms.CharField(min_length=8, widget=forms.PasswordInput(attrs={
        'class': 'form-control w-50',
        'placeholder': 'Repeat password here',
        'maxlength': '50'
    }))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("A user with this username already exists.")
        
        return username
    
    def clean(self):
        data = super().clean()
        password = data.get('password').strip()
        repeat_password = data.get('repeat_password').strip()

        if password != repeat_password:
            raise forms.ValidationError("Passwords are different")
        
        return data
    
    def save(self, commit =True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email'])
        profile = super().save(commit=False)
        profile.user = user
        if commit:
            profile.save()
        return profile
    

class QuestionForm(forms.ModelForm):
    tags = forms.CharField(  
        widget=forms.TextInput(attrs={
            'class': 'form-control w-75',
            'placeholder': 'Enter tags here, separated by commas',
        }),
        help_text="Enter tags separated by commas, e.g., 'python, django, api'."
    )
    class Meta:
        model = models.Question
        fields = ('title', 'text')  
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control w-75',
                'placeholder': 'Enter question\'s title here',
                'maxlength': '255'
            }),
            'text': forms.Textarea(attrs={
                'class': "form-control w-75",
                'rows': '11',
                'placeholder': 'Enter your question here',
                'style': 'resize: none',
            }),
        }
    
    def clean_tags(self):
        tags_input = self.cleaned_data['tags']
        tags_list = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
        invalid_tags = [tag for tag in tags_list if not tag.isalnum()]

        if invalid_tags:
            raise forms.ValidationError(f"Invalid tags: {', '.join(invalid_tags)}")

        return tags_input
    
    def save(self, profile, commit=True):
        question = super().save(commit=False)  
        question.profile = profile  
        if commit:
            question.save()  

            tags_input = self.cleaned_data['tags']
            tags_list = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
            print(tags_list)
            for tag_name in tags_list:
                tag, created = models.Tag.objects.get_or_create(tag_name=tag_name)
                question.tags.add(tag)
            
            self.save_m2m()
        return question
    

class AnswerForm(forms.ModelForm):
    class Meta:
        model = models.Answer
        fields = ('text', )
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '7',
                'placeholder': 'Enter your answer here',
                'style': 'resize: none;',
                'maxlength': '1000'
            })
        }
    def save(self, profile, question, commit=True):
        answer = super().save(commit=False)
        answer.profile = profile
        answer.question = question
        if commit:
            answer.save()
        return answer   
    

class SettingsForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ('image_path',)
        widgets = {
            'image_path':forms.ClearableFileInput(attrs={
            'class': 'form-control w-50',
            'placeholder': 'Upload an avatar',
            })
        }
    username = forms.CharField(required=False, min_length=5, widget=forms.TextInput(attrs={
        'class': 'form-control w-50',
        'placeholder': 'Enter username here',
        'maxlength': '50'
    }))
    email = forms.CharField(required=False, min_length=5, widget=forms.TextInput(attrs={
        'class': 'form-control w-50',
        'placeholder': 'Enter email here',
        'maxlength': '50'
    }))

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['email'].initial = user.email
            self.fields['username'].initial = user.username
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if (models.Profile.objects.filter(user__username=username).exists()):
            raise forms.ValidationError("Profile with this username already exists")
        if not username:
            raise forms.ValidationError("Имя пользователя не может быть пустым.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("Email не может быть пустым.")
        return email

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        if commit:
            user.save()
            profile.save()
        return profile

   