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
  def handle_task(self, id):
    """Verifies the task and then calles handle_task()"""
    if not id:
      return self.notfound()
    try:
      i = int(id)
      task = Task.get_by_id(i)
    except ValueError:
      return self.notfound()
    if not task:
      return self.notfound()
    if users.get_current_user() != task.user:
      return self.unauthorized()
    return task
    
  def notfound(self):
    response = Response('Page not found.')
    response.status_code = 404
    return response

  def unauthorized(self):
    response = Response('Access denied.')
    response.status_code = 401
    return response
    

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
    if not id:
      return self.notfound()
    context = self.get_context()
    context['title'] = 'Task'
    context['tasks'] = Task.fetch_all_active()
    try:
      i = int(id)
      task = Task.get_by_id(i)
      if task:
        if users.get_current_user() != task.user:
          return self.unauthorized()
        context['task'] = task
      else:
        return self.notfound()
      return self.render_response('task-edit.html', **context)
    except ValueError:
      return self.notfound()

  def post(self, id):
    """Updating"""
    if not id:
      return self.notfound()
    try:
      i = int(id)
      task = Task.get_by_id(i)
      if task:
        if users.get_current_user() != task.user:
          return self.unauthorized()
        task.is_archived = False
        task.save(self.request.form)
        return self.redirect_to('tasks')
      else:
        return self.notfound()
    except ValueError:
      return self.notfound()
      
  def delete(self, id):
    logging.warn(">>> task '%s' should be deleted" % id)
    try:
      i = int(id)
      task = Task.get_by_id(i)
      if task:
        if users.get_current_user() != task.user:
          return self.unauthorized()
        task.delete()
        return Response("Deleted.")
      else:
        return self.notfound()
    except ValueError:
      return self.notfound()
    

class TaskArchiveHandler(BaseHandler):
  def put(self, id):
    if not id:
      return self.notfound()
    try:
      i = int(id)
      task = Task.get_by_id(i)
      if task:
        if users.get_current_user() != task.user:
          return self.unauthorized()
        task.archive()
        return Response("Archived.")
      else:
        return self.notfound()
    except ValueError:
      return self.notfound()


class ArchiveHandler(BaseHandler):
  def get(self):
    context = self.get_context()
    context['title'] = 'Task Queue'
    context['tasks'] = Task.fetch_all_archived()
    return self.render_response('archive.html', **context)
