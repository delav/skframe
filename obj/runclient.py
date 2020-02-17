from client import Client
from route import Router

cli = Client(__name__)
sk = Router()
# storage = cli.storage


if __name__ == '__main__':
    cli.run()
