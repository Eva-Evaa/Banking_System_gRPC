import grpc
import banking_pb2
import banking_pb2_grpc
import time
from banking_pb2 import BankingRequest
from time import sleep
class Customer:
    def __init__(self, id, events):
        # unique ID of the Customer
        self.id = id
        # events from the input
        self.events = events
        # a list of received messages used for debugging purpose
        self.recvMsg = list()
        # pointer for the stub
        self.stub = None
        # writeset for customer 
        self.writeset = list()

    def createStub(self):
        self.stub = banking_pb2_grpc.BranchStub(grpc.insecure_channel("localhost:" + str(50000 + self.id)))
        


    def executeEvents(self):
        for event in self.events:

#Change to the corresponding branch
            self.stub = banking_pb2_grpc.BranchStub(grpc.insecure_channel("localhost:" + str(50000 + event["dest"])))

#If the request is query, needs to wait 3s so that all the information is propagated
            if event["interface"] == "query":
                sleep(3)

            money=0
            if event["interface"] != "query":
                money=event["money"]
            else: 
                money=0
#Request to the branch

            reply=self.stub.MsgDelivery(BankingRequest( interface=event["interface"], money=money,writeset=self.writeset))
            

#Add message according to the reply
            self.recvMsg.append({"interface": reply.interface, "dest": event["dest"], "money": reply.money})

            if event["interface"] != "query":
                self.writeset = reply.writeset
            sleep(0.3)




