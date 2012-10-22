from datetime import datetime


from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.utils.encoding import smart_str
from django.core.mail import mail_managers
import akismet
from django.conf import settings
from django.contrib.sites.models import Site

from review.assets.models import Image


CONTENT_TYPE_CHOICES = Q(name='gallery') | Q(name='image')


class PublishedManager(models.Manager):
	def published(self):
		return self.filter(published=True)

class ArticleManager(models.Manager):
	def published(self):
		return self.filter(published=True, web_date__lte=datetime.now)

class FrontPageManager(models.Manager):
	def published(self):
		return self.filter(published=True, date__lte=datetime.now)

class Tag(models.Model):
	slug = models.SlugField()
	name = models.CharField(max_length=200)
	
	def __unicode__(self):
		return self.name


class Issue(models.Model):
	date = models.DateField()
	number = models.IntegerField()
	volume = models.IntegerField()
	
	def __unicode__(self):
		return u'vol. %s num. %s date. %s' % (self.volume, self.number, self.date)


class Section(models.Model):
	slug = models.SlugField()
	name = models.CharField(max_length=200)
	
	def __unicode__(self):
		return self.name
		
	@models.permalink
	def get_absolute_url(self):
		return ('review.views.section', [self.slug])

class Article(models.Model):
	published = models.BooleanField(default=True, help_text='If not marked, this article will not appear on the website. If you would like to schedule an article for the future, mark this and see the "Web Publish Time" field.')
	issue = models.ForeignKey(Issue, null=True, blank=True, related_name='articles')
	title = models.CharField(max_length=200)
	slug = models.SlugField()
	authors = models.ManyToManyField('Author')
	web_date = models.DateTimeField('web publish time', default=datetime.now, help_text='If set to a date in the future <em>and</em> marked as published, this article will be published in the future.')
	print_date = models.DateField('print publish date', null=True, blank=True)
	lede = models.TextField(null=True, blank=True, help_text='<a href="http://daringfireball.net/projects/markdown/basics">Markdown Formatting</a>')
	full_text = models.TextField(help_text='<a href="http://daringfireball.net/projects/markdown/basics">Markdown Formatting</a>')
	section = models.ForeignKey(Section, related_name='articles')
	tags = models.ManyToManyField(Tag, null=True, blank=True, related_name='articles')
	images = models.ManyToManyField('assets.Image', null = True, blank = True, related_name='articles')
	
	objects = ArticleManager()
	
	def summary(self):
		return self.lede if self.lede else self.full_text.split('\n',1)[0]
	
	def is_published(self):
		if self.published and self.web_date <= datetime.now():
			return True
		else:
			return False
	
	def __unicode__(self):
		return self.title
	
	@models.permalink
	def get_absolute_url(self):
		return ('review.views.single', [self.slug])
		
	class Meta:
		ordering = ['-web_date']
		get_latest_by = 'web_date'


class FrontPage(models.Model):
	published = models.BooleanField()
	date = models.DateField(help_text='If this front page is marked as published and this is a date in the future, this front page will be published at that future date.')
	
	media1_content_type = models.ForeignKey(ContentType, related_name='front_page_media1', limit_choices_to=CONTENT_TYPE_CHOICES, blank=True, null=True)
	media1_object_id = models.PositiveIntegerField(blank=True, null=True)
	media1_content_object = generic.GenericForeignKey('media1_content_type', 'media1_object_id')
	media2_content_type = models.ForeignKey(ContentType, related_name='front_page_media2', limit_choices_to=CONTENT_TYPE_CHOICES, blank=True, null=True)
	media2_object_id = models.PositiveIntegerField(blank=True, null=True)
	media2_content_object = generic.GenericForeignKey('media2_content_type', 'media2_object_id')

	# articles
	story1 = models.ForeignKey('Article', related_name='front_page_story1')
	story2 = models.ForeignKey('Article', related_name='front_page_story2')
	story3 = models.ForeignKey('Article', related_name='front_page_story3')
	teaser1 = models.ForeignKey('Article', related_name='front_page_teaser1')
	teaser2 = models.ForeignKey('Article', related_name='front_page_teaser2')
	teaser3 = models.ForeignKey('Article', related_name='front_page_teaser3')
	teaser4 = models.ForeignKey('Article', related_name='front_page_teaser4')
	
	objects = FrontPageManager()
	
	def __unicode__(self):
		return u'%s' % (self.date)


class Author(models.Model):
	first_name = models.CharField(max_length = 50)
	last_name = models.CharField(max_length = 50)
	display_name = models.CharField(max_length = 100, blank = True, null = True)
	bio = models.TextField(blank = True, null = True)
	photo = models.ForeignKey('assets.Image', blank = True, null = True)
	user = models.OneToOneField('auth.User', blank = True, null = True)
	
	def __unicode__(self):
		if(self.display_name):
			return u'%s' % (self.display_name)
		else:
			return u'%s %s' % (self.first_name, self.last_name)
			
	@models.permalink
	def get_absolute_url(self):
		return ('review.views.author', [self.id])


class Blog(models.Model):
	title = models.CharField(max_length =  200)
	url = models.URLField()
	feedcache = models.TextField(null=True, blank=True)
	lastcache = models.DateTimeField(default=datetime.now)
	
	def __unicode__(self):
		return self.title


class Gallery(models.Model):
	title = models.CharField(max_length=200)
	description = models.TextField(blank=True, null=True)
	images = models.ManyToManyField(Image, through='GalleryImageMeta', related_name="galleries")
	slug = models.SlugField(max_length=40, unique=True)

	@models.permalink
	def get_absolute_url(self):
		return ('images.views.gallery', [self.slug])

	def __unicode__(self):
		return self.title

	class Meta:
		verbose_name_plural = "Galleries"


class GalleryImageMeta(models.Model):
	order = models.IntegerField(blank=True, null=True)
	title = models.CharField(blank=True, max_length=200, null=True)
	caption = models.TextField(blank=True, null=True)
	image = models.ForeignKey(Image, related_name="gallerymetas")
	gallery = models.ForeignKey(Gallery, related_name="imagedatas")

	class Meta:
		ordering = ['order']
		
class ThisWeek(models.Model):
	label = models.CharField(max_length=200, blank=True, null=True, help_text="Optional. A simple label to more easily identify this week. e.g., &ldquo;Finals Week&rdquo;")
	start_date = models.DateField()
	end_date = models.DateField()
	pdf = models.FileField(upload_to="review/thisweek/")
	datetime_added = models.DateTimeField(auto_now_add=True)
	published = models.BooleanField(default=True)
	
	objects = PublishedManager()
	
	@models.permalink
	def get_absolute_url(self):
		return ('review-thisweek-single', (), {
			'year': self.start_date.year,
			'month': self.start_date.month,
			'day': self.start_date.day})
	
	def __unicode__(self):
		date_range = u"%s \u2013 %s" % (self.start_date, self.end_date,)
		return u"%s (%s)" % (self.label, date_range) if self.label else date_range
	
	class Meta:
		ordering = ['-start_date', '-end_date', ]
