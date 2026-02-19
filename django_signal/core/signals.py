import threading
import time
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import Item, Sales


@receiver(post_save, sender=Item)
def item_saved(sender, instance, **kwargs):
    print("\n--- SIGNAL START ---")
    print("Signal thread:", threading.get_ident())

    print("Sleeping 3 seconds inside signal...")
    time.sleep(3)

    print("Inside transaction:", transaction.get_connection().in_atomic_block)
    print("--- SIGNAL END ---\n")



def async_task(instance_id):
    print("ASYNC TASK START (thread):", threading.get_ident())
    time.sleep(3)
    print("ASYNC TASK DONE for Item:", instance_id)


@receiver(post_save, sender=Sales)
def item_saved(sender, instance, **kwargs):
    print("Signal thread:", threading.get_ident())

    # Offload work to background thread
    threading.Thread(
        target=async_task,
        args=(instance.id,),
        daemon=True
    ).start()

    print("Signal finished immediately")