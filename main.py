import mysql.connector
from loguru import logger
import time
import valve.source.a2s
import telegram
import config
import functions as func
from datetime import datetime
import numpy

logger.add("newplayers.log", format="{time} {level} {message}", level="DEBUG", rotation="30 KB", compression="zip")

db = mysql.connector.connect(
	host=config.host,
	user=config.user,
	password=config.passw,
	database=config.db
)
cursor = db.cursor(buffered=True)

cursor.execute("""CREATE TABLE IF NOT EXISTS online(
    online INT(2),
    date VARCHAR(25),
    server VARCHAR(50) 
);""")
logger.success("Success db connection")
while True:
    try:
        for i in range(1420):
            timee = datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")
            for server in config.servers:
                cursor.execute("INSERT INTO online(online, date,  server) VALUES (%s, %s, %s)", (func.get_online(server), timee, str(server)))        
            db.commit()
            time.sleep(90)   
        q = datetime.strftime(datetime.now(), "%Y.%m.%d")
        otvet='' 
        for server in config.servers:        
            cursor.execute(f"""SELECT online FROM online WHERE server LIKE "{server}" AND date LIKE "{q}%" """)
            arr = cursor.fetchall()       
            otvet += f">{server[0]}:{server[1]}\n Средний онлайн - {str(func.toFixed(numpy.mean(arr), 2))}\n Максимальный онлайн - {str(max(arr)[0])}\n\n"

        telegram.send_notificaton(text=otvet)
    except Exception as e:
        logger.error(e)
        telegram.send_notificaton(text='error')
        continue           
