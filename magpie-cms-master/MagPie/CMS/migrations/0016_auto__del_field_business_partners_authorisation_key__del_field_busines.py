# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Business_Partners.authorisation_key'
        db.delete_column(u'CMS_business_partners', 'authorisation_key')

        # Deleting field 'Business_Partners.slug'
        db.delete_column(u'CMS_business_partners', 'slug')

        # Deleting field 'Business_Partners.contact'
        db.delete_column(u'CMS_business_partners', 'contact')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Business_Partners.authorisation_key'
        raise RuntimeError("Cannot reverse this migration. 'Business_Partners.authorisation_key' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Business_Partners.authorisation_key'
        db.add_column(u'CMS_business_partners', 'authorisation_key',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Business_Partners.slug'
        raise RuntimeError("Cannot reverse this migration. 'Business_Partners.slug' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Business_Partners.slug'
        db.add_column(u'CMS_business_partners', 'slug',
                      self.gf('django.db.models.fields.SlugField')(max_length=255, unique=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Business_Partners.contact'
        raise RuntimeError("Cannot reverse this migration. 'Business_Partners.contact' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Business_Partners.contact'
        db.add_column(u'CMS_business_partners', 'contact',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


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
            'business_partner_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'max_length': '1'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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