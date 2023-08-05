# OneService

Wrapper around Flask aimed at conveniently creating microservices.

Features and limitations:
- `Microservice` creates a server that can call a handler method when `/` is hit (HTTP method is configurable)
- The handler method receives the request JSON data and must respond with a `(dict, int)` tuple containing
the response data and response status code

## Usage
```python
from oneservice import Microservice

def return_doubled(json_data: dict) -> (dict, int):
    return {"result": int(json_data["a"]) * 2}, 200

m = Microservice(handler=return_doubled)
m.start()
```

You may then hit the microservice and its health endpoint:
```bash
curl http://localhost:5000/health
curl -X POST -H "Content-Type: application/json" --data '{"a": 2}' http://localhost:5000/
```

See [/examples](examples) for more code usage samples.
