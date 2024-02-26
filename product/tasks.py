from celery import shared_task
from .FCMmanage import sendPush
from .models import Discount,Recall
from rest_framework.response import Response
from rest_framework import status
from Shopx.celery import app

@app.task
def send_push_notification(id, title, tokens):

    instance = Discount.objects.get(pk=id)

    message = ''
    message += f'скидка на {instance.product.name}\n'
    message += f'цена до {instance.price}\n'
    message += f'цена со скидкой {instance.discount_rate}\n'

    
    result = sendPush(title=title,
                    registration_token=tokens.split(),
                    msg = message
                    ,
                    )
    return result



@app.task
def send_push_notification_recall(title, tokens):
    message = 'Отзыв'

    
    result = sendPush(title=title,
                    registration_token=tokens.split(),
                    msg = message
                    ,
                    )
    return result