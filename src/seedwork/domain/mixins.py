from .errors import BusinessRuleValidationException
from .rules import BusinessRule


def check_rule(rule: BusinessRule):
    if rule.is_broken():
        raise BusinessRuleValidationException(rule)


class BusinessRuleValidationMixin:
    @staticmethod
    def check_rule(rule: BusinessRule):
        check_rule(rule)
