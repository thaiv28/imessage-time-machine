from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from estherandthai import db
from flask_login import UserMixin
import datetime
from sqlalchemy.ext.hybrid import hybrid_method


class User(UserMixin, db.Model):
    __tablename__ = "user"
    
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(32), unique=True,
                                                index=True)
    password: so.Mapped[str] = so.mapped_column(sa.String(120))
    
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
class Message(db.Model):
    __tablename__ = "message"
    
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    meta: so.Mapped[str] = so.mapped_column(sa.String(100))
    reply: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5000))
    text: so.Mapped[str] = so.mapped_column(sa.String(5000))
    
    date: so.Mapped[datetime.date] = so.mapped_column(index=True)
    time: so.Mapped[datetime.time] = so.mapped_column(index=True)
    dt: so.Mapped[datetime.datetime] = so.mapped_column(index=True)
    next_date: so.Mapped[Optional[datetime.date]] = so.mapped_column(index=True)
    
    name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(50))
    reaction: so.Mapped[bool]
    image: so.Mapped[bool]
    next_send: so.Mapped[Optional[int]]
    
    @hybrid_method
    def contains(self, search, strict=True, caps=True):
    
        msg = self.text
        if caps:
            index = msg.find(search)
        else:
            index = msg.lower().find(search.lower())
        last_index = index + len(search) - 1
        
        if index == -1:
            return False
        
        if not strict:
            if index == 0:
                return True
            if msg[index - 1].isspace():
                return True
        
        # #checks if standalone word
        if index > 0 and msg[index - 1].isspace():
            if last_index < len(msg) - 1 and msg[last_index + 1].isspace():
                return True
        
        # checks if word is whole message
        if (caps and msg == search) or (not caps and msg.lower() == search.lower()):
            return True
        
        # #checks if word is at beginning
        if index == 0 and msg[last_index + 1].isspace():
            return True
        
        # #checks if word is at end
        if last_index == len(msg) - 1 and msg[index - 1].isspace():
            return True
        
        return False

    def __repr__(self):
        return '<Message {}>'.format(self.meta)
    
    def __str__(self):
        if self.reply:
            return self.meta + '\n' + self.reply + '\n' + self.text
        else:
            return self.meta + '\n' + self.text
    
    
    
    
    
    
    
    
    
    
    
    
