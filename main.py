import grpc
import banking_pb2
import banking_pb2_grpc
import json
import multiprocessing
from concurrent import futures
from Branch import Branch
from Customer import Customer
from time import sleep
import os



def BrunchFunc(branch):

    branch.createStub()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=20))
#Create server
    banking_pb2_grpc.add_BranchServicer_to_server(branch, server)
#Create unique port to communite
    server.add_insecure_port("[::]:" + str(50000 + branch.id))
    server.start()

    server.wait_for_termination()



def CustomerFunc(customer, outputsFile):

    customer.createStub()

#Customer execute events
    customer.executeEvents()

#Get result and write
    res=[]
    temp={"id": customer.id, "balance": customer.recvMsg[-1]["money"]}
    res.append(temp)


    output_file = open(outputsFile, "a")
    output_file.write(json.dumps(res, indent=4))
    
    print(str(res))




if __name__ == "__main__":

    
    if(os.path.exists("./read_your_writtes_out.json")):
        os.remove("read_your_writtes_out.json")


    branchIds = []
    processesBranch=[]
    processesCustomer=[]

#read-your-writes
    print("Start read your writes process and output is")
    branchIds = []
    processesBranch=[]
    processesCustomer=[]
    #inputs = json.load(open("read_your_writes.json"))
    inputs = json.load(open("testInput.json"))
    outputs="./read_your_writtes_out.json"
    for event in inputs:
        if not event["type"] == "customer":
            branchIds.append(event["id"])

    for event in inputs:
        if not event["type"] == "customer":

            #Create branch according to branch ids and pass it to BrunchFunc to start branch server
            branch_process = multiprocessing.Process(target=BrunchFunc, args=(Branch(event["id"], event["balance"], branchIds),))
            processesBranch.append(branch_process)
            branch_process.start()
    for event in inputs:
        if event["type"] == "customer":
            #Create customer and pass it to CustomerFunc to execute customer events

            customer_process = multiprocessing.Process(target=CustomerFunc, args=(Customer(event["id"], event["events"]),outputs))
            
            processesCustomer.append(customer_process)
            customer_process.start()
    sleep(7)
    for process in processesBranch:
        process.terminate()
    for process in processesCustomer:
        process.terminate()






