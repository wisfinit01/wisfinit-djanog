from pyexpat.errors import messages
import pandas as pd
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from registration.forms import SignUpForm
from django.contrib.auth import get_user_model
from hashlib import md5
from pathlib import Path
from affinda import AffindaAPI, TokenCredential
from django.core.files.storage import FileSystemStorage
from registration.forms import ToTransitionForm
from registration.forms import PastForm
from registration.forms import PresentForm
from django.http import HttpResponse
from registration.forms import UserLoginForm
from django.conf import settings
import os
from django.conf import settings
import datetime as date
import numpy as np
import io
import difflib
from account.models import UserDetails

from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.


User = get_user_model()
UserDetails = UserDetails()

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():

            form.save()
            username = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user, backend='account.backends.CaseInsensitiveModelBackend')
            return redirect('home')

        else:
            # context['SignUpForm'] = form
            return render(request, "registration/signup.html", {'form': form})

    else:
        form = SignUpForm()

    return render(request, "registration/signup.html", {'form': form})


# Create your views here.

def getstarted(request):
    if not request.user.is_authenticated:
        return redirect('signin')

    else:


        if request.method == 'POST':

            doc = request.FILES['myfile']  # returns a dict-like object
            user = request.user
            fs = FileSystemStorage()
            filename = fs.save(doc.name, doc)
            uploaded_file_url = fs.url(filename)
            token = "5087f573f52b5cada663d5c62958a90d75797ea0"
            credential = TokenCredential(token=token)
            client = AffindaAPI(credential=credential)
            file_pth = (uploaded_file_url)
            file_pth = os.path.join(settings.BASE_DIR, 'media', filename)
            with open(file_pth, "rb") as f:
                resume = client.create_resume(file=f)
                cv = resume.as_dict()
            transitions = processcv(cv)
            data = transitions
            slidenumber = 6


            form = ToTransitionForm(request.POST)
            form_past = PastForm(request.POST)
            form_present = PresentForm(request.POST)
            # if form.is_valid():
            # return HttpResponse(str(form.cleaned_data['languages']))
            # if form_past.is_valid():
            # return HttpResponse(str(form.cleaned_data['languages']))
            # if form_present.is_valid():
            # return HttpResponse(str(form.cleaned_data['languages']))

        else:
            form = ToTransitionForm()
            form_past = PastForm()
            form_present = PresentForm()
            data = ""
            slidenumber = 1

    return render(request, "registration/Post_RegisterForm.html",
                  {'form': form, 'form_past': form_past, 'form_present': form_present, 'data': data,'slidenumber': slidenumber})


def signin(request):
    if request.user.is_authenticated:
        return redirect('home')

    else:
        next = request.GET.get('next')
        form = UserLoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user, backend='account.backends.CaseInsensitiveModelBackend')
            return redirect('home')
            if next:
                return redirect(next)
            return redirect('home')

        context = {
            'form': form,
        }
    return render(request, 'registration/account-signin.html', context)



