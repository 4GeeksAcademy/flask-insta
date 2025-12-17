from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(
        String(120), nullable=False)
    lastname: Mapped[str] = mapped_column(
        String(120), nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)

    posts: Mapped[list["Post"]] = relationship(back_populates="user")
    comments: Mapped[list["Comment"]] = relationship(back_populates="author")
    followers: Mapped[list["Follower"]] = relationship(
        foreign_keys='Follower.user_to_id', back_populates="user_followed")
    following: Mapped[list["Follower"]] = relationship(
        foreign_keys='Follower.user_from_id', back_populates="user_follower")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "user": self.user,
            # do not serialize the password, its a security breach
        }


class Follower(db.Model):
    __tablename__ = 'follower'
    user_from_id: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key = True)
    user_to_id: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key = True)

    user_follower: Mapped["User"] = relationship(foreign_keys=[user_from_id], back_populates="following")
    user_followed: Mapped["User"] = relationship(foreign_keys=[user_to_id], back_populates="followers")


class Media(db.Model):
    __tablename__ = 'media'
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(120), nullable=False)
    url: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)

    post: Mapped["Post"] = relationship(back_populates="media")


class Comment(db.Model):
    __tablename__ = 'comment'
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(120), nullable=False)

    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)

    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)

    author: Mapped["User"] = relationship(back_populates="comments")
    post: Mapped["Post"] = relationship(back_populates="comments")


class Post(db.Model):
    __tablename__ = 'post'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    user: Mapped["User"] = relationship(back_populates="posts")

    media: Mapped[list["Media"]] = relationship(back_populates="post")
    comments: Mapped[list["Comment"]] = relationship(back_populates="post")
