import logging


def setup(level='DEBUG'):
    logging.basicConfig(
        level=logging.getLevelName(level),
        filename='loader.log',
        format='%(asctime)s %(levelname)-8s %(filename)s => %(message)s',
        datefmt='%Y-%m-%d %H:%M',
    )
