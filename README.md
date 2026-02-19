# Django Signals Assignment

## Implementation

* Signals implemented in: `core/signals.py`
* Model used: `core/models.py`
* Views used for testing: `core/views.py`
* Rectangle class: `core/utils/rectangle.py`

---

## Setup

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Server runs at:

```
http://127.0.0.1:8000/
```

---

## Endpoints Used

| Endpoint       | Purpose                                     |
| --------       | ---------                                   |
| `/test/`       | Test Django signal behaviour                |
| `/async_test/` | Test Django signal behaviour with threading |
| `/rect/`       | Test Rectangle iterator                     |

---

# Django Signals – Answers

---

## Question 1

### By default are Django signals synchronous or asynchronous?

### Implementation

`core/signals.py`

```python
@receiver(post_save, sender=Item)
def item_saved(sender, instance, **kwargs):
    print("Sleeping 3 seconds inside signal...")
    time.sleep(3)
```

### Observation

When hitting:

```
/test/
```

Console output:

```
Request total time: 3.36482572555542
"GET /test/ HTTP/1.1" 200 44

```

The HTTP response waits until the signal finishes execution.

### Conclusion

> Django signals are **synchronous by default**.

The request is blocked until the signal handler completes.

---

## Question 2

### Do Django signals run in the same thread as the caller?

### Implementation

Thread IDs printed from both view and signal:

```python
print("Caller thread:", threading.get_ident())
print("Signal thread:", threading.get_ident())
```

### Observation

Console output:

```
Caller thread: 10424
Signal thread: 10424
```

Both IDs are identical.

### Conclusion

> Django signals execute in the **same thread** as the caller by default.

No new thread or async worker is created automatically.

---

## Question 3

### Do Django signals run in the same database transaction as the caller?

### Implementation

```python
with transaction.atomic():
    Item.objects.create(name="demo")
```

Inside both view and signal:

```python
transaction.get_connection().in_atomic_block
```

### Observation

Console output:

```
Inside transaction: True
Caller inside transaction: True
```

### Conclusion

> Django signals run inside the **same database transaction** as the caller.

The signal executes before the transaction is committed.

---

## Execution Flow Summary

When `/test/` is called:

```
View starts
   ↓
Item.objects.create()
   ↓
Model save()
   ↓
post_save signal executes
   ↓
Control returns to view
   ↓
Transaction commits
   ↓
Response returned
```

Signals are triggered internally during `model.save()`.

---

Response:

```
{
  "status": "done",
  "time": 3.36482572555542
}

```

full Console output:

```
Caller thread: 10424

--- SIGNAL START ---
Signal thread: 10424
Sleeping 3 seconds inside signal...
Inside transaction: True
--- SIGNAL END ---

Caller inside transaction: True
Request total time: 3.36482572555542
"GET /test/ HTTP/1.1" 200 44
```


# Bonus — Async Demonstration

By default, signals are synchronous.

To demonstrate async behaviour, work was offloaded using a background thread.

Example:

```python
def async_task(instance_id):
    print("ASYNC TASK START (thread):", threading.get_ident())
    time.sleep(3)
    print("ASYNC TASK DONE for Item:", instance_id)
threading.Thread(target=async_task, args=(instance.id,), daemon=True).start()
```

### Observation

When hitting:

```
/async_test/
```

Console output:

```
Caller thread: 20224
Signal thread: 20224

ASYNC TASK START (thread): 24440
Signal finished immediately
Caller inside transaction: True
Request total time: 0.5045957565307617
"GET /async_test/ HTTP/1.1" 200 46
ASYNC TASK DONE for Item: 3

```
Response:

```
{
  "status": "done",
  "time": 0.504595756530762
}

```
### Result

* HTTP request returns immediately
* Background task continues execution

### Note

Threading is used only for demonstration.

In real production systems, asynchronous processing should be handled using:

* Celery
* Redis / RabbitMQ
* Background task queues

---

# Custom Python Class — Rectangle

## Requirement

* Initialize with `length` and `width`
* Instance should be iterable
* Iteration order:

  1. `{'length': value}`
  2. `{'width': value}`

---

## Implementation

`core/utils/rectangle.py`

```python
class Rectangle:
    def __init__(self, length: int, width: int):
        self.length = length
        self.width = width

    def __iter__(self):
        yield {"length": self.length}
        yield {"width": self.width}
```

---

## Example Usage

```python
r = Rectangle(10, 5)

for item in r:
    print(item)
```

console Output:

```
{'length': 10}
{'width': 5}
```

Response:

```
{
  "status": "done",
  "time": 0,
  "data": {
    "length": 10,
    "width": 5
  }
}

```

---

# Key Learnings

* Django signals are synchronous by default.
* Signals execute in the same thread.
* Signals execute inside the same database transaction.
* Async behaviour requires explicit offloading (threading / Celery).
* Python iterators can be implemented using `yield`.

---

#

Assignment implementation for Django Signals and Custom Python Classes.
