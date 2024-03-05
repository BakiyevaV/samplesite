import calendar

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.views import redirect_to_login


from django.contrib.auth.decorators import user_passes_test
from django.db import transaction
from django.db.models import Count
from django.forms.formsets import ORDERING_FIELD_NAME
from django.http import HttpResponseRedirect, HttpResponse, HttpResponsePermanentRedirect, HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import get_template, render_to_string
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, ListView, DeleteView, ArchiveIndexView, MonthArchiveView, \
    WeekArchiveView, UpdateView
from django.views.generic.base import TemplateView, RedirectView
from precise_bbcode.bbcode import get_parser

from .forms import BbForm, CommentsForm, SearchForm
from .models import Bb, Rubric, Comments
from django.forms import modelformset_factory, inlineformset_factory


# class Bbslist(ListView):
#     model = Bb
#     template_name = 'index.html'
#     context_object_name = 'bbs'
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['rubrics'] = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt = 0)
#         return context

class BbIndexView(ArchiveIndexView):
    model = Bb
    template_name = 'index.html'
    date_field = 'published'
    date_list_period = 'month'
    context_object_name = 'bbs'
    allow_empty = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        updated_date_list = []
        for date in context['date_list']:
            month_name = calendar.month_name[date.month]
            updated_date_list.append({
                'year': date.year,
                'month': month_name,
                'day': date.day
            })

        context['date_list'] = updated_date_list
        context['rubrics'] = Rubric.objects.all()
        return context



class BbMonthView(MonthArchiveView):
    model = Bb
    template_name = 'index.html'
    date_field = 'published'
    date_list_period = 'month'
    month_format = '%m'
    context_object_name = 'bbs'
    allow_empty = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        updated_date_list = []
        for date in context['date_list']:
            month_name = calendar.month_name[date.month]
            updated_date_list.append({
                'year': date.year,
                'month': month_name,
                'day': date.day
            })

        context['date_list'] = updated_date_list
        context['rubrics'] = Rubric.objects.all()
        return context



class BbRedirectView(RedirectView):
    url = '/'

class Categorylist(ListView):
    model = Bb
    template_name = 'by_rubric.html'
    context_object_name = 'bbs'
    ordering = ['-published']
    def get_queryset(self, ):
        return Bb.objects.filter(rubric=self.kwargs['rubric_id'])


class BbCreateView(CreateView, AccessMixin):
    template_name = 'create.html'
    form_class = BbForm
    success_url = reverse_lazy('bboard:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.has_perm('bboard.add_bb'):
                return render(request, self.template_name, {'message': 'Нет доступа на создание объявлений'})
            else:
                return render(request, self.template_name, {'form': self.form_class})
        else:
            return redirect_to_login(reverse('bboard:index'))
        return super().get(request, *args, **kwargs)



class AboutUs(TemplateView):
    template_name = 'footer.html'
    content = ["Некоммерческий проект.",
               "Наша цель-построить среду объединяющую продавца и покупателя для их комфортного и безопасного сотрудничества."]
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content'] = self.content
        return context

class Contacts(TemplateView):
    template_name = 'footer.html'
    content = ["сот: + 7 747 777 77 77","Адрес: г.Алматы, ул.Карасай батыра 189 "]
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content'] = self.content
        return context
class BbDetail(DetailView):
    model = Bb
    template_name = 'bb.html'
    context_object_name = 'bb'
    pk_url_kwarg = 'bb_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Bb'] = Bb.objects.filter(pk=self.kwargs['bb_id'])
        context['comments'] = Comments.objects.all().filter(bb=self.kwargs['bb_id'])
        return context

def detail(request, pk):
    parser = get_parser()
    bb = Bb.objects.get(pk=pk)
    parsed_content = parser.render(bb.content)
    pass
class CreateComment(CreateView):
    template_name = 'bb.html'
    form_class = CommentsForm
    context_object_name = 'bb'
    pk_url_kwarg = 'bb_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bb'] = get_object_or_404(Bb, pk=self.kwargs['bb_id'])
        context['comments'] = Comments.objects.filter(bb=self.kwargs['bb_id'])
        return context

    def form_valid(self, form):
        bb_id = self.kwargs['bb_id']
        bb = get_object_or_404(Bb, pk=bb_id)
        comment = form.save(commit=False)
        comment.bb = bb
        comment.save()
        return redirect(reverse('bboard:get_detail', args=[bb_id]))

