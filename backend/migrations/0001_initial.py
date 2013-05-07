# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Connector'
        db.create_table(u'backend_connector', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('backend', ['Connector'])

        # Adding model 'Floor'
        db.create_table(u'backend_floor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('backend', ['Floor'])

        # Adding model 'Room'
        db.create_table(u'backend_room', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('floor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['backend.Floor'])),
        ))
        db.send_create_signal('backend', ['Room'])

        # Adding model 'Device'
        db.create_table(u'backend_device', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('connector', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['backend.Connector'])),
            ('room', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['backend.Room'])),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=9)),
            ('status', self.gf('django.db.models.fields.CharField')(default='off', max_length=9)),
        ))
        db.send_create_signal('backend', ['Device'])

        # Adding model 'Scenario'
        db.create_table(u'backend_scenario', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('is_hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal('backend', ['Scenario'])

        # Adding model 'ScenarioDevice'
        db.create_table(u'backend_scenariodevice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['backend.Device'])),
            ('scenario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['backend.Scenario'])),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=9)),
        ))
        db.send_create_signal('backend', ['ScenarioDevice'])

        # Adding model 'Input'
        db.create_table(u'backend_input', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('protocol', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('data', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=9)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('backend', ['Input'])

        # Adding model 'Thermometer'
        db.create_table(u'backend_thermometer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('temperature', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('backend', ['Thermometer'])

        # Adding model 'Timer'
        db.create_table(u'backend_timer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('time', self.gf('django.db.models.fields.TimeField')()),
            ('monday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tuesday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('wednesday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('thursday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('friday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('saturday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sunday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('action', self.gf('django.db.models.fields.CharField')(default='off', max_length=9)),
        ))
        db.send_create_signal('backend', ['Timer'])

        # Adding model 'User'
        db.create_table(u'backend_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40, db_index=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('api_key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40, db_index=True)),
            ('allow_local', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('backend', ['User'])


    def backwards(self, orm):
        # Deleting model 'Connector'
        db.delete_table(u'backend_connector')

        # Deleting model 'Floor'
        db.delete_table(u'backend_floor')

        # Deleting model 'Room'
        db.delete_table(u'backend_room')

        # Deleting model 'Device'
        db.delete_table(u'backend_device')

        # Deleting model 'Scenario'
        db.delete_table(u'backend_scenario')

        # Deleting model 'ScenarioDevice'
        db.delete_table(u'backend_scenariodevice')

        # Deleting model 'Input'
        db.delete_table(u'backend_input')

        # Deleting model 'Thermometer'
        db.delete_table(u'backend_thermometer')

        # Deleting model 'Timer'
        db.delete_table(u'backend_timer')

        # Deleting model 'User'
        db.delete_table(u'backend_user')


    models = {
        'backend.connector': {
            'Meta': {'object_name': 'Connector'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'backend.device': {
            'Meta': {'object_name': 'Device'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'connector': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['backend.Connector']"}),
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'backend.input': {
            'Meta': {'object_name': 'Input'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'data': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
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
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40', 'db_index': 'True'})
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