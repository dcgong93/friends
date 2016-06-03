
from system.core.router import routes

routes['default_controller'] = 'Users'
routes['POST']['/register'] = 'Users#register'
routes['GET']['/friends'] = 'Users#friends'
routes['GET']['/logout'] = 'Users#logout'
routes['POST']['/login'] = 'Users#login'
routes['GET']['/profile/<id>'] = 'Users#profile'
routes['/remove/<friend_id>'] = 'Users#remove'
routes['/add/<friend_id>'] = 'Users#add'
