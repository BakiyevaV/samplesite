from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import BbForm
from .models import Bb, Rubric


def index(request):
    bbs = Bb.objects.order_by('-published')
    rubrics = Rubric.objects.all()
    # for bb in bbs:
    #     bb.title = f'{bb.title} ({bb.pk})'
    #     bb.save()

    for bb in bbs:
        for i in range(len(bb.title)):
            if bb.title[i].isdigit() and bb.title[i+1] == ')':
                if int(bb.title[i]) % 2 != 0:
                    bb.delete()
    context = {'bbs': bbs, 'rubrics': rubrics}
    return render(request, 'index.html', context)

def by_rubric(request, rubric_id):
    bbs = Bb.objects.filter(rubric=rubric_id)
    rubrics = Rubric.objects.all()
    current_rubric = Rubric.objects.get(pk=rubric_id)
    context = {'bbs': bbs, 'rubrics': rubrics,
               'current_rubric': current_rubric}
    return render(request, 'by_rubric.html', context)


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