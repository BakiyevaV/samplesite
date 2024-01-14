import json
import datetime

from django.http import HttpHeaders
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView
from .models import Clients
from .forms import UserForm, LoginForm
from django.shortcuts import redirect

class UserCreateView(CreateView):
    template_name = 'registration.html'
    form_class = UserForm
    model = Clients
def login_view(request):
    if request.method == 'POST':
        request_write(request)
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['login']
            password = form.cleaned_data['password']
            user = None
            users = Clients.objects.all()
            for u in users:
                if u.login == username and u.password == password:
                    user = u
            if user is not None:
                return redirect(reverse('bboard:index'))
            else:
                return redirect(reverse('registration'))
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def request_write(request):
    data = {}
    request_params = ('scheme', 'body', 'path', 'method', 'encoding', 'content_type', 'GET',
                      'POST', 'COOKIES', 'FILES', 'headers',
                      {'META': ('CONTENT_LENGTH', 'CONTENT_TYPE', 'HTTP_ACCEPT', 'HTTP_HOST', 'HTTP_REFERER',
                                'HTTP_USER_AGENT', 'QUERY_STRING', 'REMOTE_ADDR')})
    with open('logs.json', 'w', encoding='utf-8') as log_file:
        print(request.META["HTTP_HOST"])
        for param in request_params:
            if type(param) == str:
                data[param] = decoder(getattr(request, param))
            else:
                m_key = ""
                meta_p = {}
                for key, subparams in param.items():
                    m_key = key
                    obj = getattr(request, key)
                    for subparam in subparams:
                        meta_p[f'{subparam}'] = decoder(obj[f'{subparam}'])

                data[m_key] = meta_p
        data_for_write = {f"{datetime.datetime.now()}":data}
        json.dump(data_for_write, log_file)

def decoder(value):
    if isinstance(value, bytes):
        return value.decode("utf-8")
    elif isinstance(value, HttpHeaders):
        return dict(value)
    return value














