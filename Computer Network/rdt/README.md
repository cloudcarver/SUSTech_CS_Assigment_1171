# Lab 7 Assignment 3

Manually adjust the loss rate, corruption rate, delay rate and also delay duration in **udp.py**.

In this test, the parameters are:

```python
loss_rate=0.2, corruption_rate=0.2, delay_rate=0.2, delay=1
```

Manually send characters to the server and server will echo it back.



Go to Config.py and set **DEBUG = True**, you can see the details of the transmission. 

If you want to do more tests, please read the following instruction.

**Good luck.**





------

### Application Layer Reliable Data Transfer Protocol

author : Mike Chester Wang

----

Using Go-back N mechanism to implement an application layer reliable transfer protocol based on unreliable transfer protocol (UDP).

## Set up

```python
# print DEBUG information or not
DEBUG = True
# DEBUG = False

VERBOSE = True

# size of the udp socket buffer
BUFSIZE = 4096

# size of the segment (byte)
SEGMENT_SIZE = 1024

# the decoding format of the rdt socket
DEFAULT_CODING = 'utf-8'

# timeout
RDT_TIMEOUT = 1.5
RDT_TIMROUT_CHECKING_TIME = 0.1
RFT_WINDOW_SIZE = 10
```

If you want to see the details of the transmission, set **DEBUG = True**.

If **VERBOSE** is True, you can see the connection information

The **Segment size** should less than MSS - len(max_header) = 1448 bytes. The recommended value is **1024**.

If your received message is some messy code, you should check the encoding at first. The default encoding is **UTF-8**.



### Test

1. Start the sever by running Server.py at first

   Before start the server, plz check the ip address and port at first

```python
server_socket.bind(('127.0.0.1', 63000))
```

2. Run Test in Client.py

   There are three tests already offered in comments. You may "un"comment them to run the test.

   1. **Original Test** : Send a short string to the server, and the server will echo it back.
   
    	2. **Manually sending test** : Input the string you want to send, and the server will echo it back
    	3. **Large Text Test** : Read a file and send the content to the server, and the server will echo it back.

`EOF`
