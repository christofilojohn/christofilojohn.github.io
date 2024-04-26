# Cython magic:
from FL_cpp_server import py_fl_server, PyServerBuffer, PyBufferManager
import hashlib
import datetime
import os, sys, dill, argparse
import numpy as np

# Common helper methods for server and client
from helper import *

import threading
import queue
import dill
import time

# Number of clients variable
numberOfClients = 0
# Initialize buffers, aggregationDatabuffer has the data to send to a client,
aggregationDatabuffer = PyBufferManager()
# clientDataBuffers is a manager object that handles one buffer for each client
clientDataBuffers = PyBufferManager()
# TODO Keep performance of clients as vector
prevScore = None
newScore = None
stop_rounds = False
# Performance threshold to stop aggregation rounds
thr = 0.0055
# Public Keys of Clients
client_keys = None
symmetric_keys = None
server_public_key = None
server_private_key = None


def read_params(max_id, readKeys=False):
    """ Logic similar to tutorial code """
    # Get access to client buffers
    global clientDataBuffers
    # Init parameters
    params = []
    for mid in range(max_id):
        # Check if buffer data writing is complete, else wait for it to finish
        while not clientDataBuffers.check_buffer_complete(mid):
            time.sleep(0.1)
        clientBufferIO = BytesIO()
        buffSize = clientDataBuffers.get_buffer_size(mid)
        # print(f"Client {mid} buffer size: {buffSize}.")
        clientBufferIO.write(clientDataBuffers.get_buffer(mid, buffSize))
        # Reset the BytesIO pointer
        clientBufferIO.seek(0)
        if not readKeys:
            # Decrypt data
            eBytes = clientBufferIO.getvalue()
            dBytes = receive_and_decrypt(eBytes, symmetric_keys[mid])
            dBytesIO = BytesIO(dBytes)
            params.append(dill.load(dBytesIO))
        else:
            params.append(dill.load(clientBufferIO))
    return params

def aggregate_model(max_id, params):
    # Get access to aggregation buffer
    global aggregationDatabuffer, clientDataBuffers, newScore, prevScore, stop_rounds, numberOfClients
    # Reset the aggregation data buffer before writing
    aggregationDatabuffer.clear_all_buffers()

    """ Aggregate model - Algorithm """
    theta_total = sum([params[i]["theta"] for i in range(len(params))]) / len(params)
    var_total = sum([params[i]["var"] for i in range(len(params))]) / len(params)
    #  Calculate average score
    newScore = sum([params[i]["var_perf"] for i in range(numberOfClients)]) / (numberOfClients+1)
    print("Average score: " + str(newScore))

    """ Make decision whether to stop or not"""
    # Check whether the process should continue
    stop_rounds = checkScoreDiff(thr)
    # Set previous score as current, for the next comparison
    prevScore = newScore

    """ Dump Aggregated Model"""
    params = {"theta": theta_total, "var": var_total, "var_perf": float(stop_rounds)}

    # print(params["stop_rounds"])
    print("Decision to stop:" + str(stop_rounds))
    aggregatedBytes = dill.dumps(params)
    tempByteIO = BytesIO(aggregatedBytes)
    print("Aggregated buffer MD5: " + get_md5_checksum_from_bytesio(tempByteIO))
    tempByteIO.seek(0)
    for mid in range(max_id):
        # Encrypt using client's public key
        # https://www.preveil.com/blog/public-and-private-key/
        eBytes = encrypt_and_prepare(aggregatedBytes, symmetric_keys[mid])
        aggregationDatabuffer.set_buffer(mid, eBytes)
        aggregationDatabuffer.set_md5(mid, get_md5_checksum_from_bytesio(tempByteIO).encode())
    print(f"Size of params in bytes: {tempByteIO.getbuffer().nbytes}")

