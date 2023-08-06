# webplane


## About



## Install

```bash
pip3 install --user webplane
```

## How to use
```python
from webplane import WebApp

class MyWebApp(WebApp):

    def index(self):
        return f'Hello from {self.path}'

MyWebApp().run()
```
