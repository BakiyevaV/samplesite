from django.urls import path, re_path

from bboard.views import BbCreateView,Bbslist, Categorylist, BbDetail, CreateComment, DeleteComment, AboutUs, Contacts

app_name = 'bboard'

urlpatterns = [
    re_path(r'^add/$', BbCreateView.as_view(), name='add'),
    re_path(r'^detail/(?P<bb_id>[0-9]+)/$', BbDetail.as_view(), name='get_detail'),
    re_path(r'^rubric/(?P<rubric_id>[0-9]+)/$', Categorylist.as_view(), name='by_rubric'),
    re_path(r'^$', Bbslist.as_view(), name='index'),
    re_path(r'^a\w{3}t/$', AboutUs.as_view(), name='about'),
    re_path(r'^c\w{6}s/$', Contacts.as_view(), name='contacts'),
    re_path(r'^create/(?P<bb_id>[0-9]+)/$', CreateComment.as_view(), name='c_create'),
    re_path(r'^delete/(?P<comment_id>[0-9]+)/(?P<bb_id>[0-9]+)/$', DeleteComment.as_view(), name='delete_comment'),
]
