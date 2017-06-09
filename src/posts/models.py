from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.db import models



STATUS_CHOICES = (
    ('d', 'Draft'),
    ('p', 'Published'),
    ('w', 'Withdrawn'),
)

class Author(models.Model):
	name = models.CharField(max_length=50)
	email = models.EmailField(unique=True) #unique = ne moze se registrirati isti mail 2x

	def __unicode__(self):
		return self.name

class Category(models.Model):
	cat_name = models.CharField(max_length=50)
	cat_description = models.CharField(max_length=200)
	slug = models.SlugField(max_length=100, db_index=True)

	def __unicode__(self):
		return self.cat_name

	def get_absolute_url(self):
		return reverse('category', args=[str(self.slug)])

class Post(models.Model):
	title = models.CharField(max_length=120)
	slug = models.SlugField(unique=True)
	content = models.TextField()
	image = models.FileField(null=True,blank=True)
	status = models.CharField(max_length=1, choices=STATUS_CHOICES)
	last_updated = models.DateTimeField(auto_now=True, auto_now_add=False) #auto_now=True svaki put kad se spremi u bazu ovo ce se izvrsit
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)		#auto_now_add=True kad se prvi put spremi u bazu ovo ce se izvrsit
	author = models.ForeignKey(Author)
	categories = models.ManyToManyField(Category)
	

	
	
	def __unicode__(self):
		return self.title


	def get_absolute_url(self):
		return reverse('post', args=[str(self.slug)])

	def save(self, *args, **kwargs):
	    slug = slugify(self.title)
	    exists = Post.objects.filter(slug=slug).exists()
	    if exists:
	    	slug = "%s-%s" %(slug,self.id)

	    self.slug = slug
	    super(Post, self).save(*args, **kwargs)

