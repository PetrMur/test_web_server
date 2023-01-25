from app.server.aiohttp_server import Server
from app.utils.logger import start_logging, Logger
from settings.credentials import SERVER_HOST, SERVER_PORT


@start_logging
def main():
    Logger().info('Starting aiohttp server {} {}'.format(SERVER_HOST, SERVER_PORT))
    Server().run(SERVER_HOST, SERVER_PORT)


if __name__ == '__main__':
    main()
