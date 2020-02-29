import pika

def cloud(sender):
    credentials = pika.PlainCredentials('admin', 'Prince@99')

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='165.22.222.1',
                                    credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='json')

    data = {
        "from": sender
    }
    message = json.dumps(data)

    channel.basic_publish(exchange='', routing_key='json', body=message)
    print(" [x] Sent The JSON Data")
    connection.close()