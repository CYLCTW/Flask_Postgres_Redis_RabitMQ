try:
    import pika
    import flask
    import boto3
    from celery import Celery
    import pymongo
    from redis import Redis
except Exception as e:
    print("Error  :{} ".format(e))
app = flask.Flask(__name__)
simple_app = Celery('simple_worker',
                    broker='amqp://admin:mypass@rabbit:5672',
                    backend='mongodb://mongodb_container:27017/mydb')
@app.route('/sendMessage',methods=['POST'])
def sendMessage():
    username = flask.request.values.get('user')  # Your form's
    message = flask.request.values.get('message')
    app.logger.info("Invoking Method ")
    r = simple_app.send_task('tasks.Send_Message', kwargs={'user': username, 'mess': message})
    result = simple_app.AsyncResult(str(r.id)).result
    app.logger.info(r.backend)
    return str(result)
@app.route('/getChat',methods=['GET'])
def getChat():
    app.logger.info("Invoking Method ")
    r = simple_app.send_task('tasks.Get_Message')
    result = simple_app.AsyncResult(str(r.id)).result
    app.logger.info(r.backend)
    return str(result)


