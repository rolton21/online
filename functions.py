import valve.source.a2s
from loguru import logger
import telebot
import config 

def get_online(server):
    try:
        with valve.source.a2s.ServerQuerier(server) as srv:
            info = srv.info()
            return "{player_count}".format(**info)
    except valve.source.NoResponseError:
        logger.warning(str(server) + "not respond")
        return 0

# chars after ,
def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"        