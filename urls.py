from django.conf.urls.defaults import patterns, include, url
from review.feeds import LatestEntriesFeed, ThisWeekFeed
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('review.views',
	url(r'^article/(?P<article_slug>[\w-]+)/$', 'single'),
	url(r'^article/(?P<article_slug>[\w-]+)/comments/$', 'comments'),
	url(r'^feed/$', LatestEntriesFeed()),
	url(r'^section/(?P<section_slug>\w+)/$', 'section'),
	url(r'^author/(?P<author_id>\d+)/$','author'),
	url(r'^search/$','search', name="search"),
	url(r'^search/(?P<q>[^/]+)/$', 'search', name="search"),
	url(r'^blogs/$','blogs'),
	url(r'^gallery/(?P<slug>[\w-]+)/$', 'gallery', name="gallery"),
	url(r'^gallery/(?P<slug>[\w-]+)\.slideshow$', 'jsongallery', name="gallery"),
	
	url(r'^thisweek/$', 'thisweek_list', name="review-thisweek"),
	url(r'^thisweek/feed/$', ThisWeekFeed(), name="review-thisweek-feed"),
	url(r'^thisweek/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/(?P<day>[0-9]{1,2})/$', 'thisweek_single', name="review-thisweek-single"),
	
        url(r'^admin/', include(admin.site.urls)),
# Added by luke to fix comments
	url(r'comments/', include('django.contrib.comments.urls')),

	url(r'^$', 'index'),
) + patterns('django.views.generic',
	url(r'blogs/tumblr_embed[/?]$', 'simple.direct_to_template', {'template': 'miscellanea/tumblr.html'}),
	url(r'favicon\.ico$', 'simple.redirect_to', {'url': 'http://static.oberlinreview.org/favicon.ico'}),
) + patterns('', 
	url(r'^grappelli/', include('grappelli.urls')),
)
