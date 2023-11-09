from django.http import HttpResponse
from bboard.models import Bb
from django.template import loader
from django.shortcuts import render

def index(request):
    bbs = Bb.objects.order_by('-publiched')
    context = {'bbs': bbs}
    return render( request,'index.html',context)


# def index_old(request):
#     template = loader.get_template('index.html')
#     bbs = Bb.objects.order_by('-publiched')
#     context = {'bbs': bbs}
#     return HttpResponse(template.render(context,request))


