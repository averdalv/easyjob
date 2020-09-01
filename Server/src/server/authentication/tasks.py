from celery.task import periodic_task
from datetime import timedelta
from authentication.models import User
from order.models import SimpleOrder
from chat.models import Message,Dialogue
@periodic_task(run_every=(timedelta(days=1)),name="send_message")
def send_message():
    print("SEND_MESSAGE TASK")
    admin = User.objects.filter(is_superuser=True).first()
    new_tasks = SimpleOrder.objects.all()
    users_to_send = User.objects.filter(isPerformer=True)
    for user in users_to_send.iterator():
        Message.objects.create(message_from=admin,message_to=user,text="Создано новых {} заданий".format(str(new_tasks.count())))
    