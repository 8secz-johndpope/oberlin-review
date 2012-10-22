from django.db import models

class ScribdDocument(models.Model):
	key = models.TextField(max_length=255)
	document_id = models.CharField(max_length=255)
	access_key = models.CharField(max_length=255)
	secret_password = models.CharField(max_length=255)
	added = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	
	class Meta:
		app_label = 'assets'