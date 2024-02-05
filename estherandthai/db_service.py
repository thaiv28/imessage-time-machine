from estherandthai.models import Message, User
import datetime
from estherandthai import db
import sqlalchemy as sa
import sqlalchemy.orm as so
import os

def init_messages(file="../backup.txt",
                separator="----------------------------------------------------"):
    
    f = open(file, 'r')
    text = f.read()
    f.close()
    
    filters = ['boob', 'dick', 'cum', 'sexy', 'shirtless', 'topless', 
                        'mom', 'stroke', 'grind', 'hot', 'tip', 'nipple', 'moan']
    user_messages = {}
    updates = []
    
    split = text.splitlines()
    messages = []
        
    if split[0] == separator:
        split.pop(0)
    
    t = ''
    skip = False
    id = 1
    
    for line in split:
        if line == separator:
            for word in filters:
                if word.lower() in t.lower():
                    skip = True
                    break
                
            if skip:
                skip = False
                t = ''
                continue 

            message = message_to_model(t)

            update = {}
            # sets "next_send" property on user_messages
            if message.name in user_messages:
                update["id"] = user_messages.get(message.name)
                update["next_send"] = id
                updates.append(update)
                
            user_messages[message.name] = id
            if id == 0: print(update)
            
            db.session.add(message)
            t = ''
            id += 1              
            
        elif line != '':
            t += line + '\n'
            
    db.session.commit()
    print(updates[-1])
    print(len(updates))
    db.session.execute(sa.update(Message), updates)
    db.session.commit()
    
    init_next_dates()
    
def message_to_model(raw):
    s = raw.strip().split('\n')
    if len(s) == 3:
        meta = s[0].strip()
        reply = s[1].strip()
        text = s[2].strip()
    elif len(s) == 2:
        meta = s[0].strip()
        text = s[1].strip()
        reply = None
    else:
        meta = s[0].strip()
        text = ''
        reply = None
        
    meta_words = meta.split()
        
    date = datetime.date.fromisoformat(meta_words[0])
    time = datetime.time.fromisoformat(meta_words[1])
    dt = datetime.datetime.combine(date, time)
        
    if 'notification' not in meta:
        name = meta_words[3]
    else:
        name = None
    
    if "\nLoved " in raw\
        or "\nLiked " in raw\
        or "\nDisliked " in raw\
        or "\nLaughed at " in raw:
        reaction = True
    else:
        reaction = False
        
    if "(Image)" in text:
        image = True
    else:
        image = False
        
    return Message(meta=meta, reply=reply,text=text,date=date,
                   time=time,dt=dt,name=name,reaction=reaction, image=image)
    
def init_next_dates():
    prev = None
    updates = []
    
    for msg in db.session.scalars(sa.select(Message)):
        if prev:
            indv = {}
            indv['id'] = prev.id
            indv['next_date'] = msg.date
            updates.append(indv)
        prev = msg

    db.session.execute(sa.update(Message), updates)
    db.session.commit()
        
        
def init_next_sends():
    updates = []
    for msg in db.session.scalars(sa.select(Message)):
        indv = {}
        indv['id'] = msg.id
        next = db.session.scalar(sa.select(Message).where(Message.id > msg.id)
                                 .where(Message.name == msg.name))
        if next:
            indv['next_send'] = next.id
        else:
            indv['next_send'] = None
        print(msg.id)
        
    db.session.execute(sa.update(Message), updates)
    db.session.commit()
    
def init_login():
    user = os.environ.get('TM_USER')
    pw = os.environ.get('TM_PW')
    
    if user and pw:
        db.session.add(User(username=user, password=pw))
        db.session.commit()
    else:
        print('No valid login variables')
        exit()
    
