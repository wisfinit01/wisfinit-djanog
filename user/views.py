from django.shortcuts import render
from account.models import UserDetails
# Create your views here.


def user(request):
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

    return render(request, "user/user.html", {'form': form})



def dashboard(request):

    username = request.user.get_username()
    object_1 = UserDetails.objects.get(email=username)
    name = getattr(object_1, 'firstname')

    return render(request, "user/dashboard.html", {'username': name})
