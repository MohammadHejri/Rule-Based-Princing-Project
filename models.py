import enum
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship
from database import Base


class RuleType(enum.Enum):
    DISCOUNT = "DISCOUNT"
    MARKUP = "MARKUP"


class UserType(enum.Enum):
    B2B = "B2B"
    B2C = "B2C"


class Rule(Base):
    __tablename__ = "rules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(Enum(RuleType), index=True)

    action = relationship("Action")
    conditions = relationship("Condition")

    def __repr__(self):
        return f"Rule(id={self.id}|name={self.name}|type={self.type})"


class Condition(Base):
    __tablename__ = "conditions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ruleId = Column(Integer, ForeignKey("rules.id"))
    userType = Column(Enum(UserType), index=True)
    minPrice = Column(Integer, index=True)

    rule = relationship("Rule", back_populates="conditions")

    def __repr__(self):
        return f"Condition(id={self.id}|ruleId={self.ruleId}|userType={self.userType})"


class Action(Base):
    __tablename__ = "actions"

    id = Column(Integer, primary_key=True, index=True)
    ruleId = Column(Integer, ForeignKey("rules.id"))
    f = Column(Integer, index=True)
    p = Column(Integer, index=True)
    m = Column(Integer, index=True)

    rule = relationship("Rule", back_populates="action")

    def __repr__(self):
        return f"Action(id={self.id}|ruleId={self.ruleId}|f={self.f}|p={self.p}|m={self.m})"


class ApplicantItem:

    def __init__(self, userType, price):
        self.userType = userType
        self.price = price


class ApplyResponse:

    def __init__(self, applied, appliedRules):
        self.applied = applied
        self.appliedRules = appliedRules


class AppliedRule:

    def __init__(self, id, name, sequence, oldPrice, newPrice, displacement):
        self.id = id
        self.name = name
        self.sequence = sequence
        self.oldPrice = oldPrice
        self.newPrice = newPrice
        self.displacement = displacement
