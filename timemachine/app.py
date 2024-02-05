from flask import Flask, render_template, request, redirect, session
from timemachine.time_machine import TimeMachine
from flask_debugtoolbar import DebugToolbarExtension
import random
import os
import jsonpickle
import datetime
from dateutil.relativedelta import relativedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12).hex()
toolbar = DebugToolbarExtension(app)
    
@app.route('/')
def index():
    return redirect("/timemachine/")

@app.route("/timemachine/")
def timemachine():
    t = create_tm()
    
    return render_template("tm/index.html")

@app.route('/timemachine/message/<int:id>/<int:page>')
def message(id, page):

    t = create_tm()
    
    msg = t.getbyid(id)
    print(id)
    context = t.get_context(msg, page=page)
    rpp = t.rpp
    master_length = len(t.master)
        
    if page <= 1:
        return render_template('tm/message.html', msg=msg, context=context, id=id, 
                               rpp=rpp, page=page, master_length=master_length)
    else:
        print("returning new page of message_results")
        return render_template('tm/message_results.html', msg=msg, context=context, id=id,
                               rpp=rpp, page=page, master_length=master_length)

@app.route("/timemachine/search/<int:page>", methods=['GET'])
def timemachine_search(page):
    if request.args.get('search') == 'yearago':
        return redirect("/timemachine/date/" + (datetime.date.today()-relativedelta(years=1)).isoformat() + "/1")
        
    t = create_tm()
    if request.args.get('caps'):
        caps = True
    else:
        caps = False
    if request.args.get('strict'):
        strict = True
    else:
        strict = False

    print(request.args)

    # check if random button click
    if request.args.get('search') == 'random':
        if request.args.get('terms') == '':
            msg = t.random()
        else:
            msg = t.random_search(request.args.get('terms'), caps_sensitive=caps,
                                  strict=strict)
            
        encode(t, msg)
        return redirect("/timemachine/message/"+str(msg.id)+"/1")
    
    # if search with terms
    messages = t.search(request.args['terms'], 
                        sort_by=request.args.get('sort_by'),
                        start=request.args.get('start_date'), 
                        end=request.args.get('end_date'),
                        caps_sensitive=caps, strict=strict)
        
    if messages == []:
            return render_template('/tm/empty.html', terms=request.args['terms'],
                                messages=messages, nexts=t.get_next_sends(messages), 
                                args=request.args, page=page)
    
    # first result page
    if page <= 1:
        return render_template('/tm/search.html', terms=request.args['terms'],
                            messages=messages, nexts=t.get_next_sends(messages), args=request.args,
                            page=page, rpp=t.rpp)
    # any other page except first results
    else:
        print('Requesting new page.')
        return render_template('/tm/results.html', terms=request.args['terms'],
                            messages=messages, nexts=t.get_next_sends(messages),
                            page=page,rpp=t.rpp)
        
@app.route("/timemachine/date/<string:date>")
def timemachine_date(date):
    t = create_tm()
    messages = t.search(start=date, end=date)
    page = 1
    
    date = datetime.date.fromisoformat(date)
    str_date = date.strftime("%B %-d, %Y")
    prev_day = date - datetime.timedelta(days=1)
    next_day = date + datetime.timedelta(days=1)
 
    
    return render_template('/tm/date.html', messages=messages, nexts=t.get_next_sends(messages),
                            args=request.args, page=page,rpp=t.rpp, date=date, str_date=str_date, 
                            next_day=next_day, prev_day=prev_day)
        
@app.route("/timemachine/date/<string:date>/<int:page>")
def timemachine_date_search(date, page):
    t = create_tm()

    messages = t.search(start=date, end=date)
    
    date = datetime.date.fromisoformat(date)
    str_date = date.strftime("%B %-d, %Y")
    prev_day = date - datetime.timedelta(days=1)
    next_day = date + datetime.timedelta(days=1)
    
    if next_day > t.end_date:
        next_day = None
        
    if prev_day < t.start_date:
        prev_day = None
        
    if page <= 1:
        return render_template('/tm/date.html', messages=messages, nexts=t.get_next_sends(messages),
                               args=request.args, page=page,rpp=t.rpp, date=date, str_date=str_date, 
                               next_day=next_day, prev_day=prev_day)
    else:
        print('Requesting new page.')
        return render_template('/tm/date_results.html',messages=messages, nexts=t.get_next_sends(messages),
                               args=request.args, page=page,rpp=t.rpp, date=date, next_day=next_day, prev_day=prev_day)

def create_tm():
    f = open('../backup.txt', 'r')
    t = TimeMachine(f.read())
    f.close()

    return t

def encode(t, msg, page=1):
    session['msg'] = jsonpickle.encode(msg)
    session['context'] = jsonpickle.encode(t.get_context(msg, page))
    session['id'] = msg.id
    session['rpp'] = t.rpp
    session['master_length'] = len(t.master)
    
if __name__=='__main__':
    app.run(debug=True)
    