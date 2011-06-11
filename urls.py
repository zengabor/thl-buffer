# -*- coding: utf-8 -*-
"""URL definitions."""
from tipfy.routing import Rule, HandlerPrefix

rules = [
  HandlerPrefix('thl_buffer.handlers.', [
    Rule('/', name='welcome', handler='WelcomeHandler'),
    Rule('/tasks', name='tasks', handler='TaskListHandler'),
    Rule('/tasks/<id>', name='task', handler='TaskHandler'),
    Rule('/tasks/<id>/archive', name='archive-task', handler='TaskArchiveHandler'),
    Rule('/archive', name='archive', handler='ArchiveHandler'),
  ]),
]
