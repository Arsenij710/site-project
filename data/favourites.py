import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Favourites(SqlAlchemyBase):
    __tablename__ = 'favourites'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    book_name = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("products.name"))
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User')
    product = orm.relationship('Products')


    def __repr__(self):
        return f'{self.user_name}  {self.book_name}'


