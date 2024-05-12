import importlib

from seedwork.application.application import ApplicationModule

notifications_module = ApplicationModule("notifications")
importlib.import_module("modules.notifications.application.event")