class DeleteComment(DeleteView):
    model = Comments
    template_name = 'bb.html'
    pk_url_kwarg = 'bb_id'
    def get_success_url(self):
        bb_id = self.kwargs['bb_id']
        return reverse('bboard:get_detail', args=[bb_id])
    def get_object(self, queryset=None):
        print(get_object_or_404(Comments, pk=self.kwargs['comment_id']))
        print("айди", self.kwargs['bb_id'])
        return get_object_or_404(Comments, pk=self.kwargs['comment_id'])


class BbEditView(UpdateView):
    template_name = 'update.html'
    model = Bb
    form_class = BbForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubric'] = Rubric.objects.all()
        return context


def edit(request, pk):
    bb = Bb.objects.get(pk=pk)
    print(bb)
    if request.method == 'POST':
        bbf = BbForm(request.POST, instance=bb)
        if bbf.is_valid():
            if bbf.has_changed():
                bbf.save()
                return HttpResponseRedirect(reverse('bboard:by_rubric'), kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk})
            else:
                return HttpResponseRedirect(reverse('bboard:index'))
        else:
            context = {'form': bbf}
            return render(request, 'update.html', context)
    else:
       if request.user.has_perm('bboard.add_bb'):
            bbf = BbForm(instance=bb)
            print(bbf['title'].value())
            context = {'form': bbf}
            return render(request, 'update.html', context)
       else:
           return render(request, 'update.html', {'message': 'Нет доступа на редактирование'})

def commit_handler():
    print('СOMMITED')
def rubrics(request):
    RubricFormSet = modelformset_factory(Rubric, fields=('name',),
                                         can_order=True,
                                         can_delete=True)

    if request.method == 'POST':
        formset = RubricFormSet(request.POST)

        if formset.is_valid():
            instances = formset.save(commit=False)
            for obj in formset:
                if obj.cleaned_data:

                    sp = transaction.savepoint()
                    try:
                        rubric = obj.save(commit=False)
                        rubric.order = obj.cleaned_data[ORDERING_FIELD_NAME]
                        rubric.save()
                        transaction.savepoint_commit(sp)
                    except:
                        transaction.savepoint_rollback(sp)
                        transaction.commit()

                    transaction.on_commit(commit_handler )


            for obj in formset.deleted_objects:
                obj.delete()

            return redirect('bboard:index')

    else:
        formset = RubricFormSet()
    context = {'formset': formset}
    return render(request, 'rubrics.html', context)
@user_passes_test(lambda user: user.is_stuff)
def bbs(request, rubric_id):
    BbsFormSet = inlineformset_factory(Rubric, Bb, form=BbForm, extra=1)
    rubric = Rubric.objects.get(pk=rubric_id)
    if request.user.is_authenticated:
        print(request.user.username)
        if request.method == 'POST':
            formset = BbsFormSet(request.POST, instance=rubric)
            if formset.is_valid():
                formset.save()
                return redirect('bboard:index')
            else:
                formset = BbsFormSet(instance=rubric)
        else:
            formset = BbsFormSet(instance=rubric)
            context = {'formset': formset, 'current_rubric': rubric, 'user': request.user.username}
        return render(request, 'bbs.html', context)
    else:
        print(None)
        formset = BbsFormSet(instance=rubric)
        context = {'formset': formset, 'current_rubric': rubric, 'user': request.user.username}
        return render(request, 'bbs.html', context)


def Search(request):
    if request.method == 'POST':
        sf = SearchForm(request.POST)
        if sf.is_valid():
            keyword = sf.cleaned_data['keyword']
            rubric_id = sf.cleaned_data['rubric'].pk
            current_rubric = sf.cleaned_data['rubric']
            bbs = Bb.objects.filter(title__iregex=keyword, rubric=rubric_id)
            context = {'bbs':bbs, 'rubric': current_rubric, 'keyword': keyword}
            return render(request, 'search_results.html', context)
    else:
        sf = SearchForm()
        context = {'form': sf}
        return render(request, 'search.html', context)

# def my_login(request):
#     username = request.POST.get('username')
#     password = request.POST.get('password')
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#     else:
#         pass
#
#
# def my_logout(request):
#     logout(request)
#
# def hide_comment(request):
#     if request.user.has_perm('accounts.hide_comment'):
#         pass
# from django.contrib.auth.models import User
# admin = User.objects.get(name='admin')
# if admin.check_password('password'):
#     # дальнейшие действия при совпадении
#     pass
# else:
#     # дальнейшие действия при несовпадении
#     pass





