from django.contrib import admin
# aynı dizinde bulunduğu için .models olarak çağrılır
# from post.models import Post olarak da çağrılabilir.
from .models import Post

# Register your models here.

class PostAdmin(admin.ModelAdmin):

    list_display = ['title', 'publishing_date', 'slug']
    list_display_links = ['publishing_date']
    list_filter = ['publishing_date']
    search_fields = ['title', 'content']
    list_editable = ['title']

# Post modelini referans alarak admin modelinin hangi uygulamaya ait olduğu belirtildi
    class Meta:
        model = Post

admin.site.register(Post, PostAdmin)