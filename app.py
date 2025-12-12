from flask import Flask
from flask import redirect,render_template,session,request,flash,url_for
import os
from datetime import datetime
from models import *


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///hsadb.sqlite3'
app.config['SECRET_KEY']='mysecretkeyissecret'
db.init_app(app)
app.app_context().push()
db.create_all()

def get_curr_user():
    curr_id=session.get('id',None)
    currobj=User.query.filter_by(id=curr_id).first()

    curr_user={'id':None,'email':None,'roles':[]}
    if currobj:
        curr_user['email']=currobj.email
        curr_user['id']=currobj.id
        
        if currobj.isCustomer:curr_user['roles'].append('customer')
        if currobj.isProf:curr_user['roles'].append('prof')
        if currobj.isAdmin:curr_user['roles'].append('admin')
    return curr_user

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/access')
def access():
    curr_user=get_curr_user()
    return render_template('access.html',curr_user=curr_user)

@app.route('/login',methods=['GET','POST'])
def login():
    email=request.form.get('email')
    password=request.form.get('password')
    role=request.form.get('role')

    u=User.query.filter_by(email=email).first()

    if email=='admin@gmail.com' and password=='admin101' and role=='admin':
        return redirect(url_for('admindash'))

    if u :
        session['id']=u.id
        if password==u.password:
            if u.isAdmin and role=='admin':
                return redirect(url_for('admindash'))
            elif u.isProf and role=='professional':
                return redirect(url_for('profdash'))
            elif u.isCustomer and role=='customer':
                return redirect(url_for('customerdash'))
            else:
                flash('Enter correct role !')
                return redirect(url_for('access'))
        else:
            flash('Incorrect password !')
            return redirect(url_for('access'))
    else:
        if role=='professional':
            return redirect(url_for('profsignupg'))
        if role=='customer':
            return redirect(url_for('customersignupg'))
        return redirect(url_for('access'))

@app.route('/customersignupg',methods=['GET','POST'])
def customersignupg():
    return render_template('customersignupg.html')

@app.route('/customersignup',methods=['GET','POST'])
def customersignup():
    e=request.form.get('email')
    p1=request.form.get('password1')
    p2=request.form.get('password2')
    n=request.form.get('fullname')
    pc=request.form.get('pincode')
    address=request.form.get('address')

    
    if e and p1 and p1==p2:
        u=User.query.filter_by(email=e).first()
        if u:
            flash('user already exsists')
            return redirect(url_for('access'))
        else:
            u=User(email=e,password=p1,fullname=n,pincode=pc,address=address,isProf=False,isAdmin=False)
            db.session.add(u)
            db.session.commit()
            flash('User registered successfully !')
        return redirect(url_for('access'))
    return redirect(url_for('access'))

@app.route('/profsignupg',methods=['GET','POST'])
def profsignupg():
    services=Service.query.all()
    return render_template('profsignupg.html',services=services)

@app.route('/profsignup',methods=['GET','POST'])
def profsignup():
    e=request.form.get('email')
    p1=request.form.get('password1')
    p2=request.form.get('password2')
    n=request.form.get('fullname')
    pc=request.form.get('pincode')
    sn=request.form.get('servicename')
    ep=request.form.get('experience')
    address=request.form.get('address')
    file=request.files.get('file')
    

    if e and p1 and p1==p2:
        sp=User.query.filter_by(email=e).first()
        if sp:
            flash('user already exsists')
            #return redirect(url_for('access'))
        else:
            sp=User(email=e,password=p1,fullname=n,pincode=pc,servicename=sn,experience=ep,address=address,isProf=True,isCustomer=False)
            filename=f'{sp.id}.pdf'
            file.save(os.path.join('./static/uploads',filename))
            sp.document=filename
            db.session.add(sp)
            db.session.commit()
            flash('User registered successfully !')
        return redirect(url_for('access'))
    return redirect(url_for('access'))

@app.route('/logout')
def logout():
    session.pop('id',None)
    return redirect(url_for('access'))

#------------------------------------------------------------------------------------------------------------
@app.route('/customerdash')
def customerdash():
    curr_user=get_curr_user()       
    user=User.query.filter_by(id = curr_user['id']).first()
    if not user:
        return redirect(url_for('access'))
    
    services=Service.query.all()
    servrequests=ServiceRequest.query.filter_by(customer_id=user.id).all()
    
    return render_template('customerdash.html',services=services,servrequests=servrequests,user=user)

