from flask import Flask, render_template, request, redirect, session
from twister.time_machine import TimeMachine
import random
import os
import jsonpickle

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12).hex()
    
@app.route('/')
def index():
    return redirect("/timemachine")

@app.route("/timemachine")
def timemachine():
    t = create_tm()
    
    return redirect("/timemachine/message/"+str(random.randint(0, len(t.messages) - 1)))

@app.route('/timemachine/message/<int:id>')
def message(id):
    if 'msg' in session and session['id'] == id:
        msg = jsonpickle.decode(session['msg'])
        context = jsonpickle.decode(session['context'])
    else:
        t = create_tm()
        encode(t, t.getbyid(id))
        
        msg = t.getbyid(id)
        context = t.get_context(msg)
    
    return render_template('tm/message.html', msg=msg, context=context)

@app.route("/timemachine/search", methods=['GET'])
def timemachine_search():
    t = create_tm()
    print(request.args)
    # check if random button click
    if request.args.get('search') == 'random':
        msg = t.random()
        encode(t, msg)

        return redirect("/timemachine/message/"+str(msg.id))
    else:
        messages = t.search(request.args['terms'])
        nexts = {}
        for msg in messages:
            nexts[msg] = t.next_send(msg)
            
        if messages == []:
            return render_template('/tm/empty.html')
        else:
            msg = messages[0]
            return render_template('/tm/search.html', terms=request.args['terms'],
                                   messages=messages, nexts=nexts)

    return render_template('tm/message.html', msg=msg, conteçxt=t.get_context(msg))

@app.route("/timemachine/results")
def timemachine_results():
    pass

def create_tm():
    f = open('../backup.txt', 'r')
    t = TimeMachine(f.read())
    f.close()
    
    return t

def encode(t, msg):
    session['msg'] = jsonpickle.encode(msg)
    session['context'] = jsonpickle.encode(t.get_context(msg))
    session['id'] = msg.id
    
if __name__=='__main__':
    
    app.run()
    