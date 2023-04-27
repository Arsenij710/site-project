import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Products(SqlAlchemyBase):
    __tablename__ = 'products'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    author = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    category = sqlalchemy.Column(sqlalchemy.Integer,
                              nullable=True)
    image = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    favourites = orm.relationship("Favourites", back_populates='product')
    def __repr__(self):
        return f'{self.name}  {self.price}  {self.description}  {self.image}'