@app.route('/profdash')
def profdash():
    curr_user=get_curr_user()       
    prof=User.query.filter_by(id = curr_user['id']).first()
    service=Service.query.filter_by(name=prof.servicename).first()
    servrequests=ServiceRequest.query.filter_by(prof_id=prof.id).all()
    if prof.isBlocked:
        flash('You are blocked by the admin.For further queries, please contact admin at admin@gmail.com.')
        return(redirect(url_for('access')))
    else:
        for req in servrequests:
            if req:
                customer=User.query.filter_by(id=req.customer_id).first()
                return render_template('profdash.html',user=prof,servrequests=servrequests,service=service,customer=customer)   
    if not prof:
        return redirect(url_for('access'))
    return render_template('profdash.html',user=prof,servrequests=servrequests,service=service)


@app.route('/admindash')
def admindash():
    curr_user=get_curr_user()
    user=User.query.filter_by(id = curr_user['id']).first()

    services=Service.query.all()
    profs=User.query.filter_by(isProf=True).all()
    servreq=ServiceRequest.query.all()

    return render_template('admindash.html',services=services,profs=profs,servreq=servreq)

#-----------------------------------------------------------------------------------------------------------
#SEARCH

@app.route('/profsearch')
def profsearch():
    curr_user=get_curr_user()       
    user=User.query.filter_by(id = curr_user['id']).first()
    service=Service.query.filter_by(name=user.servicename).first()
    servrequests=ServiceRequest.query.filter_by(service_id=service.id).all()
    for req in servrequests:
        if req:
            customer=User.query.filter_by(id=req.customer_id).first()
    search=request.args.get('search')
    if search:
        sr1=ServiceRequest.query.filter_by(service_id=service.id).filter(ServiceRequest.comp_date.contains(search)).all()
    if sr1:
        return render_template('profsearch.html',user=user,service=service,servrequests=servrequests,customer=customer,sr1=sr1)
    else:
        flash('No search results !')
        redirect(url_for('profdash'))
    return render_template('profsearch.html',user=user,service=service,servrequests=servrequests,customer=customer,sr1=sr1)

@app.route('/custsearch',methods=['GET','POST'])
def custsearch():
    curr_user=get_curr_user()       
    user=User.query.filter_by(id=curr_user['id']).first()
    res=[]
    searchby=request.args.get('searchby')
    search=request.args.get('search')

    if searchby=='service':
        res=Service.query.filter(Service.name.contains(search)).all()
    elif searchby=='pincode':
        res=Service.query.join(User,User.servicename==Service.name).filter(User.pincode==search,User.isProf==True).all()
    if res:
        return render_template('custsearch.html',user=user,s1=res)
    else:
        flash('No such results found!')
        return redirect(url_for('customerdash'))

@app.route('/adminsearch',methods=['GET','POST'])
def adminsearch():
    curr_user=get_curr_user()       
    user=User.query.filter_by(id = curr_user['id']).first()
    search=request.args.get('search')
    u=[]
    if search:
        u=User.query.filter((User.isProf==True)|(User.isCustomer==True),User.fullname.contains(search)).all()
    if u is not None:
        return render_template('adminsearch.html',user=user,u=u)
    else:
        flash('No such users !')
        redirect(url_for('admindash'))
    return render_template('adminsearch.html',user=user,u=u)


#------------------------------------------------------------------------------------------------------------
@app.route('/addservice',methods=['GET','POST'])
def addservice():
    return render_template('addservice.html')

@app.route('/addnewservice',methods=['GET','POST'])
def addnewservice():
    servname=request.form.get('servicename')
    desc=request.form.get('servicedescript')
    bp=request.form.get('baseprice')

    if servname and desc and bp:
        newservice=Service.query.filter_by(name=servname).first()
        if newservice:
            flash('service already exsists')
            return redirect(url_for('addservice'))
        else:
            newservice=Service(name=servname,description=desc,base_price=bp)
            db.session.add(newservice)
            db.session.commit()
        return redirect(url_for('admindash'))
    return redirect(url_for('admindash'))

@app.route('/editservice/<int:servid>',methods=['GET','POST'])
def editservice(servid):
    service=Service.query.filter_by(id=servid).first()
    if request.method=='POST':
        servname=request.form.get('servicename')
        desc=request.form.get('servicedescript')
        bp=request.form.get('baseprice')
        tr=request.form.get('time_reqd')

        service.name = servname
        service.description = desc
        service.base_price = bp
        service.time_reqd = tr

        db.session.commit()
        return redirect(url_for('admindash'))
    return render_template('editservice.html',service=service)

