from flask import Flask, redirect, render_template, request, session, url_for
from db import Database

db = Database()

app = Flask(__name__)
app.secret_key = 'nigga'


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/perform_login', methods=['POST'])
def perform_login():
    email = request.form.get('User_email')
    password = request.form.get('User_password')

    user = db.login(email, password)

    if user:
        session['user_id'] = user['id']
        session['user_name'] = user['name']
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html', message="Invalid email or password")



@app.route('/register')
def register_page():
    session['user_type'] = 'user'
    return render_template('register.html')


@app.route('/perform_registration', methods=['POST'])
def perform_registration():
    name = request.form.get('user_name')
    email = request.form.get('user_email')
    password = request.form.get('user_password')
    user_type = session.get('user_type')

    response = db.insert(name, email, password, user_type)

    if response:
        return redirect(url_for('index'))
    else:
        return render_template('login.html', message="Email already registered")



@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('index'))

    jobs = db.get_all_jobs()
    return render_template('dashboard.html', jobs=jobs)



@app.route('/jobs')
def list_jobs():
    jobs = db.get_all_jobs()
    return render_template('jobs.html', jobs=jobs)



@app.route('/search', methods=['POST'])
def search_job():
    keyword = request.form.get('keyword')
    jobs = db.search_job(keyword)
    return render_template('jobs.html', jobs=jobs)



@app.route('/apply/<int:job_id>')
def apply_job(job_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))

    user_id = session.get('user_id')
    db.apply_job(user_id, job_id)
    return redirect(url_for('dashboard'))



@app.route('/delete_application/<int:job_id>')
def delete_application(job_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))

    user_id = session.get('user_id')
    db.delete_application(user_id, job_id)
    return redirect(url_for('dashboard'))



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
