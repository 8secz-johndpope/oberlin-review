# -*- coding: utf-8 -*-
import datetime

from django.template import Context, loader, RequestContext, Template
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator
from review.models import Article, FrontPage, Section, Author, Blog, ThisWeek
from django.core.urlresolvers import reverse

from review.models import Gallery, GalleryImageMeta

import feedparser
import datetime
from operator import itemgetter
import urllib

def index(request):
	front_page = FrontPage.objects.published().order_by('-date')

	# if there are no published front pages, raise a 404
	if not front_page:
		raise Http404('No front pages have been published.')
		
	articles = {
		'news': Article.objects.published().filter(section__name__exact='News').order_by('-web_date')[:5],
		'arts':  Article.objects.published().filter(section__name__exact='Arts').order_by('-web_date')[:5],
		'opinions':  Article.objects.published().filter(section__name__exact='Opinions').order_by('-web_date')[:5],
		'sports':  Article.objects.published().filter(section__name__exact='Sports').order_by('-web_date')[:5],
	}
	return render_to_response('review_front.html', {'front_page': front_page[0], 'articles': articles}, context_instance=RequestContext(request))

def single(request, article_slug):
	article = get_object_or_404(Article, slug__exact=article_slug)

	# the article either has to be published or the user has to be staff to preview it
	if article.is_published() or request.user.is_staff:
		# clean this up and make it work
		tem = Template(article.full_text)
		c = Context({'images': article.images,})
		article.processed_text = tem.render(c)
		return render_to_response('articles/single.html', {'article': article}, context_instance=RequestContext(request))
	else:
		raise Http404('This article is unpublished or scheduled to be published in the future.')
		
def comments(request,article_slug):
	article = get_object_or_404(Article, slug__exact=article_slug)
	return render_to_response('articles/comments.html', {'article': article}, context_instance=RequestContext(request))
	
def section(request,section_slug):
	section = get_object_or_404 (Section, slug__exact=section_slug)
	article_list = Article.objects.published().filter(section = section).order_by('-web_date')
	p = Paginator(article_list, 5)
	
	# Make sure page request is an int. If not, deliver first page.
	try:
		page = int(request.GET.get('page', '1'))
	except ValueError:
		page = 1
	
	# If page request (9999) is out of range, deliver last page of results.
	try:
		articles = p.page(page)
	except (EmptyPage, InvalidPage):
		articles = p.page(p.num_pages)
	
	return render_to_response("articles/list_page.html", {'page_title': section.name, 'section': section, 'articles': articles.object_list, 'page': articles}, context_instance=RequestContext(request))
	
def author(request, author_id):
	author = get_object_or_404 (Author, pk__exact = author_id)
	articles = Article.objects.published().filter(authors = author).order_by('-web_date')
	page_title = "Articles: %s" % author.__unicode__()
	return render_to_response("articles/list_page.html", {'page_title': page_title, 'articles': articles}, context_instance=RequestContext(request))

def search(request, q=None):
	if q:
		text_search = Article.objects.published().filter(full_text__icontains=q)
		title_search = Article.objects.published().filter(title__icontains=q)
		tags_search = Article.objects.published().filter(tags__name__icontains=q)
		lede_search = Article.objects.published().filter(tags__name__icontains=q)
		author_fname_search = Article.objects.published().filter(authors__first_name__icontains=q)
		author_lname_search = Article.objects.published().filter(authors__last_name__icontains=q)
		author_dname_search = Article.objects.published().filter(authors__display_name__icontains=q)
		results = text_search | title_search | tags_search | lede_search | author_fname_search | author_lname_search
		results = results.order_by('-web_date')
		page_title = u'Search for “%s”' % q
		return render_to_response("articles/list_page.html", {'page_title': page_title, 'articles': results}, context_instance=RequestContext(request))
	else:
		q = request.GET.get('q', 'emptiness')
		url = reverse('search', args = [q])
		return HttpResponseRedirect(url)

def blogs(request):
	needcache = Blog.objects.filter(lastcache__lte = datetime.datetime.now() - datetime.timedelta(0,600))
	for blog in needcache:
		f = urllib.urlopen(blog.url)
		blog.feedcache = f.read()
		blog.lastcache = datetime.datetime.now()
		blog.save()
		f.close()
	blogs = Blog.objects.all()
	entries = []
	blogsd = []
	for blog in blogs:
		channels = feedparser.parse(blog.feedcache.encode('utf-8', 'ignore'))
		blogsd.append({'title':blog.title,'url':channels.feed.link})
		for entry in channels.entries:
			et = entry.updated_parsed
			entrydate = datetime.datetime(et.tm_year, et.tm_mon, et.tm_mday, et.tm_hour, et.tm_hour, et.tm_min, et.tm_sec)
			entries.append({'title':entry.title,'summary':entry.summary,'url':entry.link,'date':entrydate, 'blogname':blog.title, 'blogurl':channels.feed.link})
	data = {'entries': sorted(entries, key=itemgetter('date'), reverse=True)[:20], 'blogs': blogsd}
	return render_to_response('articles/blogs.html', data, context_instance=RequestContext(request))
	
def gallery(request, slug):
	gallery = get_object_or_404(Gallery, slug__exact=slug)
	galleryimages = GalleryImageMeta.objects.filter(gallery=gallery).order_by('order')
	return render_to_response('galleries/gallery.html', {'gallery':gallery, 'galleryimages': galleryimages}, context_instance=RequestContext(request))

def jsongallery(request, slug):
	gallery = get_object_or_404(Gallery, slug__exact=slug)
	galleryimages = GalleryImageMeta.objects.filter(gallery=gallery).order_by('order')
	return render_to_response('galleries/gallery.json', {'gallery':gallery, 'galleryimages': galleryimages}, context_instance=RequestContext(request), mimetype="application/json")

def thisweek_list(request):
	thisweeks = ThisWeek.objects.published()
	return render_to_response('thisweek/index.html', {'thisweeks': thisweeks}, context_instance=RequestContext(request))
	
def thisweek_single(request, year, month, day):
	d_object = datetime.date(int(year), int(month), int(day))
	thisweek = get_object_or_404(ThisWeek, start_date=d_object)
	return render_to_response('thisweek/single.html', {'week': thisweek}, context_instance=RequestContext(request))