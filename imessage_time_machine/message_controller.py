import datetime
import _strptime
from imessage_time_machine.models import Message

class MessageController:
            
    @staticmethod
    def str_date(message):
        return message.date.strftime('%B %-d, %Y')
    
    @staticmethod
    def str_next_date(message):
        return message.next_date.strftime('%B %-d, %Y')
    
    # ex: 5/5/05
    @staticmethod
    def parentheses_date(message):
        return message.date.strftime('%-m/%-d/%y')
    
    @staticmethod
    def weekday(message):
        return message.date.strftime('%A')
    
    @staticmethod
    def str_time(message):
        return message.time.strftime('%-I:%M %p')
    
    @staticmethod
    def signed_msg(message):
        return message.name + ': ' + message.text
    
    @staticmethod
    def signed_snippet(message, length=100):
        signed = MessageController.signed_msg(message)
        if len(signed) >= length:
            return signed[0:length - 1] + '...'
        else:
            return signed
        
    @staticmethod
    def og_title(message):
        return MessageController.signed_snippet(message, length=60)
        
if __name__ == "__main__":
    text = "\n2022-12-14 18:39:47 from esther💙\nhey did u get a notecard in slimp"
    
    msg = Message(text, 0)

    assert msg.str_date() == 'December 14, 2022'
    assert msg.weekday() == 'Wednesday'
    assert msg.str_time() == '6:39 PM'
    assert msg.name == 'esther💙'


