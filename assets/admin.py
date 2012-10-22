from .models import Image, Kind, ScribdDocument
from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin

class ImageAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':("title",)}
	search_fields = ['title', 'caption', 'credit']
	list_display = ['__unicode__', 'slug', 'credit','time_uploaded','get_thumbnail_html']
	readonly_fields = ['get_large_html']
	fieldsets = ((None, {
		'fields': ('image', ('title', 'slug'), 'credit', 'caption', ('time_uploaded', 'time_taken'), 'kind')
	}),('Preview', {
		'fields': ('get_large_html',)
	})
	)

admin.site.register(Image, ImageAdmin)
admin.site.register(ScribdDocument)
admin.site.register(Kind)
