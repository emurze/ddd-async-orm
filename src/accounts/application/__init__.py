import importlib

from accounts.infra.tables import start_mappers
from seedwork.application.application import ApplicationModule

accounts_module = ApplicationModule("account")
accounts_module.register_mapper(start_mappers)
importlib.import_module("accounts.application.command")
importlib.import_module("accounts.application.query")
importlib.import_module("accounts.application.event")
