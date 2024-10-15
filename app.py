from flask import Flask, render_template

def create_app():
    app = Flask(__name__, static_folder='statics')  # Specify the static folder name

    @app.route('/')
    def home():
        return render_template('dashboard.html')  # Render the dashboard.html template

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
