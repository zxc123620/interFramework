import datetime

import pika

# ########################## consumer ##########################
user_info = pika.PlainCredentials('zxc', '123456')
connection = pika.BlockingConnection(pika.ConnectionParameters('10.168.1.207', 5672, '/', user_info))
channel = connection.channel()

# create queue
# channel.queue_declare(queue='queue_get_pics')
file = open("报警.txt", "a", encoding="utf-8")


def callback(ch, method, properties, body):
    alarm = body.decode()
    now_date = datetime.datetime.now()
    alarm = eval(alarm)
    if alarm.get("isAlarmed", None) is not None and alarm.get("alarmTime", None) is not None and alarm.get("isAlarmed",
                                                                                                           None) == "1":
        info = "uuid: %s level: %s radar: %s alarmtime: %s now_time: %s \n" % (
            alarm.get("alarmUuid"), alarm.get("level"), alarm.get("radarId"), alarm.get("alarmTime"), str(now_date))
        file.write(info)
        file.flush()
        print(" [x] Received %r" % info)
    print(body.decode())


channel.basic_consume(
    'alarmQueue',
    callback,
    auto_ack=False
)

print('[*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
file.close()
channel.close()
