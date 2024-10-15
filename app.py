from flask import Flask, render_template

def create_app():
    app = Flask(__name__, static_folder='statics')

    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/index')
    def index():
        return render_template('index.html')

    @app.route('/login')
    def login():
        return render_template('login.html')

    @app.route('/register')
    def register():
        return render_template('register.html')

    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')

    @app.route('/account')
    def account():
        return render_template('account.html')

    @app.route('/balance')
    def balance():
        return render_template('balance.html')

    @app.route('/deposit')
    def deposit():
        return render_template('deposit.html')

    @app.route('/withdrawal')
    def withdrawal():
        return render_template('withdrawal.html')

    @app.route('/transactions')
    def transactions():
        return render_template('transactions.html')

    @app.route('/admin')
    def admin():
        return render_template('admin.html')

    @app.route('/settings')
    def settings():
        return render_template('settings.html')

    @app.route('/profile')
    def profile():
        return render_template('profile.html')

    @app.route('/logout')
    def logout():
        return render_template('logout.html')

    @app.route('/error')
    def error():
        return render_template('error.html')

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

