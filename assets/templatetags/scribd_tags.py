import hashlib
import scribd


from django import template
from django.template.loader import render_to_string


from review.assets.models import ScribdDocument


SCRIBD_API_KEY = "3njeu4nsr159zdux8o3su"
SCRIBD_API_SECRET = "sec-8iira6nqg0dhq97kj4t3yb6oh"
SCRIBD_PUBLISHER_ID = "pub-45886588477078303396"


register = template.Library()


@register.simple_tag
def scribd_embed(file):
	file_contents = file.read()
	key = hashlib.sha512(file_contents).hexdigest()
	try:
		document = ScribdDocument.objects.get(key=key)
	except:
		scribd.config(SCRIBD_API_KEY, SCRIBD_API_SECRET)
		uploaded = scribd.api_user.upload(open(file.path, 'rb'), access='private')
		attributes = uploaded.get_attributes()
		document = ScribdDocument(
			key = key,
			document_id = attributes['doc_id'],
			access_key = attributes['access_key'],
			secret_password = attributes['secret_password']
		)
		document.full_clean()
		document.save()
	return render_to_string('review/assets/scribd_embed.html', {'document': document})