from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.core.urlresolvers import reverse
from review.models import Article, ThisWeek
import datetime

class LatestEntriesFeed(Feed):
	title = "The Oberlin Review"
	link = ''
	description = "The most recent Oberlin Review review."
	feed_type = Atom1Feed
	
	def items(self):
		return Article.objects.published().order_by('-web_date')[:20]
	
	def item_title(self, item):
		return item.title
	
	def item_description(self, item):
		return item.lede
		
	def item_link(self, item):
		return item.get_absolute_url()
		
	def item_pubdate(self, item):
		return item.web_date
		
	def item_author_name(self, item):
		author_list = item.authors.all()
		author_string = author_list[0].__unicode__()
		if author_list[1:]:
			for author in author_list[1:]:
				author_string += ', %s' % author.__unicode__()
		return author_string


class ThisWeekFeed(Feed):
	title = "This Week"
	link = ''
	description = "This Week: a weekly events roundup from the Oberlin Review."
	feed_type = Atom1Feed
	
	def items(self):
		return ThisWeek.objects.all()[:20]
	
	def item_title(self, item):
		return item.__unicode__()
	
	def item_link(self, item):
		return item.get_absolute_url()
	
	def item_pubdate(self, item):
		return datetime.datetime(item.start_date.year, item.start_date.month, item.start_date.day)
	
	def item_author_name(self, item):
		return u"Oberlin Review"