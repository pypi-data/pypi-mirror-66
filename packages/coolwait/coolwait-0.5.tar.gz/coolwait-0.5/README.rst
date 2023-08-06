# Example1
```python
from coolwait import pelangi
pelangi("Please wait...",delay=5,tab=2)
print("hello world")
```

# Example2
```python
import coolwait
from threading import Thread
from coolwait import pelangi

t=Thread(target=pelangi, args=("LOADING...",delay=None,tab=2))
t.start()

def do_something():
    import requests
    req=requests.get("https://google.com")
    coolwait.stop=True
    return req.text

run=do_something()
t.join()
print(run)
```
