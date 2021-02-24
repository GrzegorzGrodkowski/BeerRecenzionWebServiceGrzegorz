import beerrecenzionservice as brs


if __name__ == "__main__":
    app = brs.create_app()
    app.run()
