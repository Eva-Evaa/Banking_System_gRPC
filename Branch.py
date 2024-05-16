from concurrent import futures
import grpc
import banking_pb2
import banking_pb2_grpc
from time import sleep
from banking_pb2 import BankingRequest, BankingReply
class Branch(banking_pb2_grpc.BranchServicer):

    def __init__(self, id, balance, branches):
        # unique ID of the Branch
        self.id = id
        # replica of the Branch's balance
        self.balance = balance
        # the list of process IDs of the branches
        self.branches = branches
        # the list of Client stubs to communicate with the branches
        self.stubList = list()
        # a list of received messages used for debugging purpose
        self.recvMsg = list()
        # iterate the processID of the branches
        self.test = list()
        #writeset for branch
        self.writeset = list()




#Create Stub here so that one branch is able to find other branches through stublist
    def createStub(self):
        branchesLen=len(self.branches)
        for i in range(branchesLen):
            curID=self.branches[i]
            if curID == self.id:
                continue

            self.stubList.append(banking_pb2_grpc.BranchStub(grpc.insecure_channel("localhost:"+str(50000+curID))))

#Depends on the type of interface, MsgDelivery will call different functions and reply message
    def MsgDelivery(self,request, context):

        
            
        if(request.interface=="query"):
            return self.Query()
        elif(request.interface=="deposit"):
            return self.Deposit(request)
        elif(request.interface=="withdraw"):
            return self.Withdraw(request)
        else:
            msg = {"interface": request.interface, "result": "fail"}
            self.recvMsg.append(msg)
            return BankingReply(interface=request.interface, result="fail", money=self.balance)


#When the request is deposit, the branch needs to proprgate the information to other branches
    def Propogate_Deposit (self,request):
        for stub in self.stubList:
            stub.MsgUpdate(BankingRequest(interface="deposit", money=request.money, writeset=request.writeset))

#When the request is widthdraw, the branch needs to proprgate the information to other branches
    def Propogate_Withdraw(self, request):
        for stub in self.stubList:
            stub.MsgUpdate(BankingRequest(interface="withdraw", money=request.money, writeset=request.writeset))


#reply to the customer the balance information
    def Query(self):
        msg = {"interface": "query", "result": "success", "money": self.balance}
        self.recvMsg.append(msg)
        return BankingReply(interface="query", result="success", money=self.balance)

#change the balance according to the request
    def Withdraw(self,request):
#Determine whether all the element in request exist in self

        while True:
            temp=True
            for entry in request.writeset:
                if entry not in self.writeset:
                    temp=False
            if(temp):
                break
        
        result="suceess"
        if self.balance >= request.money:
            self.balance -= request.money

            #update writeset
            cueLen = len(self.writeset) + 1
            self.writeset.append(cueLen)

            #update money information to other branches
            self.Propogate_Withdraw(request)

#If the requested money is more than balance, the money can not be withdrawed
        else:
            print("fail")
            result="fail"

        msg = {"interface": "withdraw", "result": result}
        self.recvMsg.append(msg)

        
        return BankingReply(interface="withdraw", result=result, money=0)

#Change the balance by deposit
    def Deposit(self,request):
#Determine whether all the element in request exist in self
        while True:
            for entry in request.writeset:
                if entry not in self.writeset:
                    continue
            break
    
        result="suceess"
        self.balance += request.money

        #update writeset
        cueLen = len(self.writeset) + 1
        self.writeset.append(cueLen)

        #update money information to other branches
        self.Propogate_Deposit (request)
        msg = {"interface": "deposit", "result": "success"}
        self.recvMsg.append(msg)
        return BankingReply(interface="deposit", result=result, money=0)   

#Update with other branches and reply message
    def MsgUpdate(self,request,context):

#Determine whether all the element in request exist in self
        while True:
            temp=True
            for entry in request.writeset:
                if entry not in self.writeset:
                    temp=False
            if(temp):
                break
            
        if(request.interface=="deposit"):
            self.balance+=request.money
        elif(request.interface=="withdraw"):
            self.balance-=request.money

        #update writeset
        cueLen = len(self.writeset) + 1
        self.writeset.append(cueLen)

        msg = {"interface": request.interface, "result": "success"}

        self.recvMsg.append(msg)
        return BankingReply(interface=request.interface, result="success", money=self.balance)


