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


#@app.route('/simple_start_task')
#def call_method():
#    app.logger.info("Invoking Method ")
#    r = simple_app.send_task('tasks.longtime_add', kwargs={'x': 1, 'y': 2})
##    app.logger.info(r.backend)
#    return r.id


#@app.route('/simple_task_status/<task_id>')
#def get_status(task_id):

#    status = simple_app.AsyncResult(task_id, app=simple_app)
#    print("Invoking Method ")
#    return "Status of the Task " + str(status.state)


#@app.route('/simple_task_result/<task_id>')
#def task_result(task_id):
#    result = simple_app.AsyncResult(task_id).result
#    return "Result of the Task " + str(result)
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


