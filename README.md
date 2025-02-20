
# Part 1

First, start the server:

```bashCopypython udp_server.py```

Then, in a separate terminal, run the client with the desired payload size (in MB):

```bashCopypython udp_client.py 50  # For example, to send 50 MB```

# Part 2

First, start the server:

```bashCopypython server.py```

Then start the proxy server in a different terminal:

```bashCopypython proxy_server.py```

Finally, run the client with a 4-character message in another terminal:

``` bashCopypython client.py PING ```

## Blocked IP
```
data = {
    "server_ip": "192.168.1.100",  # This IP is blocked
    "server_port": 7000,
    "message": "PING"
}
```
