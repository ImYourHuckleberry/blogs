#get session shit figured out


from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
#secret key

db = SQLAlchemy(app)

class Blog(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True)
    body = db.Column(db.String(99999))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
       
    def __init__(self, title, body):
        self.title = title
        self.body= body
        self.owner = owner

class User(db.Model):
    id=db.Column(db.Interger, primary_key=True)
    username = db.Column(db.String(16), unique=True)
    password = db.Column(db.String(25))
    #unsure if backref should really be owner
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, email, password):
        self.username = username
        self.password = password

@app.route('/blog', methods=['POST','GET'])
def index():
    if request.args:
        blog_id = request.args.get("id")
        blog = Blog.query.get(blog_id)

        return render_template('entry.html', blog=blog)

    else:
        blogs = Blog.query.all()
        return render_template('blog.html', blogs=blogs)


@app.route('/newpost', methods=['GET', 'POST'])
def add_blog():

    #think about what you'll 
    #need to do in your /newpost 
    #route handler function since 
    #there is a new parameter to 
    #consider when creating a blog entry.

    if request.method == 'GET':
        return render_template('newpost.html', title='Add a Blog Entry')


    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        title_error = ''
        body_error = ''
        

    if len(blog_title) < 1:
        title_error = 'Bad Title'

    if len(blog_body) < 1:
        body_error = 'Bad Body'

    if not title_error and not body_error:
        new_blog = Blog(blog_title, blog_body)
        db.session.add(new_blog)
        db.session.commit()
        query_param_url = "/blog?id=" + str(new_blog.id)
        return redirect(query_param_url)

    else:
        return render_template('newpost.html',title='Add a Blog Entry', title_error=title_error, body_error=body_error)

@app.route('/signup')

@app.route('/login')

#change /index to "/"?
@app.route('/index')

@app.route('/logout', methods=['POST'])
def logout():
    del session['username']
    return redirect('/')

if __name__ == '__main__':
    app.run()