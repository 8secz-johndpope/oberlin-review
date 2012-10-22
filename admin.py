from review.models import *
from django.contrib import admin
from reversion.admin import VersionAdmin

VERSION_ADMIN = VersionAdmin if VersionAdmin else admin.ModelAdmin

class ArticleAdmin(VERSION_ADMIN):
	fieldsets = [
		(None, {'fields': [('title', 'slug'), 'lede', 'full_text', 'published']}),
		('Details', {'fields': ['authors', 'images']}),
		('Taxonomy', {'fields': ['section', 'tags']}),
		('Date', {
			'fields': [('web_date','print_date',),],
			'classes': ('collapse closed',)
		})
	]
	list_display = ('title', 'web_date', 'print_date', 'published')
	list_filter = ['web_date', 'print_date', 'section']
	prepopulated_fields = {'slug': ("title",)}
	radio_fields = {'section': admin.HORIZONTAL}
	filter_horizontal = ('images', 'authors', 'tags')
	search_fields = ['authors__first_name', 'authors__last_name', 'full_text', 'lede', 'title', 'tags__name']

class TagAdmin(admin.ModelAdmin):
	fields = ['name','slug']
	prepopulated_fields = {'slug':("name",)}

class SectionAdmin(admin.ModelAdmin):
	fields = ['name','slug']
	prepopulated_fields = {'slug':("name",)}

class BlogAdmin(admin.ModelAdmin):
	fields = ['title','url']

class GalleryImageInline(admin.TabularInline):
	model = GalleryImageMeta
	extra = 3
	verbose_name_plural = "Images"
	verbose_name = "Image"
	raw_id_fields = ['image']
	sortable_field_name = "order"

class GalleryAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ("title",)}
	fieldsets = ((None, {
		'fields': (('title','slug'),'description')
	}),)
	inlines = [GalleryImageInline]
	search_fields = ['title', 'description']

class ThisWeekAdmin(admin.ModelAdmin):
	fieldsets = ((None, {
		'fields': ('pdf', ('start_date', 'end_date'), 'label', 'published')
	}),)

class FrontPageAdmin(admin.ModelAdmin):
	fieldsets = ((None, {
		'fields': (('date','published'),)
	}),('Content', {
		'fields': (
			('media1_content_type', 'media1_object_id'),
			('media2_content_type', 'media2_object_id'),
			'story1', 'story2', 'story3',
			'teaser1', 'teaser2', 'teaser3', 'teaser4'
		)
	}))
	list_display = ('__unicode__', 'published')
	raw_id_fields = ('story1', 'story2', 'story3', 'teaser1', 'teaser2', 'teaser3', 'teaser4')

admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Author)
admin.site.register(FrontPage, FrontPageAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Issue)
admin.site.register(Section, SectionAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(ThisWeek, ThisWeekAdmin)