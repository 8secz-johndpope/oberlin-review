# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Tag'
        db.create_table('review_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('review', ['Tag'])

        # Adding model 'Issue'
        db.create_table('review_issue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('volume', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('review', ['Issue'])

        # Adding model 'Section'
        db.create_table('review_section', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('review', ['Section'])

        # Adding model 'Article'
        db.create_table('review_article', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('issue', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='articles', null=True, to=orm['review.Issue'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('web_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('print_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('lede', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('full_text', self.gf('django.db.models.fields.TextField')()),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(related_name='articles', to=orm['review.Section'])),
        ))
        db.send_create_signal('review', ['Article'])

        # Adding M2M table for field authors on 'Article'
        db.create_table('review_article_authors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('article', models.ForeignKey(orm['review.article'], null=False)),
            ('author', models.ForeignKey(orm['review.author'], null=False))
        ))
        db.create_unique('review_article_authors', ['article_id', 'author_id'])

        # Adding M2M table for field tags on 'Article'
        db.create_table('review_article_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('article', models.ForeignKey(orm['review.article'], null=False)),
            ('tag', models.ForeignKey(orm['review.tag'], null=False))
        ))
        db.create_unique('review_article_tags', ['article_id', 'tag_id'])

        # Adding M2M table for field images on 'Article'
        db.create_table('review_article_images', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('article', models.ForeignKey(orm['review.article'], null=False)),
            ('image', models.ForeignKey(orm['images.image'], null=False))
        ))
        db.create_unique('review_article_images', ['article_id', 'image_id'])

        # Adding model 'FrontPage'
        db.create_table('review_frontpage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('media1_content_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='front_page_media1', null=True, to=orm['contenttypes.ContentType'])),
            ('media1_object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('media2_content_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='front_page_media2', null=True, to=orm['contenttypes.ContentType'])),
            ('media2_object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('story1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='front_page_story1', to=orm['review.Article'])),
            ('story2', self.gf('django.db.models.fields.related.ForeignKey')(related_name='front_page_story2', to=orm['review.Article'])),
            ('story3', self.gf('django.db.models.fields.related.ForeignKey')(related_name='front_page_story3', to=orm['review.Article'])),
            ('teaser1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='front_page_teaser1', to=orm['review.Article'])),
            ('teaser2', self.gf('django.db.models.fields.related.ForeignKey')(related_name='front_page_teaser2', to=orm['review.Article'])),
            ('teaser3', self.gf('django.db.models.fields.related.ForeignKey')(related_name='front_page_teaser3', to=orm['review.Article'])),
            ('teaser4', self.gf('django.db.models.fields.related.ForeignKey')(related_name='front_page_teaser4', to=orm['review.Article'])),
        ))
        db.send_create_signal('review', ['FrontPage'])

        # Adding model 'Author'
        db.create_table('review_author', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('display_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('bio', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('photo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['images.Image'], null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, null=True, blank=True)),
        ))
        db.send_create_signal('review', ['Author'])

        # Adding model 'Blog'
        db.create_table('review_blog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('feedcache', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('lastcache', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('review', ['Blog'])

        # Adding model 'Gallery'
        db.create_table('review_gallery', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=40, db_index=True)),
        ))
        db.send_create_signal('review', ['Gallery'])

        # Adding model 'GalleryImageMeta'
        db.create_table('review_galleryimagemeta', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('caption', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(related_name='gallerymetas', to=orm['images.Image'])),
            ('gallery', self.gf('django.db.models.fields.related.ForeignKey')(related_name='imagedatas', to=orm['review.Gallery'])),
        ))
        db.send_create_signal('review', ['GalleryImageMeta'])


    def backwards(self, orm):
        
        # Deleting model 'Tag'
        db.delete_table('review_tag')

        # Deleting model 'Issue'
        db.delete_table('review_issue')

        # Deleting model 'Section'
        db.delete_table('review_section')

        # Deleting model 'Article'
        db.delete_table('review_article')

        # Removing M2M table for field authors on 'Article'
        db.delete_table('review_article_authors')

        # Removing M2M table for field tags on 'Article'
        db.delete_table('review_article_tags')

        # Removing M2M table for field images on 'Article'
        db.delete_table('review_article_images')

        # Deleting model 'FrontPage'
        db.delete_table('review_frontpage')

        # Deleting model 'Author'
        db.delete_table('review_author')

        # Deleting model 'Blog'
        db.delete_table('review_blog')

        # Deleting model 'Gallery'
        db.delete_table('review_gallery')

        # Deleting model 'GalleryImageMeta'
        db.delete_table('review_galleryimagemeta')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'images.image': {
            'Meta': {'object_name': 'Image'},
            'caption': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'credit': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'kind': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['images.Kind']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '40', 'db_index': 'True'}),
            'time_taken': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'time_uploaded': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'images.kind': {
            'Meta': {'object_name': 'Kind'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'review.article': {
            'Meta': {'object_name': 'Article'},
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['review.Author']", 'symmetrical': 'False'}),
            'full_text': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'articles'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['images.Image']"}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'articles'", 'null': 'True', 'to': "orm['review.Issue']"}),
            'lede': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'print_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'articles'", 'to': "orm['review.Section']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'articles'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['review.Tag']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'web_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'review.author': {
            'Meta': {'object_name': 'Author'},
            'bio': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['images.Image']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'review.blog': {
            'Meta': {'object_name': 'Blog'},
            'feedcache': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastcache': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'review.frontpage': {
            'Meta': {'object_name': 'FrontPage'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media1_content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'front_page_media1'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'media1_object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'media2_content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'front_page_media2'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'media2_object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'story1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'front_page_story1'", 'to': "orm['review.Article']"}),
            'story2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'front_page_story2'", 'to': "orm['review.Article']"}),
            'story3': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'front_page_story3'", 'to': "orm['review.Article']"}),
            'teaser1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'front_page_teaser1'", 'to': "orm['review.Article']"}),
            'teaser2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'front_page_teaser2'", 'to': "orm['review.Article']"}),
            'teaser3': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'front_page_teaser3'", 'to': "orm['review.Article']"}),
            'teaser4': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'front_page_teaser4'", 'to': "orm['review.Article']"})
        },
        'review.gallery': {
            'Meta': {'object_name': 'Gallery'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'galleries'", 'symmetrical': 'False', 'through': "orm['review.GalleryImageMeta']", 'to': "orm['images.Image']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '40', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'review.galleryimagemeta': {
            'Meta': {'ordering': "['order']", 'object_name': 'GalleryImageMeta'},
            'caption': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'gallery': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'imagedatas'", 'to': "orm['review.Gallery']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'gallerymetas'", 'to': "orm['images.Image']"}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'review.issue': {
            'Meta': {'object_name': 'Issue'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'volume': ('django.db.models.fields.IntegerField', [], {})
        },
        'review.section': {
            'Meta': {'object_name': 'Section'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'review.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        }
    }

    complete_apps = ['review']
