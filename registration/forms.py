from django import forms
from django.contrib.auth import authenticate,get_user_model,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from tagify.fields import TagField
from account.models import UserDetails
from hashlib import md5

# Create your forms here.

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if not user:
                raise forms.ValidationError('User Does Not Exist')

            if not user.check_password(password):
                raise forms.ValidationError('Incorrect Password')

        return super(UserLoginForm, self).clean(*args, **kwargs)


User = get_user_model()
UserDetails = UserDetails()


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    username = forms.CharField(max_length=254, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        model = UserDetails
        fields = ('username', 'first_name', 'last_name', 'email')


    def clean_password(self):
        if self.data['password1'] != self.data['password2']:
            raise forms.ValidationError('Passwords are not the same')
        return self.data['password1']

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-lg'

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']
        UserDetails.username = self.cleaned_data['email']
        UserDetails.email = self.cleaned_data['email']
        UserDetails.firstname = self.cleaned_data['first_name']
        UserDetails.lastname = self.cleaned_data['last_name']
        if commit:
            user.save()
            UserDetails.save()
        return user


class ToTransitionForm(forms.Form):
    TransitionTags_From = TagField(label='What defines your journey till date?',
                                   place_holder='Try consulting/finance/business...', delimiters=',',
                                   suggestions_chars=1,
                                   data_list=['Consulting', 'Delhi', 'Finance', 'Venture Capital', 'UK'], initial='')

    TransitionTags_To = TagField(label='What defines your journey till date?',
                                 place_holder='Try consulting/finance/business...', delimiters=',', suggestions_chars=1,
                                 data_list=['Consulting', 'Delhi', 'Finance', 'Venture Capital', 'UK'], initial='')


class PastForm(forms.Form):
    Tags_IndustryPast = TagField(label='What defines your journey till date?',
                             place_holder='Try consulting/finance/business...', delimiters=',', suggestions_chars=1,
                             data_list=['Consulting', 'Delhi', 'Finance', 'Venture Capital', 'UK'], initial='')

    Tags_FunctionalRolesPast = TagField(label='What defines your journey till date?',
                                    place_holder='Try consulting/finance/business...', delimiters=',',
                                    suggestions_chars=1,
                                    data_list=['Consulting', 'Delhi', 'Finance', 'Venture Capital', 'UK'], initial='')

    Tags_GeoPast = TagField(label='What defines your journey till date?',
                        place_holder='Try consulting/finance/business...', delimiters=',',
                        suggestions_chars=1,
                        data_list=['Consulting', 'Delhi', 'Finance', 'Venture Capital', 'UK'], initial='')

    Tags_EducationPast = TagField(label='What defines your journey till date?',
                        place_holder='Try consulting/finance/business...', delimiters=',',
                        suggestions_chars=1,
                        data_list=['Consulting', 'Delhi', 'Finance', 'Venture Capital', 'UK'], initial='')


class PresentForm(forms.Form):
    Tags_IndustryPresent = TagField(label='What defines your journey till date?',
                             place_holder='Try consulting/finance/business...', delimiters=',', suggestions_chars=1,
                             data_list=['Consulting', 'Delhi', 'Finance', 'Venture Capital', 'UK'], initial='')

    Tags_FunctionalRolesPresent = TagField(label='What defines your journey till date?',
                                    place_holder='Try consulting/finance/business...', delimiters=',',
                                    suggestions_chars=1,
                                    data_list=['Consulting', 'Delhi', 'Finance', 'Venture Capital', 'UK'], initial='')

    Tags_GeoPresent = TagField(label='What defines your journey till date?',
                        place_holder='Try consulting/finance/business...', delimiters=',',
                        suggestions_chars=1,
                        data_list=['Consulting', 'Delhi', 'Finance', 'Venture Capital', 'UK'], initial='')

    Tags_EducationPastPresent = TagField(label='What defines your journey till date?',
                        place_holder='Try consulting/finance/business...', delimiters=',',
                        suggestions_chars=1,
                        data_list=['Consulting', 'Delhi', 'Finance', 'Venture Capital', 'UK'], initial='')


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()