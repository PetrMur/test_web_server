from app.utils.env import get_from_env


SERVER_HOST = get_from_env('HOST', default='0.0.0.0')
SERVER_PORT = get_from_env('PORT', default='5000')


MYSQL_CREDENTIALS = {
    'user': get_from_env('MYSQL_USER', 'mysql'),
    'password': get_from_env('MYSQL_PASSWORD', 'mysql'),
    'host': get_from_env('MYSQL_HOST', 'mysql'),
    'port': get_from_env('MYSQL_PORT', ''),
    'database': get_from_env('MYSQL_BASE', 'db')
}


REDIS_CREDENTIALS ={
    'password': get_from_env('REDIS_PASSWORD', ''),
    'host': get_from_env('REDIS_HOST', ''),
    'port': get_from_env('REDIS_PORT', ''),
    'user': get_from_env('REDIS_USER', '')
}