def processcv(final_cv):

    companies = pd.read_csv(
        '/Users/shubhamagarwal/PycharmProjects/wisfinit_v0.1/wisfinitv0/static/wisfinitv0/assets/Files/List_of_companies_in_India_WisFinit.csv')

    companies = companies[['name', 'tags']]
    companies = companies.dropna()
    # print(companies)
    token = "5087f573f52b5cada663d5c62958a90d75797ea0"

    credential = TokenCredential(token=token)
    client = AffindaAPI(credential=credential)
    # all_resumes = client.get_all_resumes()
    # all_CV = all_resumes.as_dict()
    # b = all_CV['results']
    # # print(b)
    #
    # # [val.get('results') for val in all_CV.values()]
    #
    # # print(all_CV.items())
    # a = (pd.DataFrame.from_dict(b))
    # b = (a[a['file_name'] == 'Profile1.pdf']['identifier'])
    # resume = client.get_resume(identifier=b.values[0])
    # # final_cv = (resume.as_dict())
    # print(final_cv)

    #  Processing Education Data
    try:

        education_dic = final_cv['data']["education"][0]
        education = pd.DataFrame.from_dict(final_cv['data']["education"])
        edu_type = pd.DataFrame.from_dict(dict(education['accreditation']))
        edu_type = edu_type.T
        edu_type = list(edu_type['education'].values)
        # print(edu_type)

        dates = pd.DataFrame.from_dict(dict(education['dates']))
        dates = dates.T
        # print(dates)
        dates = dates['start_date'].values
        # print(dates)

        enddate = pd.DataFrame.from_dict(dict(education['dates']))
        enddate = enddate.T
        enddates = enddate['completion_date'].values
        # print(enddates)

        column_names = ["Transition_Type", 'StartDate', 'EndDate', "From", "To"]
        transition_df = pd.DataFrame(columns=column_names)
        # print(transition_df)

        for x in range(len(edu_type)):
            transition_df.loc[x, 'Transition_Type'] = 'Education'
            transition_df.loc[x, 'Tags'] = edu_type[x]
            transition_df.loc[x, 'From'] = ""
            transition_df.loc[x, 'StartDate'] = dates[x]
            transition_df.loc[x, 'EndDate'] = enddates[x]
    except:
        column_names = ["Transition_Type", 'StartDate', 'EndDate', "From", "To"]
        transition_df = pd.DataFrame(columns=column_names)
    # print(transition_df)

    #  Processing Work Data
    workex = pd.DataFrame.from_dict(final_cv['data']["work_experience"])
    dates = pd.DataFrame.from_dict(dict(workex['dates']))

    # print(workex)
    JobTitle = pd.DataFrame.from_dict(dict(workex['occupation']))
    JobTitle = JobTitle.T
    JobTitle = JobTitle['job_title'].values

    # print((JobTitle))

    organization = ((workex['organization']))
    # organization = organization.T
    organization = organization.values

    dates = dates.T
    startdates_workex = dates['start_date'].values
    endtdates_workex = dates['end_date'].values
    transition_df['organization'] = ""

    # print(dates)

    for y in range(len(workex)):
        x = y + len(edu_type)
        transition_df.loc[x, 'Transition_Type'] = 'Career'
        transition_df.loc[x, 'Tags'] = JobTitle[y]
        transition_df.loc[x, 'From'] = ""
        transition_df.loc[x, 'StartDate'] = startdates_workex[y]
        transition_df.loc[x, 'organization'] = organization[y]
        transition_df.loc[x, 'EndDate'] = endtdates_workex[y]

    transition_df["StartDate"] = pd.to_datetime(transition_df["StartDate"])
    transition_df["EndDate"] = pd.to_datetime(transition_df["EndDate"])
    transition_df = transition_df.sort_values(by='StartDate')
    transition_df = transition_df.reset_index(drop=True)

    transition_df['TookGap'] = 0
    transition_df['WentAgaintoEducation'] = 0
    transition_df['promotions'] = 0
    transition_df['dual_career'] = 0
    # print(transition_df.loc[2,'StartDate'] - transition_df.loc[1,'EndDate'].days)

    # print((transition_df.at[1,'EndDate'] - transition_df.at[1,'StartDate']).days)
    # transition_df.at[y,'StartDate'] =

    # print(transition_df)
    tansitions = []
    names = companies['name']
    # a = difflib.get_close_matches("ZS Ass", names )[0]
    # b = companies.loc[companies['name'] == 'Vanguard Business School','tags'].values[0]
    # print(b)

    # print(difflib.get_close_matches("TCS", companies['name'])[0])
    # print(b)

    career_df = transition_df[transition_df['Transition_Type'] == "Career"]
    for x in range(len(transition_df)):
        if x > 1:
            # print(difflib.get_close_matches(transition_df.loc[x, 'organization'], names, 1, 0.6))
            # print(difflib.get_close_matches(transition_df.loc[x - 1, 'organization'], names, 1, 0.6))
            name_curr = difflib.get_close_matches(transition_df.loc[x, 'organization'], names, 1, 0.6)
            if len(name_curr) >= 1:
                name_curr = name_curr[0]
                # print(name_curr)
                current_industry = companies.loc[companies['name'] == name_curr, 'tags'].values[0]
            if len(name_curr) == 0:
                # print('prev1')
                current_industry = ''

            name_prev = difflib.get_close_matches(transition_df.loc[x - 1, 'organization'], names, 1, 0.6)

            if len(name_prev) >= 1:
                # print('prev1')
                name_prev = name_prev[0]
                previous_industry = companies.loc[companies['name'] == name_prev, 'tags'].values[0]

            if len(name_prev) == 0:
                # print('prev1')
                previous_industry = ''

            if current_industry != previous_industry and current_industry != '' and previous_industry != '':
                Transition_text = 'Transitioned from ' + previous_industry + ' to ' + current_industry
                tansitions.append(Transition_text)

    # Checking for transitions
    for y in range(len(transition_df)):

        if y > 1:
            # Checking for career gaps
            if (transition_df.loc[y, 'StartDate'] - max(transition_df.loc[1:y - 1, 'EndDate'])).days > 90:
                transition_df.loc[y, 'TookGap'] = 1

            else:
                transition_df.loc[y, 'TookGap'] = 0

            # Checking for more education
            if transition_df.loc[y, 'Transition_Type'] == "Education" and (
                    transition_df.loc[y, 'EndDate'] - transition_df.loc[y, 'StartDate']).days > 90:
                transition_df.loc[y, 'WentAgaintoEducation'] = 1

            else:
                transition_df.loc[y, 'WentAgaintoEducation'] = 0

            # Checking for promotion
            if transition_df.organization.value_counts()[transition_df.loc[y, 'organization']] > 1:
                transition_df.loc[y, 'promotions'] = 1

            else:
                transition_df.loc[y, 'promotions'] = 0

            # Checking for dual career
            if (transition_df.loc[y, 'StartDate'] - max(transition_df.loc[1:y - 1, 'EndDate'])).days < 0:
                transition_df.loc[y, 'dual_career'] = 1

            else:
                transition_df.loc[y, 'dual_career'] = 0



        else:
            transition_df.loc[y, 'TookGap'] = 0
            transition_df.loc[y, 'WentAgaintoEducation'] = 0
            transition_df.loc[y, 'promotions'] = 0
            transition_df.loc[y, 'dual_career'] = 0

    if sum(transition_df['TookGap']) > 0:
        tansitions.append('Took a career gap')

    if sum(transition_df['WentAgaintoEducation']) > 0:
        tansitions.append('Went again for higher education')

    if sum(transition_df['promotions']) > 0:
        tansitions.append('Got promoted in same organisation')

    if sum(transition_df['dual_career']) > 0:
        tansitions.append('Pursued more than one career at a time')

    tansitions = ", ".join(tansitions)

    return tansitions
