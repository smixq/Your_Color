import datetime
import sqlalchemy
from flask_login import UserMixin

from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash


class Liked_plattes(SqlAlchemyBase):
    __tablename__ = 'liked_plattes'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    id_platte = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    id_user = sqlalchemy.Column(sqlalchemy.Integer, index=True, nullable=True)
    # email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    # hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # avatar = sqlalchemy.Column(sqlalchemy.BLOB, index=True, nullable=True)