def send_public_key(max_id, public_key):
    # Get access to aggregation buffer
    global aggregationDatabuffer, clientDataBuffers, newScore, prevScore, stop_rounds, numberOfClients
    # Reset the aggregation data buffer before writing
    aggregationDatabuffer.clear_all_buffers()
    params = {"key": public_key}
    aggregatedBytes = dill.dumps(params)
    tempByteIO = BytesIO(aggregatedBytes)
    print("Key buffer MD5: " + get_md5_checksum_from_bytesio(tempByteIO))
    tempByteIO.seek(0)
    for mid in range(max_id):
        aggregationDatabuffer.set_buffer(mid, aggregatedBytes)
        aggregationDatabuffer.set_md5(mid, get_md5_checksum_from_bytesio(tempByteIO).encode())
    print(f"Size of key in bytes: {tempByteIO.getbuffer().nbytes}")

def send_symmetric_keys(max_id):
    global aggregationDatabuffer, clientDataBuffers, newScore, prevScore, stop_rounds, numberOfClients, symmetric_keys
    # Reset the aggregation data buffer before writing
    aggregationDatabuffer.clear_all_buffers()
    for mid in range(max_id):
        # params = {"key": symmetric_keys[mid]}
        # aggregatedBytes = dill.dumps(params)
        # Encrypt the symmetric key
        eBytes = encrypt_message_rsa(symmetric_keys[mid], client_keys[mid])

        aggregationDatabuffer.set_buffer(mid, eBytes)
        # aggregationDatabuffer.set_md5(mid, get_md5_checksum_from_bytesio(tempByteIO).encode())
        # print("Key buffer MD5: " + get_md5_checksum_from_bytesio(tempByteIO))
        # tempByteIO.seek(0)

def checkScoreDiff(threshold):
    global newScore, prevScore
    if newScore is None or prevScore is None:
        return False
    else:
        return abs(newScore - prevScore) < threshold


def main(portnum=8080, numOfClients=3, numOfIterations=4):
    global numberOfClients, clientBuffs, PyServerBufferManager, prevScore, newScore, stop_rounds, client_keys, server_public_key, server_private_key, symmetric_keys
    numberOfClients = numOfClients
    print("Starting server at:", datetime.datetime.now().strftime("%H:%M:%S"))
    # Initialize server object with given parameters
    server = py_fl_server(portnum, (numOfClients - 1), aggregationDatabuffer, clientDataBuffers)

    # Start server listening thread
    server.run()

    # Encryption:
    # 1. Public key exchange:
    # Generate RSA keys
    server_private_key, server_public_key = generate_rsa_keys()
    # Receive client key/secret in params
    client_keys_dict = read_params(numOfClients, True)
    client_keys = [entry['key'] for entry in client_keys_dict]
    # Send key/secret to client as aggregated data
    send_public_key(numOfClients, server_public_key)
    # Clear key buffers, in order to reuse on next iteration
    clientDataBuffers.clear_all_buffers()
    server.aggregationDone(False)

    # for mid in range(numberOfClients):
    #     print(client_keys[mid])

    # 2. Generate and send encrypted symmetric keys:
    # Dummy receive
    for mid in range(numberOfClients):
        while not clientDataBuffers.check_buffer_complete(mid):
            time.sleep(0.1)

    symmetric_keys = [generate_aes_key() for _ in range(numberOfClients)]
    # Send key/secret to client as aggregated data
    send_symmetric_keys(numOfClients)
    # Clear key buffers, in order to reuse on next iteration
    clientDataBuffers.clear_all_buffers()
    server.aggregationDone(False)

    # Loop the process if stop_rounds is False
    while not stop_rounds:
        # Read buffers to get params
        params = read_params(numOfClients)
        # Aggregate the given parameters
        aggregate_model(numOfClients, params)
        # Clear input parameter buffers, in order to reuse on next iteration
        clientDataBuffers.clear_all_buffers()
        # Notify the handler threads that the aggregated data is ready to be sent to the client
        server.aggregationDone(stop_rounds)
    # Wait for all the processes to complete and then terminate
    server.allDone()


if __name__ == "__main__":
    """ Valavanis - Argparser to take machine id from terminal params """
    parser = argparse.ArgumentParser(description="Give model parameters.")
    parser.add_argument('--p', type=int, help='Port number')
    parser.add_argument('--c', type=int, help='Number of Clients')
    parser.add_argument('--i', type=int, help='Number of Iterations')
    args = parser.parse_args()
    # Run main function with given args
    main(args.p, args.c, args.i)
