# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'StoryPostRelation', fields ['story', 'post']
        db.delete_unique('ltumble_storypostrelation', ['story_id', 'post_id'])

        # Deleting model 'StoryPostRelation'
        db.delete_table('ltumble_storypostrelation')

    def backwards(self, orm):
        # Adding model 'StoryPostRelation'
        db.create_table('ltumble_storypostrelation', (
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tumblelog.Post'], unique=True)),
            ('story', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lstory.Story'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('ltumble', ['StoryPostRelation'])

        # Adding unique constraint on 'StoryPostRelation', fields ['story', 'post']
        db.create_unique('ltumble_storypostrelation', ['story_id', 'post_id'])

    models = {
        
    }

    complete_apps = ['ltumble']