# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Dynamic_Contents', fields ['language']
        db.delete_unique(u'CMS_dynamic_contents', ['language_id'])


        # Changing field 'Dynamic_Contents.language'
        db.alter_column(u'CMS_dynamic_contents', 'language_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['CMS.Languages']))

    def backwards(self, orm):

        # Changing field 'Dynamic_Contents.language'
        db.alter_column(u'CMS_dynamic_contents', 'language_id', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['CMS.Languages']))
        # Adding unique constraint on 'Dynamic_Contents', fields ['language']
        db.create_unique(u'CMS_dynamic_contents', ['language_id'])


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
        u'CMS.dynamic_contents': {
            'Meta': {'object_name': 'Dynamic_Contents'},
            'content': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_of'", 'to': u"orm['CMS.Institutions']"}),
            'content_type': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '2'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'max_length': '1'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'language_of'", 'to': u"orm['CMS.Languages']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'CMS.institutions': {
            'Meta': {'object_name': 'Institutions'},
            'contact_no': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'direct_claim_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'max_length': '1'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructional_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'max_length': '1'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'postal_address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'CMS.languages': {
            'Meta': {'object_name': 'Languages'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'max_length': '1'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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