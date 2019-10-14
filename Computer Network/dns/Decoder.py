import struct

# This is a tool function to assemble the each part of the domain name in a list
# and return a domain name string
def parse_domain_name_list(domain_name_list):
    domain_name = ""
    for i in range(0, len(domain_name_list)):
        domain_name += str(domain_name_list[i].decode())
        if(i != len(domain_name_list) - 1):
            domain_name += "."
    return domain_name

# The instance of this class is to help decode the DNS message.
class DNSMessage:
    
    def __init__(self):
        self.struct_format = ">6H1B"
        self.Struct = struct.Struct(self.struct_format)
        self.HeaderDict = {}
        self.QueriesDict = {}
        self.AnswerDict = {}
        self.AdditionalRecordsDict = {}

    def __str__(self):
        return "HeaderDict:{}\r\nQueriesDict:{}\r\nAnswerDict:{}\r\n".format(str(self.HeaderDict), str(self.QueriesDict), str(self.AnswerDict))

    # This is a tool function to replace the transaction ID of the answer
    # from the upper level DNS server before forwarding the answer to
    # the query process (client)
    def changeTransactionID(self, data, newID):
        data_length = len(data)
        self.struct_format = ">H" + str(data_length - 2) + "s"
        self.Struct = struct.Struct(self.struct_format)

        oldID, restPart = self.Struct.unpack_from(data)

        return struct.pack(self.struct_format, newID, restPart)

    # This method can parse the query dns message or the answer dns message from 
    # the upper level server to some dictionary:
    # 1. HeaderDict  : contains all the information of the DNS message header
    # 2. QueriesDict : contains the domain name, class and type of the query
    # 3. AnswerDict  : contains the name, type, class and time-to-live of the answer
    #                  from the upper level DNS server.
    def parse_dns(self, data):
        self.struct_format = ">6H1B"
        self.Struct = struct.Struct(self.struct_format)

        self.HeaderDict["TransactionID"], \
        Flags, \
        self.HeaderDict["QuestionCnt"], \
        self.HeaderDict["AnswerRRCnt"], \
        self.HeaderDict["AuthorityRRCnt"], \
        self.HeaderDict["AdditionalRRCnt"], \
        next_len = self.Struct.unpack_from(data)

        # Decode Flags
        self.HeaderDict["Response"] = (Flags & 0x8000) != 0
        self.HeaderDict["OpCode"] = (Flags & 0x7800)
        self.HeaderDict["AA"] = (Flags & 0x0400) != 0
        self.HeaderDict["Truncated"] = (Flags & 0x200) != 0
        self.HeaderDict["RecursionDesired"] = (Flags & 0x100) != 0
        self.HeaderDict["RA"] = (Flags & 0x80) != 0
        self.HeaderDict["Z"] = (Flags & 0x400) != 0
        self.HeaderDict["Non_authenticatedData"] = (Flags & 0x10) != 0
        self.HeaderDict["ADBit"] = (Flags & 0x20) != 0
        self.HeaderDict["RCode"] = Flags & 0xF

        # Get the domain name in the query
        """
        Since the length of the domain name is uncertain. The domain name is represented in linked manner:

        ------------------------------------------------------------------------
        | length | segment | length | segment | .... | length | segment | 0x00 |
        ------------------------------------------------------------------------

        The length is the length of the next segment
        """
        domain_name_list = []
        segment_index = 0
        useless_len = 13
        while next_len != 0:
            domain_name_list.append("")
            self.struct_format = ">"+ str(useless_len) +"s" + str(next_len) + "s" + "1B"
            useless_len += next_len + 1
            self.Struct = struct.Struct(self.struct_format)

            useless, domain_name_list[segment_index], next_len = self.Struct.unpack_from(data)

            segment_index += 1
        
        self.QueriesDict["domain_name"] = parse_domain_name_list(domain_name_list)

        # Get the type and class of the query.
        self.struct_format = ">"+ str(useless_len) +"s" + "HH"
        self.Struct = struct.Struct(self.struct_format)

        useless, \
        self.QueriesDict["Type"], self.QueriesDict["Class"]  = self.Struct.unpack_from(data)

        # Only get the first answer or authority record
        if self.HeaderDict["AnswerRRCnt"] > 0 or self.HeaderDict["AuthorityRRCnt"] > 0: # Get the first answer
            useless_len += 4
            self.struct_format = ">"+ str(useless_len) +"s" + "HHHI"
            self.Struct = struct.Struct(self.struct_format)

            useless, self.AnswerDict["Name"], self.AnswerDict["Type"],\
            self.AnswerDict["Class"], self.AnswerDict["Time_to_live"] = self.Struct.unpack_from(data)

        # Decode the Additional Record Part (Disgard since the we don't need it for this homework)

        # self.struct_format = ">"+ str(useless_len) +"s" + "HHBHHBBHH"
        # self.Struct = struct.Struct(self.struct_format)

        # useless, \
        # self.QueriesDict["Type"], self.QueriesDict["Class"], \
        # self.AdditionalRecordsDict["Name"], \
        # self.AdditionalRecordsDict["Type"], \
        # self.AdditionalRecordsDict["UDP_payload_size"],\
        # self.AdditionalRecordsDict["Higher_bits_in_extended_RCODE"],\
        # self.AdditionalRecordsDict["EDNS0_version"], \
        # self.AdditionalRecordsDict["Z"],\
        # self.AdditionalRecordsDict["Data_Length"] = self.Struct.unpack_from(data)

        # useless_len += 15
        # self.struct_format = ">"+ str(useless_len) +"s" + "HH"
        # self.Struct = struct.Struct(self.struct_format)

        # useless, self.AdditionalRecordsDict["Option_Code"],\
        # self.AdditionalRecordsDict["Option_length"] = self.Struct.unpack_from(data)

        # useless_len += 4
        # self.struct_format = ">"+ str(useless_len) +"s" + str(self.AdditionalRecordsDict["Option_length"]) + "s"
        # self.Struct = struct.Struct(self.struct_format)

        # useless, self.AdditionalRecordsDict["Option_data"] = self.Struct.unpack_from(data)