@app.route('/deleteserv/<int:servid>',methods=['GET','POST'])
def deleteserv(servid):
    serv=Service.query.filter_by(id=servid).first()
    db.session.delete(serv)
    db.session.commit()
    flash('Service deleted!')
    return redirect(url_for('admindash'))
    
@app.route('/service_details/<int:servid>',methods=['GET','POST'])  
def service_details(servid):
    service=Service.query.filter_by(id=servid).first()
    return render_template('service_details.html',service=service)

@app.route('/approveprof/<int:profid>',methods=['GET','POST'])
def approveprof(profid):
    prof=User.query.filter_by(id=profid).first()
    prof.isApproved=True
    db.session.commit()
    flash('Professional approved!')
    return redirect(url_for('admindash'))
@app.route('/rejectprof/<int:profid>',methods=['GET','POST'])
def rejectprof(profid):
    prof=User.query.filter_by(id=profid).first()
    db.session.delete(prof)
    db.session.commit()
    flash('Professional rejected!')
    return redirect(url_for('admindash'))
@app.route('/deleteprof/<int:profid>',methods=['GET','POST'])
def deleteprof(profid):
    prof=User.query.filter_by(id=profid).first()
    db.session.delete(prof)
    db.session.commit()
    flash('Professional deleted!')
    return redirect(url_for('admindash'))

@app.route('/blockuser/<int:userid>',methods=['GET','POST'])
def blockuser(userid):
    user=User.query.filter_by(id=userid).first()
    if user.isBlocked:
        flash('User already blocked !')
        return redirect(url_for('adminsearch'))
    else:
        user.isBlocked=True
        db.session.commit()
        flash('User has been blocked !')
        return redirect(url_for('adminsearch'))
    
@app.route('/unblockuser/<int:userid>',methods=['GET','POST'])
def unblockuser(userid):
    user=User.query.filter_by(id=userid).first()
    if user.isBlocked:
        user.isBlocked=False
        db.session.commit()
        flash('User unblocked !')
        return redirect(url_for('adminsearch'))
    else:
        flash('User is not in blocklist !')
        return redirect(url_for('adminsearch'))
    

    
    



#------------------------------------------------------------------------------------------------------------
@app.route('/prof_profile/<int:profid>',methods=['GET','POST'])
def prof_profile(profid):
    prof=User.query.filter_by(id=profid).first()
    return render_template('prof_profile.html',prof=prof)

@app.route('/userdetails/<int:userid>',methods=['GET','POST'])
def userdetails(userid):
    u=User.query.filter_by(id=userid).first()
    return render_template('userdetails.html',user=u)

@app.route('/editdetails/<int:userid>',methods=['GET','POST'])
def editdetails(userid):
    u=User.query.filter_by(id=userid).first()
    services=Service.query.all()
    if request.method=='POST':
        email=request.form.get('email')
        fullname=request.form.get('fullname')
        address=request.form.get('address')
        pincode=request.form.get('pincode')
        if u.isProf:
            servicename=request.form.get('servicename')
            experience=request.form.get('experience')
            u.servicename=servicename
            u.experience=experience

        u.email=email
        u.fullname=fullname
        u.address=address
        u.pincode=pincode
        db.session.commit()
        return redirect(url_for('userdetails',userid=u.id))
    return render_template('editdetails.html',user=u,services=services)



#------------------------------------------------------------------------------------------------------------
@app.route('/viewservice/<int:servid>',methods=['GET','POST'])
def viewservice(servid):
    serv=Service.query.filter_by(id=servid).first()
    servname=serv.name
    profs=User.query.filter_by(servicename=servname).all()
    return render_template('viewservice.html',serv=serv,profs=profs)

@app.route('/servrequest/<int:servid>/<int:profid>',methods=['GET','POST'])
def servrequest(servid,profid):
    serv=Service.query.filter_by(id=servid).first()
    prof=User.query.filter_by(id=profid).first()
    curr_user=get_curr_user()
    cust=User.query.filter_by(id = curr_user['id']).first()
    if cust.isBlocked:
        flash('Not allowed !')
        return redirect(url_for('customerdash'))
    else:
        return render_template('servrequest.html',serv=serv,cust=cust,prof=prof)

