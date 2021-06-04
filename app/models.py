from app import db
from app import login
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin,db.Model):
    __tablename__='user'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(64),index=True,unique=True)
    email=db.Column(db.String(120),index=True,unique=True)
    password_hash=db.Column(db.String(128))
    aadhar=db.Column(db.String(12),index=True,unique=True)
    mobile_number=db.Column(db.String(10),index=True,unique=True)
    pincode=db.Column(db.String(10))
    age=db.Column(db.Integer)
    gender=db.Column(db.String(5))
    tickets=db.relationship('ticket',backref='user_details',lazy='dynamic')
    requests_made=db.relationship('requests_',backref='request_made_by',lazy='dynamic')
    def __repr__(self):
        return '<User:{} Id:{}>'.format(self.username,self.id)
    def set_password(self,password):
        self.password_hash=generate_password_hash(password)
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

class train(db.Model):
    __tablename__='train'
    id=db.Column(db.Integer,primary_key=True)
    train_name=db.Column(db.String(100))
    no_Seats_available=db.Column(db.Integer)
    date=db.Column(db.String(100))
    tickets_booked=db.relationship('ticket',backref='train_details',lazy='dynamic')
    def __repr__(self):
        return '<Train Number:{}>'.format(self.id)

class ticket(db.Model):
    __tablename__='ticket'
    id=db.Column(db.Integer,primary_key=True)
    pnr_number=db.Column(db.Integer,unique=True,index=1)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    seat_details=db.Column(db.String(20))
    status=db.Column(db.String(10))
    no_of_passenger=db.Column(db.Integer,default=1)
    train_no=db.Column(db.Integer,db.ForeignKey('train.id'))
    applied_requests=db.relationship('requests_',backref='ticker_details',lazy='dynamic')
    def __repr__(self):
        return '<Train Number:{} User:{} Seat:{}>'.format(self.train_no,self.user_details.username,self.seat_details)

class requests_(db.Model):
    __tablename__='requests'
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    ticket_id=db.Column(db.Integer,db.ForeignKey('ticket.id'))
    req_status=db.Column(db.String(10))
    preference=db.Column(db.String(15))
    exchange_with_id=db.Column(db.Integer)
    def __repr__(self):
        return '<P1:{} change with P2:{}>'.format(self.ticket_id,self.exchange_with_id)

def create_sample_instances():
    r=User(username='Adithya Narayan',email='adithyanarayan1234@gmail.com',aadhar="856734445656",mobile_number="9048338928",pincode="673008",age=19,gender="Male")
    r.set_password('Adithya')
    db.session.add(r)
    db.session.commit()
    r=User(username='Limka',email='limka@gmail.com',aadhar="856734445655",mobile_number="9333338928",pincode="673021",age=23,gender="F")
    r.set_password('Limka')
    db.session.add(r)
    db.session.commit()
    r=User(username='Pinky',email='pinky@gmail.com',aadhar="996734445655",mobile_number="9933338928",pincode="683021",age=23,gender="F")
    r.set_password('Pinky')
    db.session.add(r)
    db.session.commit()
    r=User(username='Charlie',email='charlie@gmail.com',aadhar="856733335655",mobile_number="9333339028",pincode="673044",age=20,gender="Male")
    r.set_password('Charlie')
    db.session.add(r)
    db.session.commit()
    r=User(username='Pringles',email='pringle@gmail.com',aadhar="444734445655",mobile_number="9333334448",pincode="673021",age=45,gender="Male")
    r.set_password('Pringles')
    db.session.add(r)
    db.session.commit()
    t=train(id=12406,train_name='Jan Shatabdi',no_Seats_available=72,date='31-05-2021')
    db.session.add(t)
    db.session.commit()
    u=ticket(train_no=12406,pnr_number=186054321,user_id=1,seat_details="S2-32-LB",status='CNF')
    db.session.add(u)
    db.session.commit()
    u=ticket(train_no=12406,pnr_number=186054322,user_id=2,seat_details="S2-15-UB",status='CNF')
    db.session.add(u)
    db.session.commit()
    u=ticket(train_no=12406,pnr_number=186054323,user_id=3,seat_details="S2-05-MB",status='CNF')
    db.session.add(u)
    db.session.commit()
    u=ticket(train_no=12406,pnr_number=186054324,user_id=4,seat_details="S2-10-MB",status='CNF')
    db.session.add(u)
    db.session.commit()
    

