from Connection import UDPConnection
from Decoder import DNSMessage
from Cache import Cache
import Config
             
if __name__ == "__main__":
    udp_connection_client = UDPConnection()
    udp_connection_client.bind(Config.IPaddr, Config.Port)
    cache = Cache()
    while True:
        """
        Receive query from client
        """
        dns_message = DNSMessage() 
        try:
            message = udp_connection_client.blocked_recv() # Get message from the client
        except ConnectionResetError:
            continue
        dns_message.parse_dns(message) # Parse the message received
        search_key = (dns_message.QueriesList[0].QNAME, dns_message.QueriesList[0].QTYPE) # the search key is for query the cache: qname and qtype
        transaction_id = dns_message.Header.TransactionID # The transaction ID of the query from client

        if Config.VERBOSE:
            print("Transaction ID:{}. Search Key: {}".format(transaction_id, search_key))
        """
        Find Answer in cache
        """
        if Config.VERBOSE:
            print("Cache: {}".format(cache.itemdict.keys()))
        cache_msg = cache.get(search_key) # Find the answer in the cache
        if cache_msg != Cache.ANSWER_EXPIRE and cache_msg != Cache.ANSWER_NOT_FOUND: # The answer is in the cache and it is not out of date
            if Config.CACHE_VERBOSE:
                print("Cache hit.")
            udp_connection_client.sendto(dns_message.changeTransactionID(cache_msg, transaction_id)) # Send the answer to the client directly
            continue
        else: # The answer is not found or out of date
            if Config.CACHE_VERBOSE:
                print("Cache miss :", cache_msg)
            """
            Forward query to upper level DNS sever
            """
            udp_connection_DNS = UDPConnection() # Connect to the upper level server
            udp_connection_DNS.sendto_server(message, Config.DNS_server_IPaddr, Config.DNS_server_Port) # Forward the query to the server
            try:
                message = udp_connection_DNS.blocked_recv() # Receive the response from the server
            except ConnectionResetError:
                continue
            dns_message.parse_dns(message) # parse
            if Config.VERBOSE:
                print("This smallest TTL is:", dns_message.minTTL)
            cache.append(search_key, message, dns_message.minTTL) # cache the answer
            udp_connection_client.sendto(dns_message.changeTransactionID(message, transaction_id)) # Send the answer to the client