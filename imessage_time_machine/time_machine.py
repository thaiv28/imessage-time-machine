import random
from imessage_time_machine import db, app
from imessage_time_machine.models import Message
import argparse
import datetime
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask import session
import jsonpickle

class TimeMachine():
    def __init__(self, test=False):
        if not test and session.get("tm_length"):
            self.length = session.get("tm_length")
        else:
            self.length = db.session.query(Message).count()
            if not test: session["tm_length"] = self.length
        if not test and session.get("start_dt"):
            self.start_dt = jsonpickle.decode(session.get("start_dt"))
        else:
            self.start_dt = db.session.scalar(db.select(Message).order_by(Message.dt)).dt
            if not test: session["start_dt"] = jsonpickle.encode(self.start_dt)
        
        self.rpp=50
        self.end_dt = datetime.datetime.now()
             
    def random(self):
        return self.getbyid(random.randint(0, self.length))
            
    def random_search(self, term, caps=False, strict=False):
        results = self.search(term, caps=caps, strict=strict)
        if results:
            return random.choice(results)
        else:
            return None
    
    def search(self, term='', page=None, caps=False, strict=False, reactions=False,
               sort_by='Oldest first', start=None, end=None, image=False):
        ret = []

        
        if start: 
            start_date = datetime.date.fromisoformat(start)
            min_time = datetime.time(hour=0)
            start_dt = datetime.datetime.combine(start_date, min_time)
        else:
            start_dt = self.start_dt
        if end: 
            end_date = datetime.date.fromisoformat(end)
            max_time = datetime.time(hour=23, minute=59, second=59)
            end_dt = datetime.datetime.combine(end_date, max_time)
        else:
            end_dt = self.end_dt

        if term:
            s = term.strip()
        
        print("start_dt: " + str(start_dt))
        print("end_dt: " + str(end_dt))
        ret = list(db.session.scalars(sa.select(Message)
                                     .where(Message.dt <= end_dt)
                                     .where(Message.dt >= start_dt)
                                     .where(Message.text.contains(term))
                                     .where(image or Message.image == False)
                                     .where(reactions or Message.reaction == False)))
        
  
        if sort_by == 'Latest first':
            ret.reverse()
        elif sort_by == 'Random':
            random.shuffle(ret)

        return ret
    
    
    def next(self, msg):
        return self.getbyid(msg.id + 1)
    
    # returns next message the same user sent
    def next_send(self, msg):
        return self.getbyid(msg.next_send)
    
    def get_next_sends(self, messages):
        nexts = {}
        for msg in messages:
            nexts[msg] = self.next_send(msg)
        
        return nexts
    
    def getbyid(self, id):
        return db.session.scalar(sa.select(Message).where(Message.id == id))
    
    # strict variable determines if allows search term to be start of a word,
    # but not the whole word
    def contains(self, msg, search, strict=True, caps=True):
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
        
    def get_context(self, msg, page, lower_scope=10, buffer=1, only_relevant=False):
        upper_scope = self.rpp
        index = msg.id

        if page <= 1:
            if index > lower_scope:
                lower = index - lower_scope
            else:
                lower = 1
                
            if index + upper_scope < self.length:
                upper = index + upper_scope
            else:
                upper = self.length
        else:
            lower = index + (page - 1) * upper_scope
            upper = index + page * upper_scope
            
            if lower >= self.length:
                return []
            if upper >= self.length:
                upper = self.length
            
        ret = []
        last = self.getbyid(lower)

        for i in range(lower, upper):
            current = self.getbyid(i)
            if only_relevant:
                # check if same day
                if current.date == msg.date:
                    ret.append(current)
                    last = current
                elif i > lower:
                    if current.datetime - last.datetime < \
                    datetime.timedelta(hours=2):
                        ret.append(current)
            else:
                ret.append(current)
        
        return ret
    
    def dates(self, s=None, e=None, image=False, reactions=True):
        collect = True
        if not s: 
            start_dt = self.start_dt
        if not e: 
            end_dt = self.end_dt
    
        return list(db.session.scalars(sa.select(Message)
                                     .where(Message.dt <= end_dt)
                                     .where(Message.dt >= start_dt)
                                     .where(image or Message.image == False)
                                     .where(reactions or Message.reaction == False)))
        
        
    
    def valid_date(self, start, end):
        if end < start: 
            return False
        return True
    

    
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    
        strict = False
        caps = False
        rand = False
        search = None
        
        parser = argparse.ArgumentParser()
        parser.add_argument("-s", "--search", help = "Search for specific term.")
        parser.add_argument("-r", "--rand", action='store_true',
                            help="Return random message.")
        parser.add_argument("-st", "--strict", action='store_true',
                        help="Search for only standalone word")
        parser.add_argument("-c", "--caps", action='store_true',
                            help="Search is caps sensitive")
        parser.add_argument('-ct', '--context', nargs='?', default=0, const=10,
                            help="Get context for message.")
        parser.add_argument('-sd', '--startdate', help="Start date")
        parser.add_argument('-ed', '--enddate', help="End date")
        args = parser.parse_args()
        
        t = TimeMachine(test=True)
        string = ''
        
        if args.startdate or args.enddate:
            t.dates(datetime.date.fromisoformat(args.startdate), 
                    datetime.date.fromisoformat(args.enddate))

        if args.search:
            search_results = t.search(args.search, strict=args.strict, 
                                    caps=args.caps)
            if len(search_results) == 0:
                print("No messages found")
                exit()
                
            if args.rand:
                msg = search_results[random.randint(0, len(search_results) - 1)]
            else:
                msg = search_results[0]
                
        else:
            msg = t.random()
            
        if args.context != 0:
            string += t.separator + '\n'  
            for m in t.get_context(msg):
                string += t.separator + "\n"
                string += str(m) + "\n"
        
        print(msg)
        if string: print(string)
        print("next: " + t.next_send(msg).text)
    