import json

import pika, sys, os
from django.core.management.base import BaseCommand
from transaction.models import Vehicle


class Command(BaseCommand):
    def handle(self, *args, **options):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='cross-info')

        def callback(ch, method, properties, body):
            json_body = json.loads(body)
            plate = json_body.get('license_plate')
            vehicle_type = json_body.get('type')
            vehicle = Vehicle.objects.filter(license_plate=plate).first()
            if vehicle:
                vehicle.type = vehicle_type
                vehicle.save()
            else:
                Vehicle.objects.create(license_plate=plate, type=vehicle_type)
            print(f'[*] Finished create/update vehicle')

        channel.basic_consume(queue='vehicle', on_message_callback=callback, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()