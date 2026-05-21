from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index = True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    
    posts = relationship('Post', back_populates='author')

class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True, index = True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    author_id = Column(Integer, ForeignKey('users.id'))
    
    author = relationship('User', back_populates='posts')

class Comment(Base):
    __tablename__ = 'comments'
    
    id = Column(Integer, primary_key=True, index = True)
    body = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    post_id = Column(Integer, ForeignKey('posts.id'))
    author_id = Column(Integer, ForeignKey('users.id'))
    
    post = relationship('Post', back_populates='comments')
    author = relationship('User', back_populates='comments')

