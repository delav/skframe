from client import Client

cli = Client(__name__)
sk = cli.rt


if __name__ == '__main__':
    cli.run()
