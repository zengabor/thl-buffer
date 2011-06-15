# -*- coding: utf-8 -*-

import logging
from google.appengine.api import users

from tipfy.app import Response
from tipfy.handler import RequestHandler
from tipfyext.jinja2 import Jinja2Mixin
from tipfy.auth import user_required
from tipfy.auth.google import GoogleMixin

import logging
import re

from models import Task

class BaseHandler(RequestHandler, Jinja2Mixin, GoogleMixin):
  def get_context(self):
    context = {
      'handler': self.__class__.__name__,
    }
    user = users.get_current_user()
    if user:
      context['user'] = user
      context['logouturl'] = users.create_logout_url(self.request.path)
    else:
      context['loginurl'] = users.create_login_url(self.request.path)
    return context
    
class BaseTaskHandler(BaseHandler):
  def get_task(self, id):
    """Verifies the task and then calles handle_task()"""
    if not id:
      self.abort(404)
    try:
      i = int(id)
      task = Task.get_by_id(i)
    except ValueError:
      self.abort(404)
    if not task:
      self.abort(404)
    if users.get_current_user() != task.user:
      self.abort(401)
    return task


class WelcomeHandler(BaseHandler):
  def get(self):
    if (users.get_current_user()):
      referer = self.request.headers.get('Referer')
      domain = self.request.host
      if referer is None or not re.match("^https?://%s/" % re.escape(domain), referer):
        return self.redirect_to('tasks')
    context = self.get_context()
    context['title'] = 'Welcome'
    return self.render_response('welcome.html', **context)


class TaskListHandler(BaseHandler):
  def get(self):
    context = self.get_context()
    context['title'] = 'Task Queue'
    context['tasks'] = Task.fetch_all_active()
    return self.render_response('tasks.html', **context)    

  def post(self):
    """creates new task"""
    if self.request.form.get('title'):
      task = Task()
      task.save(self.request.form)

    return self.redirect_to('tasks')


class TaskHandler(BaseTaskHandler):
  def get(self, id):
    context = self.get_context()
    context['title'] = 'Task'
    context['tasks'] = Task.fetch_all_active()
    context['task'] = self.get_task(id)
    return self.render_response('task-edit.html', **context)

  def post(self, id):
    """Updating"""
    task = self.get_task(id)
    task.is_archived = False
    task.save(self.request.form)
    return self.redirect_to('tasks')
      
  def delete(self, id):
    task = self.get_task(id)
    task.delete()
    return Response("Deleted.")
    

class TaskArchiveHandler(BaseTaskHandler):
  def put(self, id):
    task = self.get_task(id)
    task.archive()
    return Response("Archived.")


class ArchiveHandler(BaseHandler):
  def get(self):
    context = self.get_context()
    context['title'] = 'Task Queue'
    context['tasks'] = Task.fetch_all_archived()
    return self.render_response('archive.html', **context)
