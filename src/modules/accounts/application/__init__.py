import importlib

from lato import ApplicationModule

account_module = ApplicationModule("account")
importlib.import_module("modules.accounts.application.command")
importlib.import_module("modules.accounts.application.query")
importlib.import_module("modules.accounts.application.event")
