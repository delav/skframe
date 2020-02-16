from client import Client
from client import Router

cli = Client(__name__)
sk = Router()


if __name__ == '__main__':
    cli.run()
