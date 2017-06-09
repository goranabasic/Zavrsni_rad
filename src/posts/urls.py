from django.conf.urls import url
from .views import (
	index,
	post_detail,
	about,
	contact,
	cat_detail,
	)

urlpatterns = [
	url(r'^$',index, name='home'),
	url(r'^about/',about, name='about'),
	url(r'^contact/',contact, name='contact'),
	url(r'^(?P<slug>[\w-]+)/$',post_detail, name='post'),
	url(r'^category/(?P<cat_slug>[\w-]+)/$', cat_detail, name='category'),



]