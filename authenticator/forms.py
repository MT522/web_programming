from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Contestant, Judge, Score

CSS_FORM_CONTROL_ATTRIBUTE = 'form-control'

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label = 'Email', widget=forms.EmailInput(
        attrs={'class': CSS_FORM_CONTROL_ATTRIBUTE} 
    ))
    first_name = forms.CharField(max_length=127, label = 'First Name', widget= forms.TextInput(
        attrs={'class': CSS_FORM_CONTROL_ATTRIBUTE}
    ))
    last_name = forms.CharField(max_length=127, label = 'Last Name',widget= forms.TextInput(
        attrs={'class': CSS_FORM_CONTROL_ATTRIBUTE}
    ))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs): # I will go to great lenghts to make this great
        super(RegistrationForm, self).__init__(*args, **kwargs) # idek
        self.fields['username'].widget.attrs['class'] = CSS_FORM_CONTROL_ATTRIBUTE
        self.fields['password1'].widget.attrs['class'] = CSS_FORM_CONTROL_ATTRIBUTE
        self.fields['password2'].widget.attrs['class'] = CSS_FORM_CONTROL_ATTRIBUTE
        
    def clean(self):
        try:
            username = self.cleaned_data['username']

            users = User.objects.all()

            duplicate_username = False
            for user in users:
                if (user.username.lower() == username.lower()):
                    duplicate_username = True
                    break
        
            if (duplicate_username):
                self.add_error('username', 'This username is already taken!')
        except Exception:
            self.add_error('username', 'Entered username is invalid!')

class ContestantProfileForm(forms.ModelForm):
    gender = forms.ChoiceField(label="Gender:", choices=Contestant.Gender.choices, widget=forms.RadioSelect())
    
    phone = forms.CharField(label="Phone Number:", help_text="Example : 09**461*****", max_length=14, widget= forms.TextInput())
    telegram_id = forms.CharField(label="Telegram ID:", help_text="Example : @my.tel", max_length=127, widget= forms.TextInput())
    national_id = forms.CharField(label="National or Student ID:", help_text="Example : 001*******", max_length=127, widget= forms.TextInput())

    affiliation = forms.CharField(label="University/Company:", help_text="Example: Sharif University of Technology", max_length=127, widget= forms.TextInput())
    major = forms.CharField(label="Major:", help_text="Example : Electrical Engineering", max_length=127, widget= forms.TextInput())

    prof_name = forms.CharField(label="Advising Professor:", max_length=63, widget= forms.TextInput())
    prof_email = forms.EmailField(label="Advising Professor Email:", max_length=127, widget= forms.EmailInput())

    resume = forms.FileField(label="Resume:", help_text="Upload resume in PDF format", widget= forms.ClearableFileInput())
    resume_share_consent = forms.ChoiceField(label="Consent to share resume with sponsors:", choices=Contestant.Resume_Approve.choices, widget=forms.RadioSelect())

    league = forms.ChoiceField(label="Undergrad/Grad:", choices=Contestant.League.choices, widget=forms.RadioSelect())
    
    class Meta:
        model = Contestant
        fields = ('gender', 'phone', 'telegram_id', 'national_id', 
        'affiliation', 'major', 'prof_name', 'prof_email', 'resume', 'resume_share_consent', 'league')

    def clean(self):
        cleaned_data = super().clean()
        phone = self.cleaned_data['phone']
        national_id = self.cleaned_data['national_id']
        resume = self.files.get('resume')

        if (phone.isdigit() == False):
            self.add_error('phone', 'Phone number must contain only digits!')
        if (national_id.isdigit() == False):
            self.add_error('national_id', 'National/Student ID must contain only digits!')
        if (len(phone) < 10):
            self.add_error('phone', 'Invalid phone number!')
        if (self.validate_file_extension(value=resume) == False):
            self.add_error('resume', 'You must upload a PDF file for your resume!')

    def validate_file_extension(self, value):
        if (value.name.endswith('.pdf') == False):
            return False
        else:
            return True