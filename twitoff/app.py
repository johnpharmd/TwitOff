"""Main application and routing logic for TwitOff."""
from decouple import config
from flask import Flask, render_template, request
from .models import DB, User, Tweet
from .predict import predict_user
from .twitter import add_or_update_user


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['ENV'] = config('ENV')
    DB.init_app(app)

    @app.route('/')
    def root():
        users = User.query.all()
        tweets = Tweet.query.all()
        return render_template('baseone.html', title='Home', users=users,
                               tweets=tweets)

    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None):
        message = ''
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = 'User {} successfully added!'.format(name)
            tweets = User.query.filter(User.name == name).one().tweets
        except Exception as e:
            message = 'Error adding {}: {}'.format(name, e)
            tweets = []
        return render_template('user.html', title=name, tweets=tweets,
                               message=message)    
    
    @app.route('/compare', methods=['POST'])
    def compare():
        user1, user2 = request.values['user1'], request.values['user2']
        tweeted = request.values['tweet_text']
        if user1 == user2:
            return 'Cannot  compare a user to themself!'
        else:
            # 'prediction' changed to 'y, proba' -- HT SL/LSDS01
            y, proba = predict_user(user1, user2,
                                    request.values['tweet_text'])
            # 'prediction' changed to 'y'
            # return user1 if y else user2
            if y:
                return render_template('compare.html', user=user1,
                                       tweeted=tweeted, prediction=y,
                                       probability=round(proba*100, 3))

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('baseone.html', title='DB Reset!', users=[])

    return app
