## Simple Local DNS Resolver

#### Set up

- Open `config.php` to set up server IP, the IP address of the upper level DNS server. The port number is always 53 for DNS server. 

  ```python
  # Basic settings #
  IPaddr = '127.0.0.1'
  Port = 53
  ```

  `VERBOSE` is the argument to decide whether the server will print the state message or not.

  ```python
  # Runtime settings #
  VERBOSE = True
  ```

  Also, don't forget to set up the IP address of the upper level DNS server

  ```python
  DNS_server_IPaddr = '172.18.1.92' # ns1.sustech.edu.cn
  ```

  *note : This ip address is okay if the you use SUSTC-WiFi.*

- Run server

  ```bash
  $ python DNSolver.py
  ```

  If `VERBOSE = True`, the sever will print `UDP connection is set up.`



#### dig Test

- Use dig to test the local resolver

  ```bash
  $ dig @127.0.0.1 baidu.com
  ```

  *note : the server IP is 127.0.0.1 in this example*

​		The query time is 293 msec for the first retrieve

​		![1571025390088](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\1571025390088.png)



​		The query time is 2 msec for the second retrieve

​		![1571025437463](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\1571025437463.png)

​		

​		The query time is much shorted than the first retrieve since the answer is cached.



#### Global Test

- For the windows users, find `使用下面的DNS服务器地址(E)` in `控制面板>所有控制面板项>网络连接>右击所用网络>属性>Internet协议版本4(TCP/IPv4)`, and fill the blank with your server's IP address:

  ![1571029614944](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\1571029614944.png)

-  The cache will soon be filled with many queries and their answer.

  ```bash
  Receive 30 bytes from ('127.0.0.1', 60052)
  Transaction ID:45490. Search Key: ('www.iana.org', 28)
  Cache: dict_keys([('clients1.google.com', 1), ('clients1.google.com', 28), ('config.pinyin.sogou.com', 1), ('ping.pinyin.sogou.com', 1), ('config.pinyin.sogou.com', 28), ('ping.pinyin.sogou.com', 28), ('download.pinyin.sogou.com', 1), ('download.pinyin.sogou.com', 28), ('vortex.data.microsoft.com', 1), ('vortex.data.microsoft.com', 28), ('www.baidu.com', 1), ('www.baidu.com', 28), ('ss1.bdstatic.com', 1), ('cambrian-images.cdn.bcebos.com', 1), ('ss1.bdstatic.com', 28), ('cambrian-images.cdn.bcebos.com', 28), ('ss0.bdstatic.com', 1), ('ss0.bdstatic.com', 28), ('ss0.baidu.com', 1), ('ss0.baidu.com', 28), ('ss2.baidu.com', 1), ('ss2.baidu.com', 28), ('sp1.baidu.com', 1), ('sp1.baidu.com', 28), ('sp0.baidu.com', 1), ('sp0.baidu.com', 28), ('accounts.google.com', 1), ('accounts.google.com', 28), ('www.sogou.com', 1), ('www.sogou.com', 28), ('suggestion.baidu.com', 1), ('suggestion.baidu.com', 28), ('example.com', 1), ('example.com', 28), ('www.iana.org', 1)])    
  Cache miss : ANSWER_NOT_FOUND
  Send 30 bytes to 172.18.1.92:53
  Receive 262 bytes from ('172.18.1.92', 53)
  Send 262 bytes to ('127.0.0.1', 60052)
  ```

- The local resolver behave well like nothing changes.

- If we turn off the server, the browser and the other network application are not working.

  ![1571029897162](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\1571029897162.png)



#### Feature

- Only UDP is used.

- The cache will keep the answer of the DNS query, and return the answer back to the client if the answer is out of date (determined by time-to-live).

- The cache is only stored in the memory. The cache will be empty after reboot.
- The server handle requests in sequential way. That means ioloop or threading technique are not used. Since the DNS request will be sent for several times until the client gets the answer, multi-threading or ioloop are not needed for simplicity concern.