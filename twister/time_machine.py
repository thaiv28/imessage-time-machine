import random
from twister.message import Message
import argparse
import datetime

class TimeMachine():
    def __init__(self, text):
        self.text = text
        self.separator = '----------------------------------------------------'
        self.master = self.get_messages(text)
        self.messages = self.master
        
    
    def random(self):
        return self.messages[random.randint(0, len(self.messages) - 1)]
    
    
    def search(self, term, caps_sensitive=False, strict=False):
        ret = []
        
        s = term.strip()
        
        for msg in self.messages:
            if caps_sensitive and self.contains(msg.text, s, strict=strict):
                ret.append(msg)
            if not caps_sensitive and self.contains(msg.text.upper(), s.upper(),
                                                    strict=strict):
                ret.append(msg)
        return ret
    
    
    def get_messages(self, text):
        split = text.splitlines()
        messages = []
        
        if split[0] == self.separator:
            split.pop(0)
        
        counter = 0
        t = ''
        for line in split:
            if line == self.separator:
                messages.append(Message(t, counter))
                t = ''
                counter += 1
            elif line != '':
                t += line + '\n'
                
        return messages
    
    # strict variable determines if allows search term to be start of a word,
    # but not the whole word
    def contains(self, msg, search, strict=True):
        index = msg.find(search)
        last_index = index + len(search) - 1
        
        if index == -1:
            return False
        
        # #checks if standalone word
        if index > 0 and msg[index - 1].isspace():
            if last_index < len(msg) - 1 and msg[last_index + 1].isspace():
                return True
        
        # checks if word is whole message
        if msg == search:
            return True
        
        # #checks if word is at beginning
        if index == 0 and msg[last_index + 1].isspace():
            return True
        
        # #checks if word is at end
        if last_index == len(msg) - 1 and msg[index - 1].isspace():
            return True
        
        if not strict:
            if index == 0:
                return True
            if msg[index - 1].isspace():
                return True
        
        return False
        
    def get_context(self, msg, scope=10):
        index = self.messages.index(msg)
        
        if index > scope:
            lower = index - scope
        else:
            lower = 0
            
        if index < len(self.messages) - scope - 1:
            upper = index + scope
        else:
            upper = len(self.messages) - 1
            
        ret = []
        for i in range(lower, upper):
            ret.append(self.messages[i])
            
        return ret
    
    def dates(self, s=None, e=None):
        collect = True
        if s: 
            start = s.isoformat()
            collect = False
        if e: 
            end = e.isoformat()
        
        messages = []
        
        for msg in self.master:
            if start and start in msg.meta:
                collect = True
                
            if end and end in msg.meta:
                collect = False
                break
            
            if collect:
                messages.append(msg)
        
        self.messages = messages
    
    def valid_date(self, start, end):
        if end < start: 
            return False
        return True
    
if __name__ == "__main__":
    f = open('../backup.txt', 'r')
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
    
    t = TimeMachine(f.read())
    string = ''
    
    if args.startdate or args.enddate:
        t.dates(datetime.date.fromisoformat(args.startdate), 
                datetime.date.fromisoformat(args.enddate))

    if args.search:
        search_results = t.search(args.search, strict=args.strict, 
                                  caps_sensitive=args.caps)
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
    
    f.close()
    