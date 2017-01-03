# eventer-client
A Python client for the Eventer platform

## Example usage

```python

    event = Event(category="585a34dfa3b2ac2a641e6eb6", url="http://localhost/api")

    event.filename = "hello_world.exe"
    event.extension = "exe"
    event.size = 1099910
    event.submit()
    
```

or 

```python

    Event.from_dict("585a34dfa3b2ac2a641e6eb6",
                    "http://localhost/api",
                    {
                        "filename": "hello_world.exe",
                        "extension": "exe",
                        "size": 1099910
                    }).submit()

```
