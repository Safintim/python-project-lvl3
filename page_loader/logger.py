import logging


def setup(level="INFO"):
    logging.basicConfig(
        level=logging.getLevelName(level),
        filename="page-loader.log",
        format="%(asctime)s %(levelname)-8s %(filename)s => %(message)s",
        datefmt="%Y-%m-%d %H:%M",
    )
