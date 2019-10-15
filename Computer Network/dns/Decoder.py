import Config
import Util
import struct

# This is a tool function to assemble the each part of the domain name in a list
# and return a domain name string
def parse_domain_name_list(domain_name_list):
    if(len(domain_name_list) == 0):
        return "0"
    domain_name = ""
    for i in range(0, len(domain_name_list)):
        domain_name += str(domain_name_list[i].decode())
        if(i != len(domain_name_list) - 1):
            domain_name += "."
    return domain_name

# The instance of this class is to help decode the DNS message.
class Query(object):

    def __init__(self):
        self.__dict__={field:None for field in ('length', 'QNAME', 'QTYPE', 'CLASS')}

    def __str__(self):
        return "---------Query---------\r\nQNAME : {}\r\nQTYPE : {}\r\nCLASS : {}".format(self.QNAME, self.QTYPE, self.CLASS)
        
class RescourceRecord(object):

    def __inti__(self):
        self.__dict__={field:None for field in ('length', 'NAME', 'TYPE', 'CLASS', 'TTL', 'RDLENGTH', 'RDATA')}

    def __str__(self):
        return "---------RR---------\r\nNAME : {}\r\nTYPE : {}\r\nCLASS : {}\r\nTTL : {}\r\nRDLENGTH : {}\r\nRDATA : {}".format(
            self.NAME, self.TYPE, self.CLASS, self.TTL, self.RDLENGTH, self.RDATA)

class Header(object):

    def __int__(self):
        self.__dict__={field:None for field in ('length', 'TransactionID', 'Flags', 'QuestionCnt', 'AnswerCnt', 'AuthorityRRCnt', 'AdditionalRRCnt',\
            'Response', 'Opcode', 'AA', 'Truncated', 'RecursionDesired', 'RA', 'Z', 'Non_authenticatedData', 'AD', 'RCode')}
        self.length = 12 # Length of DNS header
    def __str__(self):
        return "---------Header---------\r\nTransactionID : {}'\r\nQuestionCnt : {}'\r\nAnswerCnt : {}'\r\nAuthorityCnt : {}'\r\nAdditionalRRCnt : {}'\r\nResponse : {}'\r\nOpcode : {}'\r\nAA : {}'\r\nTruncated : {}'\r\nRecursionDesired : {}'\r\nRA : {}'\r\nZ : {}'\r\nNon_autenticatedData : {}'\r\nAD : {}'\r\nRCode : {}'\r\n".format(
                self.TransactionID, self.QuestionCnt, self.AnswerCnt, self.AuthorityRRCnt, self.AdditionalRRCnt,\
                self.Response, self.Opcode, self.AA, self.Truncated, self.RecursionDesired, self.RA, self.Z, self.Non_authenticatedData, \
                self.AD, self.RCode)

