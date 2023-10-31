import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, People as PeopleModel, Transactions as TransactionModel


class People(SQLAlchemyObjectType):
    class Meta:
        model = PeopleModel
        interfaces = (relay.Node, )

class Transaction(SQLAlchemyObjectType):
    class Meta:
        model = TransactionModel
        interfaces = (relay.Node, )

class Query(graphene.ObjectType):
    node = relay.Node.Field()

    all_people = SQLAlchemyConnectionField(People.connection)
    all_transactions = SQLAlchemyConnectionField(Transaction.connection)

schema = graphene.Schema(query=Query)