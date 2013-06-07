# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Program'
        db.create_table(u'automation_program', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'automation', ['Program'])

        # Adding model 'LogicBlock'
        db.create_table(u'automation_logicblock', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('program', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['automation.Program'])),
            ('type', self.gf('django.db.models.fields.IntegerField')()),
            ('function', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('x', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('y', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('_data', self.gf('django.db.models.fields.TextField')(default='{}')),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
        ))
        db.send_create_signal(u'automation', ['LogicBlock'])

        # Adding model 'Link'
        db.create_table(u'automation_link', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start', self.gf('django.db.models.fields.related.ForeignKey')(related_name='outputs', to=orm['automation.LogicBlock'])),
            ('end', self.gf('django.db.models.fields.related.ForeignKey')(related_name='inputs', to=orm['automation.LogicBlock'])),
        ))
        db.send_create_signal(u'automation', ['Link'])


    def backwards(self, orm):
        # Deleting model 'Program'
        db.delete_table(u'automation_program')

        # Deleting model 'LogicBlock'
        db.delete_table(u'automation_logicblock')

        # Deleting model 'Link'
        db.delete_table(u'automation_link')


    models = {
        u'automation.link': {
            'Meta': {'object_name': 'Link'},
            'end': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'inputs'", 'to': u"orm['automation.LogicBlock']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'outputs'", 'to': u"orm['automation.LogicBlock']"})
        },
        u'automation.logicblock': {
            'Meta': {'object_name': 'LogicBlock'},
            '_data': ('django.db.models.fields.TextField', [], {'default': "'{}'"}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True'}),
            'function': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'program': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['automation.Program']"}),
            'type': ('django.db.models.fields.IntegerField', [], {}),
            'x': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'y': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'automation.program': {
            'Meta': {'object_name': 'Program'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['automation']