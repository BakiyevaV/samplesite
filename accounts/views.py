from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse_lazy, resolve
from django.views.decorators.http import require_GET, require_POST, require_safe, require_http_methods
from django.views.generic.edit import CreateView

from bboard.models import Rubric, Bb
from .models import Clients
from .forms import UserForm, LoginForm
from django.shortcuts import redirect

class UserCreateView(CreateView):
    template_name = 'registration.html'
    form_class = UserForm
    model = Clients
    success_url = reverse_lazy('index')
def login_view(request):

    a = Clients.objects.all()
    if request.method == 'POST':
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
                return redirect('index')  # Replace 'main_page' with the actual URL name for your main page
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def require_save(args):
    pass


# @require_http_methods(["GET","POST"])
# @require_GET()
# @require_POST()
# @require_safe()
# @gzip_page()
def index(request):
    r = get_object_or_404(Rubric, name = "Недвижимость")
    bbs = get_list_or_404(Bb, rubric_id = r)

    res = resolve('/2/')
    context = {'title':'Тестовая страница','bbs':bbs, 'res': res}
    return render(request, 'test.html', context)



