from django.conf.urls import patterns, include, url
# handler500 = 'codechef.views.my_custom_error_view'
urlpatterns = patterns('',
  
    url(r'^$','codechef.views.index'),
    url(r'^results/$','codechef.views.results'),
)
