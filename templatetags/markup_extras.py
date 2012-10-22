from django.template.defaultfilters import stringfilter
from django import template
from django.template.loader import render_to_string
from review.assets.models import Image
import re

register = template.Library()

@register.filter(name='title')
@stringfilter
def title(value):
	newvalue = re.sub(r"\*\*(.*)\*\*", r"<strong>\g<1></strong>", value)
	return re.sub("\*(.*)\*",  r"<em>\g<1></em>", newvalue)

def replace_images(matchobj):
	slug = matchobj.group('slug')
	image = Image.objects.filter(slug__exact=slug)[0]
	return render_to_string('articles/embedded_image.html', {'image':image, 'MEDIA_URL':'http://boson.csr.oberlin.edu/review_static/'})

@register.filter(name='formatimages')
@stringfilter
def title(value):
	return re.sub(r'\[\[(?P<slug>[-\w]+)\]\]', replace_images, value)