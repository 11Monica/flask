# all the imports
import os
import sqlite3
from flask import Flask,request,session,g,redirect,url_for,abort,render_template,flash


#create our little application:)
app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g,'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db
@app.teardown_appcontext
def close_db(error):
    if hasattr(g,'sqlite_db'):
        g.sqlite_db.close()

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read()) 
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

'''@app.route('/')
def show_entries():
    db=get_db()
    cur = db.execute('select title,text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html',entries=entries)'''

##person
@app.route('/' , methods=['GET','POST'])   #if not methods,the code of update_person will Method Not Allowed The method is not allowed for the requested URL.
def show_persons():
    db=get_db()
    cur = db.execute('select name, tel, studentid,sex,tel,emile,class,department,self_introduction from persons order by id desc')
    persons = cur.fetchall()
    return render_template('show_persons.html',persons=persons)

'''@app.route('/add',methods=['post'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title,text) values (?,?)',
                [request.form['title'],request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))'''

#person
@app.route('/add_per',methods=['POST'])
def add_person():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into persons (name,studentid,sex,tel,emile,class,department,self_introduction) values (?, ?, ?, ?, ?, ?, ?, ?)',
                [request.form['name'],request.form['studentid'],request.form['sex'],request.form['tel'],request.form['emile'],request.form['class'],request.form['department'],request.form['self_introduction']])
    db.commit()
    flash('New person was successfully posted')
    return redirect(url_for('show_persons'))


@app.route('/login',methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logger in')
            return redirect(url_for('show_persons'))
            
    return render_template('login.html',error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    flash('You were logged out')
    return redirect(url_for('show_persons'))

#update
'''@app.route('/<string:person_id>',methods=['PUT'])
def update_person(person_id):
    person=file(lambda a:a['personid'] == person_id,persons)
    if len(person)==0:
        about(404)'''
#delet
@app.route('/person/<int:person_id>/del',methods=['GET'])
def delete_person(person_id):
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('DELETE from persons where studentid = %d' %person_id )
    db.commit()
    flash('Person was successfully deleted')
    return redirect(url_for('show_persons'))
#udate
@app.route('/person/update',methods=['GET', 'POST'])
def update_person() :
    error = None
    if not session.get('logged_in'):
        abort(401)
    if request.method == 'POST':
        db = get_db()
        db.execute("update persons set name=?, studentid=?,sex=?,tel=?,emile=?,class=?,department=?,self_introduction=?  where studentid = ? " ,[request.form['name'],request.form['studentid'],request.form['sex'],request.form['tel'],request.form['emile'],request.form['class'],request.form['department'],request.form['self_introduction'], request.form['studentid']]  )
        db.commit()
        flash('Successfully update')
        return redirect(url_for('show_persons'))
    else:
        return render_template('update_person.html',error=error)
   
    
if __name__ == '__main__':
    app.run()