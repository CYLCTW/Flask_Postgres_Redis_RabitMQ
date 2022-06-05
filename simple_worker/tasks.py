import time
from celery import Celery
from celery.utils.log import get_task_logger
from sqlalchemy import create_engine
from redis import Redis
redis = Redis(host='redis', port=6379,charset="utf-8", decode_responses=True)
logger = get_task_logger(__name__)

app = Celery('tasks',
             broker='amqp://admin:mypass@rabbit:5672',
             backend='mongodb://mongodb_container:27017/mydb')
db_name = 'database'
db_user = 'username'
db_pass = 'secret'
db_host = 'postgres_container'
db_port = '5432'
# Connecto to the database
db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
db = create_engine(db_string)

#@app.task()
#def longtime_add(x, y):
 #   logger.info('Got Request - Starting work ')
#    time.sleep(4)
 #   logger.info('Work Finished ')
 #   return x + y
@app.task()
def Send_Message(user,mess):
    print(str(user)+" "+str(mess))
    db.execute("INSERT INTO Logger2 (username,message) " + \
               "VALUES (" + \
               str(user) + "," + \
               str(mess) + ");")
    print("Done")
    query = "" + \
            "SELECT * " + \
            "FROM Logger2 "
    result_set = db.execute(query)
    dannie = ""
    for (r) in result_set:
        dannie = dannie + "User: " + (str(r[0])) + " Message: " + (str(r[1])) + "\n"

    redis.setex(query, 3600, dannie)
    r="Send message"
    return r
@app.task()
def Get_Message():

    query = "" + \
            "SELECT * " + \
            "FROM Logger2 "
    result_set = db.execute(query)
    if redis.exists(query):
        f=redis.get(query)
        return f
        print("Yes")
    dannie = ""
    for (r) in result_set:
        dannie = dannie + "User: " + (str(r[0])) + " Message: " + (str(r[1])) + "\n"

    redis.setex(query,3600, dannie)
    return dannie


