# -*- coding: utf-8 -*-
from sqlalchemy import (
    Column,
    Integer,
    String, UniqueConstraint, MetaData)

from sqlalchemy.ext.declarative import (
    declarative_base,
    declared_attr,
)

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

MAX_INDEX_NAME_LENGTH = 63


def uq_generate(constraint, table):
    str_tokens = [column.name for column in constraint.columns]
    key = hex(abs(hash((",".join(str_tokens).encode('ascii')))))[2:]
    length = MAX_INDEX_NAME_LENGTH - len(key) - 4
    return '{}_{}'.format(key, str_tokens[0][:length])


convention = {
    'uq_generate': uq_generate,
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(uq_generate)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s',
}


class Base(object):
    @declared_attr
    def __tablename__(cls):
        return '{}_{}'.format(cls.__module__.split('.')[0],
                              cls.__name__.lower())

    __table_args__ = {'mysql_engine': 'InnoDB'}

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=Base,
                        metadata=MetaData(naming_convention=convention))


class MyModel(Base):
    __table_args__ = (
        UniqueConstraint('att_a', 'att_b', 'att_c'),
    )

    name = Column(String(255), unique=True)

    att_a = Column(Integer, nullable=False)
    att_b = Column(Integer, nullable=False)
    att_c = Column(Integer, nullable=False)
