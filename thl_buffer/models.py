#!/usr/bin/env python
# encoding: utf-8

import urllib
import logging

from google.appengine.ext import db
from google.appengine.api import users

class Task(db.Model):
  path = db.StringProperty(indexed=False, default="/inbox/tasks")
  title = db.StringProperty(indexed=False)
  notes = db.TextProperty(indexed=False)
  url = db.StringProperty(indexed=False)
  start_date = db.StringProperty(indexed=False)
  due_date = db.StringProperty(indexed=False)
  estimated_time = db.StringProperty(indexed=False)
  priority = db.IntegerProperty(indexed=False)
  is_archived = db.BooleanProperty(default=False)
  user = db.UserProperty(auto_current_user_add=True)
  created = db.DateTimeProperty(auto_now_add=True, indexed=False)
  updated = db.DateTimeProperty(auto_now=True)
  
  def get_thl_uri(self):
    """{{ task.title|urlencode }}&notes={{ task.notes|urlencode }}&url={{ task.url|urlencode }}&startDate={{ task.start_date|urlencode }}&dueDate={{ task.due_date|urlencode }}"""
    if not self.title:
      return None
    if not self.path:
      logging.warn('None')
      self.path = "/inbox/tasks"
    uri = "thehitlist://%s?method=POST&title=%s" % (self.path, urllib.quote(self.title.encode('utf-8')))
    if self.notes:
      uri += "&notes=%s" % urllib.quote(self.notes.encode('utf-8'))
    if self.url:
      uri += "&url=%s" % urllib.quote(self.url.encode('utf-8'))
    if self.start_date:
      uri += "&startDate=%s" % urllib.quote(self.start_date.encode('utf-8'))
    if self.due_date:
      uri += "&dueDate=%s" % urllib.quote(self.due_date.encode('utf-8'))
    if self.estimated_time:
      uri += "&estimatedTime=%s" % urllib.quote(self.estimated_time.encode('utf-8'))
    if self.priority:
      uri += "&priority=%s" % urllib.quote(str(self.priority))
    return uri
  
  def archive(self):
    if not self.is_archived:
      self.is_archived = True
      self.put()
      
  def save(self, requestform):
    self.title = requestform.get('title')
    self.path = requestform.get('path')
    self.url = requestform.get('url')
    self.notes = requestform.get('notes')
    self.start_date = requestform.get('start_date')
    self.due_date = requestform.get('due_date')
    self.put()
  
  @classmethod
  def fetch_all_active(self):
    return self.fetch_all(False)

  @classmethod
  def fetch_all_archived(self):
    return self.fetch_all(True)
  
  @classmethod
  def fetch_all(self, is_archived=False):
    user = users.get_current_user()
    if user:
      query = self.all()
      query.filter('is_archived = ', is_archived)
      query.filter('user = ', user)
      query.order('updated')
      return query.fetch(100)
  