from django.db import models
from datetime import datetime
from sorl.thumbnail import get_thumbnail

__all__ = ('Image', 'Kind',)

class Kind(models.Model):
	name = models.CharField(max_length=200)

	def __unicode__(self):
		return self.name
	class Meta:
		app_label = 'assets'
	
class Image(models.Model):
	image = models.ImageField(upload_to='images', height_field = 'height', width_field = 'width')
	height = models.IntegerField(blank=True, null=True, editable = False)
	width = models.IntegerField(blank=True, null=True, editable = False)
	credit = models.CharField(blank=True, max_length=200, null=True)
	title = models.CharField(blank=True, max_length=200, null=True)
	caption = models.TextField(blank=True, null=True)
	time_uploaded = models.DateTimeField(default=datetime.now)
	time_taken = models.DateField(blank=True, null=True)
	kind = models.ForeignKey(Kind)
	slug = models.SlugField(max_length=40, unique=True)
		
	def get_thumbnail_html(self):
		return u"<img src=\""+get_thumbnail(self.image, '100x100').url+"\" />" if self.image else None
	get_thumbnail_html.allow_tags=True
	get_thumbnail_html.short_description="Thumb"
	
	def get_large_html(self):
		return u"<img src=\""+get_thumbnail(self.image, '750x1000').url+"\" />" if self.image else None
	get_large_html.allow_tags=True
	get_large_html.short_description="Large"
		
	def __unicode__(self):
		if self.title:
			return self.title
		else:
			return self.slug
	
	class Meta:
		app_label = 'assets'