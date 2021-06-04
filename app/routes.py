from app import app,db
from flask import request,redirect,url_for,render_template,flash,get_flashed_messages,jsonify
from flask_login import current_user,login_user,logout_user,login_required
from app.models import User,ticket,train,requests_
from app.forms import LoginForm,RegisterForm
from werkzeug.urls import url_parse
from wtforms.validators import ValidationError
from datetime import datetime
import re
@app.route('/',methods=['POST','GET'])
@app.route('/home',methods=['POST','GET'])
def home():
    if(request.method=='POST'):
        pnr=request.form['pnr']
        if(ticket.query.filter_by(pnr_number=pnr).first() is None):
            flash("Invalid PNR",category="danger")
            return redirect(url_for('home'))
        print(pnr)
        p=ticket.query.filter_by(pnr_number=pnr).first()
        print(p)
        return render_template('info.html',person=p)
    return render_template('index.html')

@app.route('/logout')
def logout():
    db.session.commit()
    logout_user()
    return redirect(url_for('home'))

@app.route('/register',methods=['POST','GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form=RegisterForm()
    if form.validate_on_submit():
        user=User(email=form.email.data,username=form.username.data,aadhar=form.aadhar.data,mobile_number=form.mobile_number.data,pincode=form.area_pincode.data,age=form.age.data,gender=form.gender.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Successfully Registered',category="success")
        print(form.password.data)
        return redirect(url_for('home'))
    return render_template('registration.html',form=form,title='Register')


@app.route('/contactus')
@login_required
def contact():
    return render_template('Contact.html')


@app.route('/chatpage')
@login_required
def chatpage():
    return render_template('Chat.html')

@app.route('/seatchange',methods=['GET','POST'])
@login_required
def seatchange():
    if request.method=='POST':
        pnr=request.form['pnr']
        seatno=request.form['changetoseatno']
        berth=request.form['changetoberth']
        compartment=request.form['changetocompno']
        if berth not in ['LB','UB','MB']:
            flash('Invalid Berth',category='danger')
            return redirect(url_for('seatchange'))
        if(int(seatno)>72 or int(seatno)<1):
            flash('Invalid Seatno',category='danger')
            return redirect(url_for('seatchange'))
        if(ticket.query.filter_by(pnr_number=pnr).first() is None):
            flash('Invalid Ticket PNR',category='danger')
            return redirect(url_for('seatchange'))
        print("Passed 1")
        t=ticket.query.filter_by(pnr_number=pnr).first()
        r=requests_(user_id=current_user.id,ticket_id=t.id,req_status="WAIT",preference=compartment+"-"+seatno+"-"+berth)
        ticket_preferable=ticket.query.filter_by(train_no=t.train_no).all()
        print(ticket_preferable)
        if(ticket_preferable is None):
            return "No exchange possible please wait"
        possible=[]
        for i in ticket_preferable:
            if(i.seat_details[-2:]==berth):
                possible.append(i)
        if possible is None:
            for i in ticket_preferable:
                if(i.seat_details[:2]==compartment):
                    possible.append(i)
        print(possible)
        if possible:
            return render_template('allrequests.html',possible=possible,T=t)
        else:
            return "error"
    return render_template('seat.html')

@app.route('/render_requests/<int:tic>/<int:ticket2>/',methods=['GET','POST'])
def req(tic,ticket2):
    i=int(tic)
    j=int(ticket2)
    print(i)
    print(j)
    all_requests=requests_.query.filter_by(ticket_id=j).all()
    if all_requests is None:
        t=ticket.query.filter_by(id=tic).first()
        r=requests_(user_id=current_user.id,ticket_id=j,req_status="WAIT",preference=t.seat_details,exchange_with_id=i)
        db.session.add(r)
        db.session.commit()
    elif(len(all_requests)>0):
        f=0
        for i in all_requests:
            if i.req_status=='CONF' or i.req_status=='DNY':
               pass 
            else:
                f=1
        if(f!=1):
            t=ticket.query.filter_by(id=tic).first()
            r=requests_(user_id=current_user.id,ticket_id=j,req_status="WAIT",preference=t.seat_details,exchange_with_id=i)
            db.session.add(r)
            db.session.commit()

    else:
        flash('A request on the ticket already exists',category='danger')
        return redirect(url_for('home'))
    print(r)
    flash('Request Placed Successfully',category='success')
    return redirect(url_for('home'))

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Email or Password',category="danger")
            return redirect(url_for('login'))
        login_user(user,remember=form.remember_me.data)
        next_page=request.args.get('next')
        if not next_page or url_parse(next_page).netloc!='':
            next_page=url_for('home')
        return redirect(next_page)
    return render_template('login.html',title='SignIn',form=form)


@app.route('/profile',methods=['GET','POST'])
def profile():
    r=requests_.query.filter_by(user_id=current_user.id).all()
    r_=requests_.query.filter_by(exchange_with_id=current_user.id).all()
    q_=ticket.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html',r=r,r_=r_,q_=q_)

@app.route('/accept/<int:req>',methods=['GET','POST'])
def accept(req):
    r=requests_.query.filter_by(exchange_with_id=req).first()
    if(r.exchange_with_id!=current_user.id):
        flash("Error",category='danger')
    r.req_status="CONF"
    p=r.exchange_with_id
    adi_ticket=ticket.query.filter_by(user_id=p).first()
    lim_ticket=r.ticker_details
    temp=adi_ticket.seat_details
    adi_ticket.seat_details=lim_ticket.seat_details
    lim_ticket.seat_details=temp
    db.session.add(adi_ticket)
    db.session.add(lim_ticket)
    db.session.add(r)
    db.session.commit()
    r=requests_.query.filter_by(user_id=current_user.id).all()
    r_=requests_.query.filter_by(exchange_with_id=current_user.id).all()
    q_=ticket.query.filter_by(user_id=current_user.id).all()
    return redirect(url_for('profile',r=r,r_=r_,q_=q_))

@app.route('/deny/<int:req>',methods=['GET','POST'])
def deny(req):
    r=requests_.query.filter_by(exchange_with_id=req).first()
    if(r.exchange_with_id!=current_user.id):
        flash("Error",category='danger')
    r.req_status="DNY"
    db.session.add(r)
    db.session.commit()
    r=requests_.query.filter_by(user_id=current_user.id).all()
    r_=requests_.query.filter_by(exchange_with_id=current_user.id).all()
    q_=ticket.query.filter_by(user_id=current_user.id).all()
    return redirect(url_for('profile',r=r,r_=r_,q_=q_))