@app.route('/req_serv/<int:servid>/<int:profid>',methods=['GET','POST'])
def req_serv(servid,profid):
    serv=Service.query.filter_by(id=servid).first()
    servname=serv.name
    profs=User.query.filter_by(servicename=servname).all()

    sid=request.form.get('servid')
    pid=request.form.get('profid')
    cid=request.form.get('custid')
    reqdate=request.form.get('comp_date')

    reqdate=datetime.strptime(reqdate,'%Y-%m-%d') if reqdate else None

    if sid and pid and cid and reqdate:
        newservreq=ServiceRequest.query.filter_by(prof_id=pid).first()
        compdate=[]
        if newservreq:
            compdate=newservreq.comp_date
            if compdate==reqdate:
                flash('service request already exsists')
                return redirect(url_for('servrequest',servid=sid,profid=pid))
            newservreq=ServiceRequest(service_id=sid,prof_id=pid,customer_id=cid,comp_date=reqdate)
            db.session.add(newservreq)
            db.session.commit()
        else:
            newservreq=ServiceRequest(service_id=sid,prof_id=pid,customer_id=cid,comp_date=reqdate)
            db.session.add(newservreq)
            db.session.commit()
        return redirect(url_for('customerdash'))
    return render_template('customerdash.html',serv=serv,profs=profs)

@app.route('/editreq/<int:reqid>',methods=['GET','POST'])
def editreq(reqid):
    servrequest=ServiceRequest.query.filter_by(id=reqid).first()

    if request.method=='POST':
        sid=request.form.get('servid')
        pid=request.form.get('profid')
        cid=request.form.get('custid')
        reqdate=request.form.get('comp_date')
        reqdate=datetime.strptime(reqdate,'%Y-%m-%d') if reqdate else None

        servrequest.service_id=sid
        servrequest.prof_id=pid
        servrequest.customer_id=cid
        servrequest.comp_date=reqdate
        db.session.commit()
        flash('Service request updated !')
        return redirect(url_for('customerdash'))
    return render_template('editreq.html',req=servrequest)


@app.route('/acceptreq/<int:reqid>',methods=['GET','POST'])
def acceptreq(reqid):
    servrequest=ServiceRequest.query.filter_by(id=reqid).first()
    if servrequest:
        servrequest.serv_stat='assigned'
        db.session.commit()
        flash('Service request accepted !')
        return redirect(url_for('profdash'))
    return redirect(url_for('profdash'))

@app.route('/rejectreq/<int:reqid>',methods=['GET','POST'])
def rejectreq(reqid):
    servrequest=ServiceRequest.query.filter_by(id=reqid).first()
    if servrequest:
        servrequest.serv_stat='rejected'
        db.session.commit()
        flash('Service request rejected !')
        return redirect(url_for('profdash'))
    return redirect(url_for('profdash'))
@app.route('/exitreq/<int:reqid>',methods=['GET','POST'])
def exitreq(reqid):
    servrequest=ServiceRequest.query.filter_by(id=reqid).first()
    if servrequest:
        servrequest.serv_stat='exited'
        db.session.commit()
        flash('Service location exited !')
        return redirect(url_for('profdash'))
    return redirect(url_for('profdash'))

@app.route('/closereq/<int:reqid>',methods=['GET','POST'])
def closereq(reqid):
    servrequest=ServiceRequest.query.filter_by(id=reqid).first()
    if servrequest.serv_stat=='exited':
        servrequest.serv_stat='closed'
        db.session.commit()
        flash('Service closed !')
        return redirect(url_for('customerdash'))
        #return render_template('feedbackform.html',reqid=reqid)
    return redirect(url_for('customerdash'))

@app.route('/deletereq/<int:reqid>',methods=['GET','POST'])
def deletereq(reqid):
    servrequest=ServiceRequest.query.filter_by(id=reqid).first()
    db.session.delete(servrequest)
    db.session.commit()
    flash('Service request deleted!')
    return redirect(url_for('customerdash'))

#------------------------------------------------------------------------------------------------------------------------

@app.route('/feedback/<int:reqid>',methods=['GET','POST'])
def feedback(reqid):
    curr_user=get_curr_user()
    user=User.query.filter_by(id=curr_user['id']).first()
    servrequest=ServiceRequest.query.filter_by(id=reqid).first()
    prof=User.query.filter_by(id=servrequest.prof_id).first()
    return render_template('feedback.html',user=user,servrequest=servrequest,prof=prof)
