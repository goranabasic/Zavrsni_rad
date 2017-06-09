from urllib import quote_plus
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render,get_object_or_404,get_list_or_404
from .models import Post, Category
from .forms import Contact
from django.db.models import Q
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt,csrf_protect 


# Create your views here.
def index(request):
	queryset = Post.objects.filter(status='p').order_by('-timestamp')

	page = request.GET.get('page')
	query = request.GET.get('q')
        if query:
        	 queryset = queryset.filter(
        	 	Q(title__icontains=query) |
        	 	Q(content__icontains=query) |
        	 	Q(author__name__icontains=query) 
				).distinct()

	paginator = Paginator(queryset, 5) # Show 5 posts per page

	try:
	    queryset = paginator.page(page)
	except PageNotAnInteger:
	    # If page is not an integer, deliver first page.
	    queryset = paginator.page(1)
	except EmptyPage:
	    # If page is out of range (e.g. 9999), deliver last page of results.
	    queryset = paginator.page(paginator.num_pages)
	context = {
		"object_list":queryset,
		"title": "Clean Blog",
		"categories": Category.objects.all(),
	}
	return render(request,'index.html',context)

def post_detail(request,slug=None):
	instance = get_object_or_404(Post,slug=slug)
	share_string = quote_plus(instance.content)
	context = {
		"title":instance.title,
		"instance": instance,
		"share_string":share_string,
		"categories": Category.objects.all(),
		}
	return render(request,'post.html',context)

def cat_detail(request,cat_slug=None):
	categories = get_object_or_404(Category,slug=cat_slug)
	posts = Post.objects.filter(categories=categories,status='p').order_by('-timestamp')
	page = request.GET.get('page')
	query = request.GET.get('q')
        if query:
        	 posts = posts.filter(
        	 	Q(title__icontains=query) |
        	 	Q(content__icontains=query) |
        	 	Q(author__name__icontains=query) 
				).distinct()
	paginator = Paginator(posts, 5) # Show 5 posts per page

	try:
	    posts = paginator.page(page)
	except PageNotAnInteger:
	    # If page is not an integer, deliver first page.
	    posts = paginator.page(1)
	except EmptyPage:
	    # If page is out of range (e.g. 9999), deliver last page of results.
	    posts = paginator.page(paginator.num_pages)
	context = {
		"categories":categories,
		"posts": posts,
		"category_list": Category.objects.all(),
		}
	return render(request, 'category.html',context)
	
def about(request):
	context = {
		"categories": Category.objects.all(),
		
		}
	return render(request,'about.html',context)

@csrf_exempt
def contact(request):
	form = Contact(request.POST or None)
	if form.is_valid():
		name = form.cleaned_data.get("name")
		email = form.cleaned_data.get("email")
		message = form.cleaned_data.get("message")
		subject = 'Site Contact form'
		from_email = settings.EMAIL_HOST_USER
		to_email = [settings.EMAIL_HOST_USER]
		contact_message = "%s: %s"%(name,message)

		send_mail(
	    subject,
	    contact_message,
	    from_email,
	    to_email,
	    fail_silently=False,
	)
	context = {
		"form": form,
		"categories": Category.objects.all(),
		}
	return render_to_response('contact.html',context,context_instance=RequestContext(request))