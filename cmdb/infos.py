import configparser
import os


def db_infos(sec, opts):
    path = "{}/{}".format(os.getenv('IMP'), 'app.ini')
    config = configparser.ConfigParser()
    config.read(path)
    try:
        res = config.get(sec, opts)
    except KeyError:
        return -1
    return res

