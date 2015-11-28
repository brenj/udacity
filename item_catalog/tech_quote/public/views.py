"""Public views for tech_quote (homepage, etc...)."""

from flask import Blueprint, flash, redirect, request, url_for
from flask.ext.login import login_user, logout_user, login_required

from tech_quote.extensions import login_manager
from tech_quote.models.quote import Quote
from tech_quote.models.user import User
from tech_quote.oauth.providers import GitHubSignIn
from tech_quote.utils import with_template

blueprint = Blueprint(
    'public', __name__, static_folder='../static',
    template_folder='templates/public')

login_manager.login_view = 'public.index'
login_manager.login_message_category = 'danger'


@login_manager.user_loader
def load_user(user_id):
    """Reload the user object from the user ID stored in the session."""
    return User.query.get(user_id)


@blueprint.route("/logout")
@login_required
def logout():
    """User will be logged out, and their session will be cleaned up."""
    logout_user()
    return redirect(url_for('public.index'))


@blueprint.route('/')
@blueprint.route('/quotes')
@blueprint.route('/quotes/<int:page>')
@with_template()
def index(page=1):
    """Render TQ Homepage."""
    quotes = Quote.get_quotes_with_pagination(page)

    prev_page = url_for('public.index', page=quotes.prev_num)
    next_page = url_for('public.index', page=quotes.next_num)

    return dict(quotes=quotes, prev_page=prev_page, next_page=next_page)


@blueprint.route('/login/oauth/github')
def login_with_github():
    """Log a user in with GitHub OAuth credentials."""
    return redirect(GitHubSignIn().service.get_authorize_url())


@blueprint.route('/login/oauth/github/authorized')
def handle_github_redirect():
    """Handle redirect from GitHub access request (/login/oauth/github')."""
    code = request.args['code']

    session = GitHubSignIn().service.get_auth_session(data={'code': code})
    github_user_data = session.get('user').json()

    user = User.by_github_id(github_user_data['id'])
    if user is None:
        user = User.create(
            user_email=github_user_data['email'],
            user_name=github_user_data['name'],
            user_github_id=github_user_data['id'],
            user_github_login=github_user_data['login'],
            user_avatar_url=github_user_data['avatar_url'])

    login_user(user)
    flash("Logged in successfully!", 'success')

    return redirect(
        url_for('user.profile', user_login=user.user_github_login))
