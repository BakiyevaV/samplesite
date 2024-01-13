from django.urls import path, re_path

from bboard.views import index, by_rubric, BbCreateView, about_us,contacts, get_detail,create_comment,delete_comment
app_name = 'bboard'

urlpatterns = [
    re_path(r'^add/$', BbCreateView.as_view(), name='add'),
    # re_path(r'^add/save/$', add_save, name='add_save'),
    # re_path(r'^add/$', bb_create, name='add'),Ы
    # re_path(r'^add/$', add_and_save, name='add'),
    re_path(r'^(?P<rubric_id>[0-9]*)/$', by_rubric, name='by_rubric'),
    re_path(r'^$', index, name='index'),
    re_path(r'^a\w{3}t/$', about_us, name='about'),
    re_path(r'^c\w{6}s/$', contacts, name='contacts'),
    re_path(r'^d\w{4}l/(?P<bb_id>[0-9]*)/$', get_detail, name='get_detail'),
    re_path(r'^c_{5}e/(?P<bb_id>[0-9]*)/$', create_comment, name='c_create'),
    re_path(r'^d\w*_c\w*t/(?P<comment_id>[0-9]*)/(?P<bb_id>[0-9]*)/$', delete_comment, name='delete_comment'),
]
