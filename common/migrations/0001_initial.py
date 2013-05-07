# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Furniture'
        db.create_table(u'common_furniture', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('floor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['backend.Floor'])),
            ('x1', self.gf('django.db.models.fields.IntegerField')()),
            ('y1', self.gf('django.db.models.fields.IntegerField')()),
            ('x2', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('y2', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['backend.Device'])),
        ))
        db.send_create_signal('common', ['Furniture'])

        # Adding model 'Plan'
        db.create_table(u'common_plan', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('floor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['backend.Floor'])),
            ('x', self.gf('django.db.models.fields.IntegerField')()),
            ('y', self.gf('django.db.models.fields.IntegerField')()),
            ('width', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('height', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('room', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['backend.Room'])),
        ))
        db.send_create_signal('common', ['Plan'])

        # Adding model 'Temp'
        db.create_table(u'common_temp', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('floor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['backend.Floor'])),
            ('x', self.gf('django.db.models.fields.IntegerField')()),
            ('y', self.gf('django.db.models.fields.IntegerField')()),
            ('thermometer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['backend.Thermometer'])),
        ))
        db.send_create_signal('common', ['Temp'])


    def backwards(self, orm):
        # Deleting model 'Furniture'
        db.delete_table(u'common_furniture')

        # Deleting model 'Plan'
        db.delete_table(u'common_plan')

        # Deleting model 'Temp'
        db.delete_table(u'common_temp')


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
        'backend.room': {
            'Meta': {'object_name': 'Room'},
            'floor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['backend.Floor']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'backend.thermometer': {
            'Meta': {'object_name': 'Thermometer'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'temperature': ('django.db.models.fields.FloatField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'common.furniture': {
            'Meta': {'object_name': 'Furniture'},
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['backend.Device']"}),
            'floor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['backend.Floor']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'x1': ('django.db.models.fields.IntegerField', [], {}),
            'x2': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'y1': ('django.db.models.fields.IntegerField', [], {}),
            'y2': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'common.plan': {
            'Meta': {'object_name': 'Plan'},
            'floor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['backend.Floor']"}),
            'height': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['backend.Room']"}),
            'width': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'x': ('django.db.models.fields.IntegerField', [], {}),
            'y': ('django.db.models.fields.IntegerField', [], {})
        },
        'common.temp': {
            'Meta': {'object_name': 'Temp'},
            'floor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['backend.Floor']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'thermometer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['backend.Thermometer']"}),
            'x': ('django.db.models.fields.IntegerField', [], {}),
            'y': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['common']