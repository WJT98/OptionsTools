# coding=utf-8
from .entity import Entity, Base
from sqlalchemy import Column, String

from marshmallow import Schema, fields


class Ticker(Entity, Base):
	__tablename__ = 'tickers'
	ticker = Column(String, primary_key=True)

class TickerSchema(Schema):
    ticker = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()