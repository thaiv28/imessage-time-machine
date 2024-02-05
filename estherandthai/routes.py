from flask import Flask, render_template, request, redirect, session, flash, abort, url_for, redirect
from estherandthai.time_machine import TimeMachine
from estherandthai.message_controller import MessageController
from flask_debugtoolbar import DebugToolbarExtension
import jsonpickle
import datetime
from dateutil.relativedelta import relativedelta
from flask_login import LoginManager, UserMixin, current_user, login_user, login_required, login_manager
from estherandthai.models import User
from estherandthai.config import Config
from flask_sqlalchemy import SQLAlchemy
from estherandthai import app, db, models, login
from django.utils.http import url_has_allowed_host_and_scheme
from urllib.parse import urlsplit

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
   
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == "POST":
        next = request.form['next']
        
        user = db.session.scalar(
            db.select(User).where(User.username == request.form['username']))
        print(user)
        
        if user is None or user.password != request.form['password']:
            
            flash('Invalid username or password')
            return render_template('login.html', invalid=True, next=next)
        
        login_user(user)
        
        print(next)
        if not url_has_allowed_host_and_scheme(next, request.host):
            return abort(400)
        
        return redirect(next or url_for('index'))
    else:
        return render_template('login.html', next=request.args.get('next'), invalid=False)


@app.route('/')
@login_required
def index():
    return redirect("/timemachine/")

@app.route("/timemachine/")
@login_required
def timemachine():
    t = TimeMachine()

    return render_template("tm/index.html")

@app.route('/timemachine/message/<int:id>/')
def message_one(id):
    return redirect('/timemachine/message/'+str(id)+'/1')

@app.route('/timemachine/message/<int:id>/<int:page>')
@login_required
def message(id, page):
    t = TimeMachine()
    cont = MessageController()
    
    msg = t.getbyid(id)
    context = t.get_context(msg, page=page)
    rpp = t.rpp
    master_length = t.length
        
    if page <= 1:
        return render_template('tm/message.html', cont=cont, msg=msg, context=context, id=id, 
                               rpp=rpp, page=page, master_length=master_length, url=request.url)
    else:
        print("returning new page of message_results")
        return render_template('tm/message_results.html', cont=cont, msg=msg, context=context, id=id,
                               rpp=rpp, page=page, master_length=master_length, url=request.url)

@app.route("/timemachine/search/<int:page>", methods=['GET'])
@login_required
def timemachine_search(page):
    if request.args.get('search') == 'yearago':
        return redirect("/timemachine/date/" + (datetime.date.today()-relativedelta(years=1)).isoformat() + "/1")
        
    t = TimeMachine()
    cont = MessageController()
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
            msg = t.random_search(request.args.get('terms'), caps=caps,
                                  strict=strict)
            
            if msg == None:
                return render_template('/tm/empty.html', terms=request.args['terms'], 
                                args=request.args, page=page, url=request.url)
            
        return redirect("/timemachine/message/"+str(msg.id)+"/1")
    
    # if search with terms
    messages = t.search(request.args['terms'], page=page,
                        sort_by=request.args.get('sort_by'),
                        start=request.args.get('start_date'), 
                        end=request.args.get('end_date'),
                        caps=caps, strict=strict)
        
    if messages == []:
            return render_template('/tm/empty.html', terms=request.args['terms'],
                                messages=messages, nexts=t.get_next_sends(messages), 
                                args=request.args, page=page, url=request.url)
    
    # first result page
    if page <= 1:
        return render_template('/tm/search.html', cont=cont, terms=request.args['terms'],
                            messages=messages, nexts=t.get_next_sends(messages), args=request.args,
                            page=page, rpp=t.rpp, url=request.url)
    # any other page except first results
    else:
        print('Requesting new page.')
        return render_template('/tm/results.html', cont=cont, terms=request.args['terms'],
                            messages=messages, nexts=t.get_next_sends(messages),
                            page=page,rpp=t.rpp, url=request.url)
        
@app.route("/timemachine/date/<string:date>")
@login_required
def timemachine_date(date):
    t = TimeMachine()
    cont = MessageController()
    messages = t.search(start=date, end=date, image=True, reactions=True)
    page = 1
    
    date = datetime.date.fromisoformat(date)
    str_date = date.strftime("%B %-d, %Y")
    prev_day = date - datetime.timedelta(days=1)
    next_day = date + datetime.timedelta(days=1)
 
    
    return render_template('/tm/date.html', cont=cont, messages=messages, nexts=t.get_next_sends(messages),
                            args=request.args, page=page,rpp=t.rpp, date=date, str_date=str_date, 
                            next_day=next_day, prev_day=prev_day, url=request.url)
        
@app.route("/timemachine/date/<string:date>/<int:page>")
@login_required
def timemachine_date_search(date, page):
    t = TimeMachine()
    cont = MessageController()

    messages = t.search(start=date, end=date)
    
    date = datetime.date.fromisoformat(date)
    str_date = date.strftime("%B %-d, %Y")
    prev_day = date - datetime.timedelta(days=1)
    next_day = date + datetime.timedelta(days=1)
    
    if next_day > t.end_dt.date():
        next_day = None
        
    if prev_day < t.start_dt.date():
        prev_day = None
        
    if page <= 1:
        return render_template('/tm/date.html', cont=cont, messages=messages, nexts=t.get_next_sends(messages),
                               args=request.args, page=page,rpp=t.rpp, date=date, str_date=str_date, 
                               next_day=next_day, prev_day=prev_day, url=request.url)
    else:
        print('Requesting new page.')
        return render_template('/tm/date_results.html', cont=cont, messages=messages, nexts=t.get_next_sends(messages),
                               args=request.args, page=page,rpp=t.rpp, date=date, next_day=next_day, prev_day=prev_day, url=request.url)


    
if __name__=='__main__':
    app.run(debug=True)
    