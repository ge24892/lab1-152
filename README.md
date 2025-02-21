
# Part 1

First, start the server:

```python udp_server.py```

Then, in a separate terminal, run the client with the desired payload size (in MB):

```python udp_client.py 50  # For example, to send 50 MB```

# Part 2

First, start the server:

```python server.py```

Then start the proxy server in a different terminal:

```python proxy_server.py```

Finally, run the client with a 4-character message in another terminal:

``` python client.py PING ```

## Blocked IP
```
data = {
    "server_ip": "192.168.1.100",  # This IP is blocked
    "server_port": 7000,
    "message": "PING"
}
```
