# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Kind'
        db.create_table('assets_kind', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('assets', ['Kind'])

        # Adding model 'Image'
        db.create_table('assets_image', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('height', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('width', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('credit', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('caption', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('time_uploaded', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('time_taken', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('kind', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['assets.Kind'])),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=40, db_index=True)),
        ))
        db.send_create_signal('assets', ['Image'])


    def backwards(self, orm):
        
        # Deleting model 'Kind'
        db.delete_table('assets_kind')

        # Deleting model 'Image'
        db.delete_table('assets_image')


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
        }
    }

    complete_apps = ['assets']
