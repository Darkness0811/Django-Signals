from django.shortcuts import render
import threading
import time
from django.http import JsonResponse
from django.db import transaction
from .models import Item, Sales
from .utlis.rectangle import Rectangle

# Create your views here.

def test_signal(request):
    print("Caller thread:", threading.get_ident())

    start = time.time()

    with transaction.atomic(): # begin transition then commit or rollback
        Item.objects.create(name="demo")
        print("Caller inside transaction:",
            transaction.get_connection().in_atomic_block)

    end = time.time()

    print("Request total time:", end - start)

    return JsonResponse({"status": "done", "time": end-start})

def async_test_signal(request):
    print("Caller thread:", threading.get_ident())

    start = time.time()

    with transaction.atomic(): # begin transition then commit or rollback
        Sales.objects.create(name="demo")
        print("Caller inside transaction:",
            transaction.get_connection().in_atomic_block)

    end = time.time()

    print("Request total time:", end - start)

    return JsonResponse({"status": "done", "time": end-start})



def test_rectangle(request):
    start = time.time()

    r = Rectangle(10, 5)
    data = {"length" : 0, "width" : 0}
    for item in r:
        print(item)
        for key in item:
            data[key] = item[key]
    
    end = time.time()
    
    return JsonResponse({"status": "done", "time": end-start, "data": data})
