from review.models import Blog

def review(request):
	blogs = Blog.objects.all()
	blogsd = []
	for blog in blogs:
		# slicing the /rss off the URL is hacky, but I am lazy tonight. FIX LATER
		blogsd.append({'title':blog.title,'url':blog.url[:-3]})
	return {'blogs': blogsd}