
from dataclasses import dataclass
from flask import render_template, request, flash, url_for,redirect
from zetta_app.forms import LoginForm,zetta_form,RegistrationForm,RequestResetForm, ResetPasswordForm
from zetta_app import app,db,mail
from zetta_app.forms import zetta_form,UpdateAccountForm
from zetta_app.models import User,zetta_dbform
from flask_login import login_required,logout_user,login_user,current_user
from flask_mail import Message
import joblib
import pandas as pd
rf_model=joblib.load('random_forest.pkl')

@app.route('/predictor_form',methods=['GET','POST'])
@login_required
def predictor(): 
    form=zetta_form()
    flash(f"Hey Hello {current_user.name}")
    
    return(render_template("predictor_form.html",form=form))

@app.route('/',methods=['POST','GET'])
@app.route('/login',methods=['POST','GET'])  
def login():  
    print(current_user)
    if current_user.is_authenticated:
        flash(f"Hey Hello {current_user.name}")
        return(redirect(url_for('predictor')))
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if (user) and (user.password==form.password.data):
            login_user(user)
            flash(f"logged in successfully")
            return(redirect(url_for('predictor')))
        else:
            flash('check password and email')
        
    return render_template('login.html',form=form)




@app.route('/dashboard',methods=['POST','GET'])  
@login_required
def dashboard():
    if request.method=='POST':
        new_form=zetta_dbform(patient_name=request.form['patient_name'],
            age=request.form['age'],
            weight=request.form['weight'],
            bmi=request.form['bmi'],
            blood_pressure=request.form['blood_pressure'],
            insulin=request.form['insulin'],
            cardio=request.form['cardio_stress_level'],
            liver=request.form['liver_stress_level'],
            smoking=request.form['smoking_history_in_years'],
            )
        db.session.add(new_form)
        db.session.commit()
        data_for_predictions=[int(request.form['age']),
        int(request.form['weight']),
        float(request.form['bmi']),
        int(request.form['blood_pressure']),
        int(request.form['insulin']),
        int(request.form['cardio_stress_level']),
        float(request.form['liver_stress_level']),
        float(request.form['smoking_history_in_years'])]
        disease_probability=rf_model.predict_proba(pd.DataFrame(data_for_predictions).T)[0][1]
        flash('form submitted successfully Here is The report')
        return(render_template("dashboard.html",disease_probability=disease_probability))
    flash(f"Hey Hello {current_user.name}")
    return(render_template("dashboard.html"))
  


@app.route('/register',methods=['POST','GET'])
def register(): 
    if current_user.is_authenticated:
        flash(f"Hey Hello {current_user.name}")
        return(redirect(url_for('predictor')))
    form=RegistrationForm()
    if form.validate_on_submit():
        user=User(username=form.username.data,
        email=form.email.data,
        name=form.name.data,
        designation=form.designation.data,
        
        contact=form.contact.data,
        gmail=form.gmail.data,
        password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        
        flash(f"user craeted successfully")
        return(redirect(url_for('login')))
    return render_template('register.html',form=form)



@app.route('/profile',methods = ['GET','POST'])  
@login_required
def profile(): 
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        
        flash('Your account has been updated!')
        return redirect(url_for('profile'))
    flash(f"Hey Hello {current_user.name}")
    return render_template('profile.html',form=form)
     

@app.route('/logout',methods = ['GET','POST'])  
@login_required
def logout():  
   logout_user()
   return redirect(url_for("login"))


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/reset_request", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('predictor'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.')
        return redirect(url_for('login'))
    return render_template('reset_request.html', form=form)


@app.route("/reset_token/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('predictor'))
    user = User.verify_reset_token(token)
    print(user)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        print(form.password.data)
        print(user.password)

        user.password = form.password.data
        db.session.commit()
        flash('Your password has been updated! You are now able to log in')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

def main(event,context):
    app.run(debug=True)
    print("New changes")
if __name__ == '__main__':  
   main()
