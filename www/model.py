#!/usr/bin/env python3
# coding:utf-8

import time
import uuid

from myorm import Model, StringField, BoolField, FloatField, TextField, IntField


def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)


class User(Model):
    __table__ = 'user'
    id = StringField(primary_key=True, default=next_id, col_type='varchar(50)')
    email = StringField(col_type='varchar(50)')
    password = StringField(col_type='varchar(50)')
    admin = BoolField()
    name = StringField(col_type='varchar(50)')
    image = StringField(col_type='varchar(500)')
    created_at = FloatField(default=time.time)


class Blog(Model):
    __table__ = 'blog'
    id = StringField(primary_key=True, default=next_id, col_type='varchar(50)')
    user_id = StringField(col_type='varchar(50)')
    user_name = StringField(col_type='varchar(50)')
    user_image = StringField(col_type='varchar(500)')
    cat_id = StringField(col_type='varchar(50)')
    cat_name = StringField(col_type='varchar(50)')
    view_count = IntField()
    title = StringField(col_type='varchar(50)')
    summary = StringField(col_type='varchar(200)')
    content = TextField()
    created_at = FloatField(default=time.time)


class Comment(Model):
    __table__ = 'comment'
    id = StringField(primary_key=True, default=next_id, col_type='varchar(50)')
    blog_id = StringField(col_type='varchar(50)')
    user_id = StringField(col_type='varchar(50)')
    user_name = StringField(col_type='varchar(50)')
    user_image = StringField(col_type='varchar(500)')
    content = TextField()
    created_at = FloatField(default=time.time)


class Category(Model):
    __table__ = 'category'
    id = StringField(primary_key=True, default=next_id, col_type='varchar(50)')
    name = StringField(col_type='varchar(50)')
    created_at = FloatField(default=time.time)
