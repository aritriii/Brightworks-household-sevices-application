from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db=SQLAlchemy()

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(30),nullable=False,unique=True)
    password=db.Column(db.String(30),nullable=False)
    fullname=db.Column(db.String(30))
    address=db.Column(db.String(80))
    pincode=db.Column(db.Integer)

    servicename=db.Column(db.String(30),db.ForeignKey('service.name'))
    experience=db.Column(db.Integer)
    document=db.Column(db.String(100))
    rating=db.Column(db.Integer,default=0.0)
    countrating=db.Column(db.Integer)

    isApproved=isProf=db.Column(db.Boolean,default=False)
    isCustomer=db.Column(db.Boolean,default=True)
    isProf=db.Column(db.Boolean,default=False)
    isAdmin=db.Column(db.Boolean,default=False)
    isBlocked=db.Column(db.Boolean,default=False)

class Service(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(40),nullable=False,unique=True)
    time_reqd=db.Column(db.Integer)
    description=db.Column(db.String(200))
    base_price=db.Column(db.Integer)

class ServiceRequest(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    service_id=db.Column(db.Integer,db.ForeignKey('service.id'),nullable=False)
    customer_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    prof_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=True)
    req_date=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    comp_date=db.Column(db.DateTime)
    serv_stat=db.Column(db.String(20),nullable=False,default='requested')
    remarks=db.Column(db.Text)
