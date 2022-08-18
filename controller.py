from models import *
from database import *


class Controller:

    def __init__(self):
        self.session = createNewSession()

    def respond(self, applicantItem):
        self.appliedRulesSequence = []
        rules = self.getAllRules()
        for rule in rules:
            ruleSatisfied = True
            for condition in rule.conditions:
                conditionSatisfied = self.checkCondition(condition, applicantItem)
                if not conditionSatisfied:
                    ruleSatisfied = False
                    break
            if ruleSatisfied:
                self.applyRule(rule, applicantItem.price)
        applied = len(self.appliedRulesSequence) > 0
        response = ApplyResponse(applied, self.appliedRulesSequence)
        return response

    def getAllRules(self):
        return self.session.query(Rule).all()

    def checkCondition(self, condition, applicantItem):
        return condition.userType == applicantItem.userType and applicantItem.price >= condition.minPrice

    def applyRule(self, rule, applicantItemPrice):
        sequence = len(self.appliedRulesSequence)
        oldPrice = self.getOldPrice(applicantItemPrice)
        displacement = self.getDisplacement(rule.action[0], oldPrice)
        newPrice = self.getNewPrice(rule.type, oldPrice, displacement)
        appliedRule = AppliedRule(rule.id, rule.name, sequence, oldPrice, newPrice, displacement)
        self.appliedRulesSequence.append(appliedRule)

    def getOldPrice(self, applicantItemPrice):
        if len(self.appliedRulesSequence) > 0:
            return self.appliedRulesSequence[-1].newPrice
        return applicantItemPrice

    def getDisplacement(self, action, oldPrice):
        return min(action.f + oldPrice * action.p / 100, action.m)

    def getNewPrice(self, ruleType, oldPrice, displacement):
        if ruleType == RuleType.MARKUP:
            return oldPrice + displacement
        elif ruleType == RuleType.DISCOUNT:
            return oldPrice - displacement
