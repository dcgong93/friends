
from system.core.controller import *

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)

        self.load_model('User')
        self.db = self._app.db

    def index(self):
        return self.load_view('index.html')

    def friends(self):
        id=session['id']
        user = self.models['User'].get_user_id(id)
        friends = self.models['User'].show_friends(id)
        other_users = self.models['User'].get_other_users(id)
        print "FRIENDS"
        print friends
        return self.load_view('friends.html', user=user[0], friends=friends, other_users=other_users)

    def profile(self, id):
        user = self.models['User'].get_user_id(id)
        return self.load_view('profile.html', user=user[0])

    def register(self):
        reg_info = {
            'name': request.form['name'],
            'alias': request.form['alias'],
            'email': request.form['email'],
            'password': request.form['password'],
            'pw_confirm': request.form['pw_confirm'],
            'dob': request.form['dob']
        }
        reg_status = self.models['User'].register_user(reg_info)
        if reg_status['status'] == True:
            session['id'] = reg_status['user']['id']
            return redirect('/friends')
        else:
            for message in reg_status['errors']:
                flash(message, 'reg_errors')
            return redirect('/')

    def login(self):
        login_info = {
            'email': request.form['email'],
            'password': request.form['password']
        }
        login_status = self.models['User'].login_user(login_info)
        if login_status['status'] == True:
            session['id'] = login_status['user']['id']
            session['name'] = login_status['user']['name']
            return redirect ('/friends')
        else:
            for message in login_status['errors']:
                flash(message, 'login_error')
            return redirect('/')

    def logout(self):
        session['id'] = []
        return redirect ('/')

    def add(self, friend_id):
        id = friend_id
        info={
            'friend_id':id,
            'user_id':session['id']
        }
        friend = self.models['User'].add_friend(info)
        return redirect ('/friends')

    def remove(self, friend_id):
        id=friend_id
        info={
            'friend_id':id,
            'user_id':session['id']
        }
        cut = self.models['User'].remove_friend(info)
        return redirect ('/friends')
