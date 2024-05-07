from modules.accounts.domain.entities import Account
from seedwork.infra.repository import SqlAlchemyRepository


class AccountSqlAlchemyRepository(SqlAlchemyRepository):
    entity_class = Account
