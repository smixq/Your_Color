import datetime
import sqlalchemy
from sqlalchemy.util.preloaded import orm

from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash


class Liked_palettes(SqlAlchemyBase):
    __tablename__ = 'liked_palettes'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    id_palette = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("saved_palettes.id"))
    id_user = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now())
    user = orm.relationship('User')
    palette = orm.relationship('Saved_palettes')
    # email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    # hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # avatar = sqlalchemy.Column(sqlalchemy.BLOB, index=True, nullable=True)