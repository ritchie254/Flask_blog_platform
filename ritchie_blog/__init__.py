from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from ritchie_blog.models.all_models import User, Base
from ritchie_blog.auth import bp


app = Flask(__name__)

engine = create_engine('mysql+pymysql://root:root@localhost/ritchie', pool_pre_ping=True)

#creating all tables
Base.metadata.create_all(engine)


#register blueprints
app.register_blueprint(bp)

@app.route('/', strict_slashes=False)
def home():
    return render_template('layout.html')


if __name__ == '__main__':
    app.run(port=5000, debug=True, host='0.0.0.0')
