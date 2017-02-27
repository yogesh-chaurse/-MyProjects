# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Business_Partners.business_partner_id'
        db.add_column(u'CMS_business_partners', 'business_partner_id',
                      self.gf('django.db.models.fields.CharField')(default=datetime.datetime(2015, 2, 20, 0, 0), max_length=255),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Business_Partners.business_partner_id'
        db.delete_column(u'CMS_business_partners', 'business_partner_id')


    models = {
        u'CMS.business_partner_regions': {
            'Meta': {'object_name': 'Business_Partner_Regions'},
            'business_partner': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'region_of'", 'unique': 'True', 'to': u"orm['CMS.Business_Partners']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'max_length': '1'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'business_partner_of'", 'unique': 'True', 'to': u"orm['CMS.Regions']"})
        },
        u'CMS.business_partners': {
            'Meta': {'object_name': 'Business_Partners'},
            'authorisation_key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'business_partner_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'contact': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'max_length': '1'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'CMS.regions': {
            'Meta': {'object_name': 'Regions'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'max_length': '1'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'CMS.themes': {
            'Meta': {'object_name': 'Themes'},
            'business_partner': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'theme_of'", 'unique': 'True', 'to': u"orm['CMS.Business_Partners']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'font_color': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'max_length': '1'}),
            'is_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'max_length': '1'}),
            'logo': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'splash_screen': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'theme_color': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['CMS']