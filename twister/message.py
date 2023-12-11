import datetime

class Message():
    def __init__(self, text, id):
        s = text.strip().split('\n')
        if len(s) == 3:
            self.meta = s[0].strip()
            self.reply = s[1].strip()
            self.text = s[2].strip()
        elif len(s) == 2:
            self.meta = s[0].strip()
            self.text = s[1].strip()
            self.reply = None
        else:
            self.meta = s[0].strip()
            self.text = ''
            self.reply = None
            
        self.meta_words = self.meta.split()
            
        self.date = datetime.date.fromisoformat(self.meta_words[0])
        self.time = datetime.datetime.strptime(self.meta_words[1], "%H:%M:%S")
            
        if 'notification' not in self.meta:
            self.name = self.meta_words[3]
        else:
            self.name = None
        
        self.id = id
            
    def str_date(self):
        return self.date.strftime('%B %-d, %Y')
    
    def weekday(self):
        return self.date.strftime('%A')
    
    def str_time(self):
        return self.time.strftime('%-I:%M %p')
    
    def signed_msg(self):
        return self.name + ': ' + self.text
        
    def __str__(self):
        if self.reply:
            return self.meta + '\n' + self.reply + '\n' + self.text
        else:
            return self.meta + '\n' + self.text
        
if __name__ == "__main__":
    text = "\n2022-12-14 18:39:47 from esther💙\nhey did u get a notecard in slimp"
    
    msg = Message(text)

    assert msg.str_date() == 'December 14, 2022'
    assert msg.weekday() == 'Wednesday'
    assert msg.str_time() == '6:39 PM'
    assert msg.name == 'esther💙'


