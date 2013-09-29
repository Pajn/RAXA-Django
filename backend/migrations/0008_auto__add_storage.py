# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Storage'
        db.create_table(u'backend_storage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('owner', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('_data', self.gf('django.db.models.fields.TextField')(default='{}')),
        ))
        db.send_create_signal('backend', ['Storage'])


    def backwards(self, orm):
        # Deleting model 'Storage'
        db.delete_table(u'backend_storage')


    models = {
        'backend.connector': {
            'Meta': {'object_name': 'Connector'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'backend.device': {
            'Meta': {'object_name': 'Device'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'connector': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['backend.Connector']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['backend.Room']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'off'", 'max_length': '9'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'backend.floor': {
            'Meta': {'object_name': 'Floor'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'viewbox': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'backend.input': {
            'Meta': {'object_name': 'Input'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True'}),
            'data': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'protocol': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'backend.room': {
            'Meta': {'object_name': 'Room'},
            'floor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['backend.Floor']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'backend.scenario': {
            'Meta': {'object_name': 'Scenario'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'backend.scenariodevice': {
            'Meta': {'object_name': 'ScenarioDevice'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['backend.Device']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'scenario': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['backend.Scenario']"})
        },
        'backend.storage': {
            'Meta': {'object_name': 'Storage'},
            '_data': ('django.db.models.fields.TextField', [], {'default': "'{}'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'owner': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'backend.thermometer': {
            'Meta': {'object_name': 'Thermometer'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'temperature': ('django.db.models.fields.FloatField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'backend.timer': {
            'Meta': {'object_name': 'Timer'},
            'action': ('django.db.models.fields.CharField', [], {'default': "'off'", 'max_length': '9'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'friday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'saturday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sunday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'thursday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'time': ('django.db.models.fields.TimeField', [], {}),
            'tuesday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'wednesday': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'backend.user': {
            'Meta': {'object_name': 'User'},
            'allow_local': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'api_key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'theme': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['common.Theme']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40', 'db_index': 'True'})
        },
        'common.theme': {
            'Meta': {'object_name': 'Theme'},
            'builtin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'css': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
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

    complete_apps = ['backend']