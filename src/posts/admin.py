from django.contrib import admin

# Register your models here.
from .models import Post,Author,Category

class PostModelAdmin(admin.ModelAdmin):
	list_display = ["title", "last_updated","timestamp","author","status"]
	list_display_links = ["last_updated"]
	list_editable = ["title"]
	search_fields = ["title", "content"]
	prepopulated_fields = {'slug': ('title',), }

	class Meta:
			model = Post

	
class CategoryModelAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('cat_name',), }

	class Meta:
			model = Category

admin.site.register(Post,PostModelAdmin)
admin.site.register(Author)
admin.site.register(Category,CategoryModelAdmin)