@app.route('/feedbacked/<int:reqid>',methods=['GET','POST'])
def feedbacked(reqid):
    curr_user=get_curr_user()
    user=User.query.filter_by(id=curr_user['id']).first()
    servrequest=ServiceRequest.query.filter_by(id=reqid).first()
    prof=User.query.filter_by(id=servrequest.prof_id).first()
    rating=request.form.get('rating')
    remarks=request.form.get('remarks')
    rating=float(rating)
    if rating and rating>=0 and rating<=5:
        servrequest.remarks=remarks
        if prof.countrating is None:
            prof.countrating=0
        if prof.rating is None:
            prof.rating=rating
        else:
            prof.rating=round((prof.rating*prof.countrating + rating)/(prof.countrating+1.0),2)
            prof.countrating+=1

        db.session.commit()
        flash('Thank You for providing feedback !')
        return redirect(url_for('customerdash'))
    else:
        flash('Invalid value provided in rating !')
    return render_template('feedback.html',user=user,servrequest=servrequest,prof=prof)

@app.route('/ratecust/<int:reqid>',methods=['GET','POST'])
def ratecust(reqid):
    curr_user=get_curr_user()
    user=User.query.filter_by(id=curr_user['id']).first()
    servrequest=ServiceRequest.query.filter_by(id=reqid).first()
    cust=User.query.filter_by(id=servrequest.customer_id).first()
    return render_template('ratecust.html',user=user,servrequest=servrequest,cust=cust)

@app.route('/ratedcust/<int:reqid>',methods=['GET','POST'])
def ratedcust(reqid):
    curr_user=get_curr_user()
    user=User.query.filter_by(id=curr_user['id']).first()
    servrequest=ServiceRequest.query.filter_by(id=reqid).first()
    cust=User.query.filter_by(id=servrequest.customer_id).first()
    rating=request.form.get('rating')
    rating=float(rating)
    if rating and rating>=0 and rating<=5:
        if cust.rating is None:
            cust.rating=0.0
        if cust.countrating is None:
            cust.countrating=0
        cust.rating=round((cust.rating*cust.countrating+rating)/(cust.countrating+1.0),2)
        cust.countrating += 1
        db.session.commit()
        flash('Thank You for providing feedback !')
        return redirect(url_for('profdash'))
    else:
        flash('Invalid value provided in rating !')
    return render_template('ratecust.html',user=user,servrequest=servrequest,cust=cust)


@app.route('/adsummary',methods=['GET','POST'])
def adsummary():
    profs=User.query.filter_by(isProf=True).all()
    custs=User.query.filter_by(isCustomer=True).all()
    profcount=len(profs)
    custcount=len(custs)
    return render_template('adsummary.html',profcount=profcount,custcount=custcount)

@app.route('/profsummary',methods=['GET','POST'])
def profsummary():
    prof=get_curr_user()
    profid=prof['id']
    servreq=ServiceRequest.query.filter_by(prof_id=profid,serv_stat='requested').all()
    servassign=ServiceRequest.query.filter_by(prof_id=profid,serv_stat='assigned').all()
    servreject=ServiceRequest.query.filter_by(prof_id=profid,serv_stat='rejected').all()
    servclosed=ServiceRequest.query.filter_by(prof_id=profid,serv_stat='closed').all()
    reqcount=len(servreq)
    assigncount=len(servassign)
    rejectcount=len(servreject)
    closedcount=len(servclosed)
    return render_template('profsummary.html',reqcount=reqcount,assigncount=assigncount,rejectcount=rejectcount,closedcount=closedcount)

@app.route('/custsummary',methods=['GET','POST'])
def custsummary():
    cust=get_curr_user()
    custid=cust['id']
    servreq=ServiceRequest.query.filter_by(customer_id=custid,serv_stat='requested').all()
    servassign=ServiceRequest.query.filter_by(customer_id=custid,serv_stat='assigned').all()
    servreject=ServiceRequest.query.filter_by(customer_id=custid,serv_stat='rejected').all()
    servclosed=ServiceRequest.query.filter_by(customer_id=custid,serv_stat='closed').all()
    reqcount=len(servreq)
    assigncount=len(servassign)
    rejectcount=len(servreject)
    closedcount=len(servclosed)
    return render_template('custsummary.html',reqcount=reqcount,assigncount=assigncount,rejectcount=rejectcount,closedcount=closedcount)


if __name__=='__main__':
    app.run(debug=True)