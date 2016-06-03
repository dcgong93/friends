
from system.core.model import Model
import re

class User(Model):
    def __init__(self):
        super(User, self).__init__()

    def register_user(self, reg_info):
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors = []

        if not reg_info['name']:
            errors.append('Name cannot be blank')
        elif len(reg_info['name']) < 2:
            errors.append('Name must be at least 2 characters long')
        if not reg_info['alias']:
            reg_info['alias']=reg_info['name']
        if not reg_info['email']:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(reg_info['email']):
            errors.append('Email format must be valid')
        if not reg_info['password']:
            errors.append('Password cannot be blank')
        elif len(reg_info['password']) < 8:
            errors.append('Password must be at least 8 characters long')
        elif reg_info['password'] != reg_info['pw_confirm']:
            errors.append('Password and confirmation must match')
        if not reg_info['dob']:
            errors.append('Must input Date of Birth')
        if errors:
            return {"status": False, "errors": errors}
        else:
            password = reg_info['password']
            pw_hash = self.bcrypt.generate_password_hash(password)
            reg_query = "INSERT INTO users(name, alias, email, pw_hash, dob, created_at) VALUES(:name, :alias, :email, :pw_hash, :dob, NOW())"
            reg_data = {
                'name': reg_info['name'],
                'alias': reg_info['alias'],
                'email': reg_info['email'],
                'pw_hash': pw_hash,
                'dob': reg_info['dob']
            }
            get_user_query = "SELECT * FROM users ORDER BY id DESC LIMIT 1"
            users = self.db.query_db(reg_query, reg_data)
            user = self.db.query_db(get_user_query)
            return {"status":True, 'users':users, 'user':user[0]}

    def login_user(self, user_info):
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        password = user_info['password']
        email = user_info['email']
        errors = []

        if not user_info['email']:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(user_info['email']):
            errors.append('Email format must be valid')
        if not user_info['password']:
            errors.append('Password cannot be blank')
        if errors:
            return {"status":False, "errors":errors}
        else:
            query = "SELECT * FROM users WHERE email = :email LIMIT 1"
            data = {'email': email}
            user = self.db.query_db(query, data)
            if user:
                if self.bcrypt.check_password_hash(user[0]['pw_hash'], password):
                    return {"status":True, 'user':user[0]}
                else:
                    errors.append('Incorrect password')
                    return {"status":False, "errors":errors}
            else:
                errors.append('Please enter valid email or password')
                return {"status":False, "errors":errors}

    def get_user_id(self,id):
        get_id_query = "SELECT * FROM users WHERE id= :id"
        data = {
            'id':id
        }
        return self.db.query_db(get_id_query, data)

    def show_friends(self,id):
        join = "SELECT * FROM users JOIN friends ON users.id = friends.user_id LEFT JOIN users AS users2 on users2.id = friends.friend_id WHERE users.id = :id"
        data = {'id':id}
        return self.db.query_db(join, data)

    def get_other_users(self,id):
        get_all = "SELECT * FROM users WHERE users.id NOT IN (SELECT friend_id FROM friends WHERE (user_id=:id OR friend_id=:id)) AND users.id != :id"
        data = {'id':id}
        return self.db.query_db(get_all, data)

    def add_friend(self, info):
        new_friend_query = "INSERT INTO friends (friend_id, user_id) VALUES (:friend_id, :user_id)"
        data = {
            'friend_id':info['friend_id'],
            'user_id':info['user_id']
        }
        return self.db.query_db(new_friend_query, data)

    def remove_friend(self, info):
        remove_query = "DELETE FROM friends WHERE user_id = :user_id AND friend_id = :friend_id"
        data = {
            'user_id':info['user_id'],
            'friend_id':info['friend_id']
        }
        return self.db.query_db(remove_query, data)
