# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'ScribdDocument.key'
        db.alter_column('assets_scribddocument', 'key', self.gf('django.db.models.fields.TextField')(unique=True, max_length=255))

        # Adding unique constraint on 'ScribdDocument', fields ['key']
        db.create_unique('assets_scribddocument', ['key'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'ScribdDocument', fields ['key']
        db.delete_unique('assets_scribddocument', ['key'])

        # Changing field 'ScribdDocument.key'
        db.alter_column('assets_scribddocument', 'key', self.gf('django.db.models.fields.CharField')(max_length=255))


    models = {
        'assets.image': {
            'Meta': {'object_name': 'Image'},
            'caption': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'credit': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'kind': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['assets.Kind']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '40', 'db_index': 'True'}),
            'time_taken': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'time_uploaded': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'assets.kind': {
            'Meta': {'object_name': 'Kind'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'assets.scribddocument': {
            'Meta': {'object_name': 'ScribdDocument'},
            'access_key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'document_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.TextField', [], {'unique': 'True', 'max_length': '255'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'secret_password': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['assets']
