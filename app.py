

from flask import Flask, render_template,request,redirect,url_for,flash
import smtplib
import os
app=Flask(__name__)
app.config["SECRET_KEY"]=os.environ.get("SECRET_KEY")
PASSWARD=os.environ.get("PASSWARD")
EMAIL=os.environ.get("EMAIL")
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/about")
def about():
    return render_template("about.html")
@app.route("/timing")
def timing():
    return render_template("class-timetable.html")
@app.route("/services")
def services():
    return render_template("services.html")
@app.route("/contact",methods=["GET","POST"])
def contact():
    name=request.form.get("name")
    email=request.form.get("email")
    phone_number=request.form.get("phone_number")
    comment=request.form.get("comment")
    print(name,email,phone_number,comment)
    if request.method=="POST":
        if name=="" or email=="" or phone_number=="" or comment=="":
            flash("Please fill all the fields")
            print("hi")
            return render_template("contact.html")
        
        with smtplib.SMTP("smtp.gmail.com",587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(EMAIL,PASSWARD)
            msg=f"Subject:New message from {name}\n\nName:{name}\nEmail:{email}\nPhone number:{phone_number}\nComment:{comment}"
            smtp.sendmail(EMAIL,EMAIL,msg)
            return redirect(url_for('home')) 
    return render_template("contact.html")
@app.route("/404")
def error():
    return render_template("404.html")
if __name__=="__main__":
    app.run(debug=True)