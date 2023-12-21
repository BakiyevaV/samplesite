from django.db.models import Count
from django.http import HttpResponseRedirect, HttpResponse, HttpResponsePermanentRedirect, HttpResponseNotFound, Http404
from django.shortcuts import render
from django.template.loader import get_template, render_to_string
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView

from .forms import BbForm
from .models import Bb, Rubric

def index(request):
    bbs = Bb.objects.all()
    rubrics = Rubric.objects.annotate(cnt=Count("bb")).filter(cnt__gt=0)
    context = {"bbs": bbs, "rubrics": rubrics}
    # template = get_template('index.html')
    # return HttpResponse(template.render(context=context, request=request))
    return HttpResponse(render_to_string('index.html', context, request))

# def index(request):
#     response = HttpResponse("Здесь будет", content_type='text/plain; charset=UTF-8')
#     response.write(' главная')
#     response.writelines((' страница', ' сайта'))#
#     response['keywords'] = "python, django"
#     return response

# def index(request):
#     bbs = Bb.objects.order_by('-published')
#     rubrics = Rubric.objects.all()
#     # # for bb in bbs:
#     # #     bb.title = f'{bb.title} ({bb.pk})'
#     # #     bb.save()
#     #
#     # for bb in bbs:
#     #     for i in range(len(bb.title)):
#     #         if bb.title[i].isdigit() and bb.title[i+1] == ')':
#     #             if int(bb.title[i]) % 2 != 0:
#     #                 bb.delete()
#     # rubrics = []
#     # for r in Rubric.objects.all():
#     #     if len(r.bb_set.all()) != 0:
#     #         rubrics.append(r)
#
#     rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt = 0)
#
#     # rubrics = Rubric.objects.filter(bb__isnull = False ).distinct()
#     context = {'bbs': bbs, 'rubrics': rubrics}
#     return render(request, 'index.html', context)

def by_rubric(request, rubric_id):
    bbs = Bb.objects.filter(rubric=rubric_id)
    rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
    current_rubric = Rubric.objects.get(pk=rubric_id)
    context = {'bbs': bbs, 'rubrics': rubrics,
               'current_rubric': current_rubric}
    return render(request, 'by_rubric.html', context)

# def bb_create(request):
#     bbf = BbForm()
#     context = {'form': bbf}
#     return render(request, 'create.html', context)

# def add_save(request):
#     bbf = BbForm(request.POST)
#
#     if bbf.is_valid():
#         bbf.save()
#         return HttpResponseRedirect(
#             reverse('bboard:by_rubric'),
#             kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}
#         )
#     else:
#         context = {'form': bbf}
#         return render(request, 'create.html', context)


def add_and_save(request):
    print(request.headers["Accept-Encoding"])
    print(request.headers["Cookie"])
    print(request.resolver_match)
    print(request.body)
    if request.headers.get('x-request-with') == 'XMLHttpRequest':
        if request.method == 'POST':
            bbf = BbForm(request.POST)#данные после отправки
            if bbf.is_valid():
                bbf.save()
                return HttpResponseRedirect(
                    reverse('bboard:by_rubric',
                    kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk})
                )
            else:
                context = {'form': bbf}
                return render(request, 'create.html', context)
        else:
            bbf = BbForm()
            context = {'form': bbf}
            return render(request, 'create.html', context)




class BbCreateView(CreateView):
    template_name = 'create.html'
    form_class = BbForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

def about_us(request):
    content = ["Некоммерческий проект.",
                "Наша цель-построить среду объединяющую продавца и покупателя для их комфортного и безопасного сотрудничества."]
    context = {'content': content}
    return render(request, 'footer.html', context)

def contacts(request):
    content = ["сот: + 7 747 777 77 77","Адрес: г.Алматы, ул.Карасай батыра 189 "]
    context = {'content': content}
    return render(request, 'footer.html', context)

#class GetBbDetail()

class BbDetailView(DetailView):
    template_name = 'bb.html'
    model = Bb




# def detail(request, bb_id):
#     try:
#         bb = Bb.objects.get(pk = bb_id)
#     except Bb.DoesNotExist:
#         # return HttpResponseNotFound('Такое объявление не существует')
#         raise Http404('Такое объявление не существует')
#     return HttpResponse()

#request.user.is_autenticated