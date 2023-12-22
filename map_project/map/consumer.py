import pika
from map.models import Location
def callback(ch, method, properties, body):
    action = method.routing_key
    print(f"Method called: {method.routing_key}")
    print(f"Properties: {properties}")
    print(f"Received message: {body}")
    if("incident_deletion"==action):
        print(f"INCIDENT DELETION ACTION")
        id = int(body)
        print(f"ID:{id}")
        location = Location.objects.get(id=id)
        print(f"{location}")

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',port=5672,virtual_host='/'))
channel = connection.channel()

channel.queue_declare(queue='incident_deletion')
channel.basic_consume(queue='incident_deletion', on_message_callback=callback, auto_ack=True)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