class DNSMessage:
    
    def __init__(self):
        self.Header = Header()
        self.QueriesList = []
        self.RRsList = []
        self.minTTL = 2147483647 #2^31 - 1

    def __str__(self):
        return "{}\r\n{}\r\n{}\r\n".format(str(self.Header), str(self.QueriesList), str(self.RRsList))

    # def toCachedByteStream(self):
    #     struct_format = ">" + self.Header.length + "s" + ()
    #     cached_rr_flag_list = []
    #     for rr in self.RRsList:
    #         if(rr.TTL > 0):
    #             cached_rr_flag_list.append(1)
    #         else:
    #             cached_rr_flag_list.append(0)

    #     byte_tuple = 
        

    # This is a tool function to replace the transaction ID of the answer
    # from the upper level DNS server before forwarding the answer to
    # the query process (client)
    def changeTransactionID(self, data, newID):
        data_length = len(data)
        struct_format = ">H" + str(data_length - 2) + "s"
        Struct = struct.Struct(struct_format)

        oldID, restPart = Struct.unpack_from(data)

        return struct.pack(struct_format, newID, restPart)

    # This method can parse the query dns message or the answer dns message from 
    # the upper level server to some dictionary:
    # 1. HeaderDict  : contains all the information of the DNS message header
    # 2. QueriesDict : contains the domain name, class and type of the query
    # 3. AnswerDict  : contains the name, type, class and time-to-live of the answer
    #                  from the upper level DNS server.
    def parse_dns(self, data):
        self.packetiterator = Util.PacketIterator(data, endian=">")

        # Header 
        useless, \
        self.Header.TransactionID, \
        Flags, \
        self.Header.QuestionCnt, \
        self.Header.AnswerCnt, \
        self.Header.AuthorityRRCnt, \
        self.Header.AdditionalRRCnt = self.packetiterator.next("6H", 12)

        # Decode Flags
        self.Header.Response = (Flags & 0x8000) != 0
        self.Header.Opcode = (Flags & 0x7800)
        self.Header.AA = (Flags & 0x0400) != 0
        self.Header.Truncated = (Flags & 0x200) != 0
        self.Header.RecursionDesired = (Flags & 0x100) != 0
        self.Header.RA = (Flags & 0x80) != 0
        self.Header.Z = (Flags & 0x400) != 0
        self.Header.Non_authenticatedData = (Flags & 0x10) != 0
        self.Header.AD = (Flags & 0x20) != 0
        self.Header.RCode = Flags & 0xF
        
        if Config.VERBOSE:
            print(self.Header)

        # Get the domain name in the query
        """
        Since the length of the domain name is uncertain. The domain name is represented in linked manner:
        ------------------------------------------------------------------------
        | length | segment | length | segment | .... | length | segment | 0x00 |
        ------------------------------------------------------------------------
        The length is the length of the next segment
        """
        for i in range(0, self.Header.QuestionCnt):
            self.QueriesList.append(Query())
            query_len = 0

            domain_name_list = []
            segment_index = 0
            useless, next_len = self.packetiterator.next("B", 1)
            query_len += 1
            while next_len != 0:
                if Config.DEBUG:
                    print("in loop")
                domain_name_list.append("")

                useless, \
                domain_name_list[segment_index], next_len = self.packetiterator.next(str(next_len) + "s" + "B", (next_len+1))
                query_len += next_len + 1

                segment_index += 1

            self.QueriesList[i].QNAME = parse_domain_name_list(domain_name_list)

            # Get the type and class of the query.
            useless, \
            self.QueriesList[i].QTYPE, self.QueriesList[i].CLASS = self.packetiterator.next("HH", 4)      
            query_len += 4
            self.QueriesList[i].length = query_len

        if Config.VERBOSE:
            for i in range(0, self.Header.QuestionCnt):
                if Config.DEBUG:
                    print("in loop")
                print(self.QueriesList[i])

        # Only get the smallest ttl of all RRs
        RRsCNT = self.Header.AnswerCnt + self.Header.AuthorityRRCnt + self.Header.AdditionalRRCnt
        if Config.VERBOSE:
            print("Number of Resource Record:",RRsCNT)
        for i in range (0, RRsCNT):
            self.RRsList.append(RescourceRecord())
            rr_len = 0

            domain_name_list = []
            segment_index = 0
            useless, next_len = self.packetiterator.next("B", 1)
            rr_len += 1

            if(next_len >= 192): # the domain name is represented by a pointer
                useless, \
                pointer = self.packetiterator.next("B", 1)
                rr_len += 1
                self.RRsList[i].NAME = "pointer:" + str(pointer)
            else:
           
                while next_len != 0:
                    if Config.DEBUG:
                        print("in loop")
                    domain_name_list.append("")

                    useless, domain_name_list[segment_index], next_len = self.packetiterator.next(str(next_len) + "s" + "B", (next_len+1))
                    rr_len += next_len + 1

                    segment_index += 1

                self.RRsList[i].NAME = parse_domain_name_list(domain_name_list)

            useless, \
            self.RRsList[i].TYPE,\
            self.RRsList[i].CLASS, \
            self.RRsList[i].TTL,\
            self.RRsList[i].RDLENGTH = self.packetiterator.next("HHIH", 10)
            rr_len += 10

            useless, \
            self.RRsList[i].RDATA = self.packetiterator.next(str(self.RRsList[i].RDLENGTH) + "s", self.RRsList[i].RDLENGTH)
            rr_len += self.RRsList[i].RDLENGTH

            self.RRsList[i].length = rr_len

            # Get the smallest TTL
            if(self.RRsList[i].TTL > 0 and self.minTTL > self.RRsList[i].TTL):
                self.minTTL = self.RRsList[i].TTL

        if Config.VERBOSE:
            for i in range(0, RRsCNT):
                if Config.DEBUG:
                    print("in loop")
                print(self.RRsList[i])
