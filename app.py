from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class Todo(db.Model):
    sns=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(500),nullable=False)
    date=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno} {self.title}"


@app.route('/',methods=['GET','POST'])
def helloworld():
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTodo=Todo.query.all()
    
    return render_template('index.html',allTodo=allTodo)

@app.route("/show")
def products():
    allTodo=Todo.query.all()
    print(allTodo)
    return 

@app.route("/update/<int:sns>",methods=['GET','POST'])
def update(sns):
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo.query.filter_by(sns=sns).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo=Todo.query.filter_by(sns=sns).first()
    
    return render_template('update.html',todo=todo)    
@app.route("/delete/<int:sns>")
def delete(sns):
    todo=Todo.query.filter_by(sns=sns).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
