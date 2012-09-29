# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table('vote_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('vote', ['Category'])

        # Adding model 'Menu'
        db.create_table('vote_menu', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(unique=True)),
        ))
        db.send_create_signal('vote', ['Menu'])

        # Adding model 'Meal'
        db.create_table('vote_meal', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('menu', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vote.Menu'])),
        ))
        db.send_create_signal('vote', ['Meal'])

        # Adding M2M table for field categories on 'Meal'
        db.create_table('vote_meal_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('meal', models.ForeignKey(orm['vote.meal'], null=False)),
            ('category', models.ForeignKey(orm['vote.category'], null=False))
        ))
        db.create_unique('vote_meal_categories', ['meal_id', 'category_id'])

        # Adding model 'Vote'
        db.create_table('vote_vote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('meal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vote.Meal'])),
            ('rating', self.gf('django.db.models.fields.SmallIntegerField')()),
        ))
        db.send_create_signal('vote', ['Vote'])

        # Adding model 'VoteEvent'
        db.create_table('vote_voteevent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('room_number', self.gf('django.db.models.fields.IntegerField')()),
            ('meal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vote.Meal'])),
        ))
        db.send_create_signal('vote', ['VoteEvent'])

        # Adding unique constraint on 'VoteEvent', fields ['room_number', 'meal']
        db.create_unique('vote_voteevent', ['room_number', 'meal_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'VoteEvent', fields ['room_number', 'meal']
        db.delete_unique('vote_voteevent', ['room_number', 'meal_id'])

        # Deleting model 'Category'
        db.delete_table('vote_category')

        # Deleting model 'Menu'
        db.delete_table('vote_menu')

        # Deleting model 'Meal'
        db.delete_table('vote_meal')

        # Removing M2M table for field categories on 'Meal'
        db.delete_table('vote_meal_categories')

        # Deleting model 'Vote'
        db.delete_table('vote_vote')

        # Deleting model 'VoteEvent'
        db.delete_table('vote_voteevent')


    models = {
        'vote.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'vote.meal': {
            'Meta': {'object_name': 'Meal'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['vote.Category']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'menu': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vote.Menu']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'vote.menu': {
            'Meta': {'object_name': 'Menu'},
            'date': ('django.db.models.fields.DateField', [], {'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'vote.vote': {
            'Meta': {'object_name': 'Vote'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vote.Meal']"}),
            'rating': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        'vote.voteevent': {
            'Meta': {'unique_together': "(('room_number', 'meal'),)", 'object_name': 'VoteEvent'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vote.Meal']"}),
            'room_number': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['vote']