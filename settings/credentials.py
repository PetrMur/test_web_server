from app.utils.env import get_from_env


SERVER_HOST = get_from_env('HOST', default='127.0.0.1')
SERVER_PORT = get_from_env('PORT', default='5000')


MYSQL_CREDENTIALS = {
    'user': get_from_env('MYSQL_USER', 'mysql'),
    'password': get_from_env('MYSQL_PASSWORD', 'password'),
    'host': get_from_env('MYSQL_HOST', '127.0.0.1'),
    'port': get_from_env('MYSQL_PORT', '3306'),
    'database': get_from_env('MYSQL_BASE', '')
}


REDIS_CREDENTIALS = {
    'password': get_from_env('REDIS_PASSWORD', ''),
    'host': get_from_env('REDIS_HOST', '127.0.0.1'),
    'port': get_from_env('REDIS_PORT', '6379'),
    'user': get_from_env('REDIS_USER', '')
}

DADATA = {
    'token': get_from_env('DADATA_TOKEN', ''),
    'secret': get_from_env('DADATA_SECRET', '')
}
