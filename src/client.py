# Cython magic:
import time
from io import BytesIO
# Cython imports to use C++ infrastructure
from FL_cpp_client import py_fl_client, PyClientBuffer
# Machine Learning client imports
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score
from joblib import dump, load

# Common helper methods for server and client
from helper import *

# Data subfolder
DATA_PATH = "./data/"
model = GaussianNB()
mid = -1
# Initialize data buffers
aggregationBuffer = PyClientBuffer()
paramsBuffer = PyClientBuffer()
# Aggregation round global variable
aggregationRound = 0
stop_rounds = False
# https://www.ibm.com/docs/en/zos/2.5.0?topic=pdk-using-rsa-public-keys-protect-keys-sent-between-systems
# Encryption keys placeholders
client_private_key = None
client_public_key = None
server_public_key = None
symmetric_key = None

def load_data(dataset_id='default'):
    # global X_train, X_eval, X_test, y_train,  y_eval, y_test
    """ Load data csv file """
    df = pd.read_csv(f"{DATA_PATH}data_portion_{mid}.csv", header=0)
    y = df['target'].copy()
    df.drop(['target'], axis=1, inplace=True)
    """ Training, Evaluation, Test split """
    # stratify maintains the distibutions
    X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=0.2, shuffle=True, stratify=y)
    return X_train, X_test, y_train, y_test


def train_model(x, y):
    global paramsBuffer, model, mid
    model.fit(x, y)
    # parameters = gnb.get_params()
    f1 = model.score(x, y)
    print(f"Client: {mid} completed initial training...")
    return f1


def readParams(readKeys=False):
    """ Get new params from the buffer """
    global aggregationBuffer, paramsBuffer
    while not aggregationBuffer.check_complete():
        print("waiting for new params...")
        time.sleep(0.1)
    # Create BytesIO object
    clientBufferIO = BytesIO()
    # Get buffer size for read and write read data to BytesIO object
    buffSize = aggregationBuffer.size()
    clientBufferIO.write(aggregationBuffer.read(buffSize))
    # Reset the BytesIO pointer
    aBuffMD5 = get_md5_checksum_from_bytesio(clientBufferIO)
    print("MD5: " + aBuffMD5)
    # Testing
    clientBufferIO.seek(0)
    if not readKeys:
        # Decrypt data
        eBytes = clientBufferIO.getvalue()
        dBytes = receive_and_decrypt(eBytes, symmetric_key)
        dBytesIO = BytesIO(dBytes)

        # Load the serialized data to memory
        params = dill.load(dBytesIO)
    else:
        # Load the serialized data to memory
        params = dill.load(clientBufferIO)
    return params

def readSymmetricKeys():
    global aggregationBuffer, paramsBuffer
    while not aggregationBuffer.check_complete():
        time.sleep(0.1)
    # Create BytesIO object
    clientBufferIO = BytesIO()
    # Get buffer size for read and write read data to BytesIO object
    buffSize = aggregationBuffer.size()
    clientBufferIO.write(aggregationBuffer.read(buffSize))
    # Reset the BytesIO pointer
    aBuffMD5 = get_md5_checksum_from_bytesio(clientBufferIO)
    print("MD5: " + aBuffMD5)
    # Testing
    clientBufferIO.seek(0)
    eBytes = clientBufferIO.getvalue()
    return eBytes

def readServerPublicKey():
    global aggregationBuffer, paramsBuffer
    while not aggregationBuffer.check_complete():
        print("waiting for new params...")
        time.sleep(0.1)
    # Create BytesIO object
    clientBufferIO = BytesIO()
    # Get buffer size for read and write read data to BytesIO object
    buffSize = aggregationBuffer.size()
    clientBufferIO.write(aggregationBuffer.read(buffSize))
    # Reset the BytesIO pointer
    aBuffMD5 = get_md5_checksum_from_bytesio(clientBufferIO)
    print("MD5: " + aBuffMD5)
    # Testing
    clientBufferIO.seek(0)
    # Load the serialized data to memory
    params = dill.load(clientBufferIO)
    return params

def updateModel(params, X_train, X_test, y_train, y_test):
    """ Update model """
    global aggregationBuffer, model, stop_rounds
    """ Initially get only the theta and var. parameters """
    model.theta_ = params["theta"]
    model.var_ = params["var"]
    # Get message to stop from val_perf variable (reused for efficiency and symmetry)
    stop_rounds = True if params["var_perf"] == 1.0 else False
    print("Decision to stop: " + str(stop_rounds))
    # Update model using new params and same training set
    model.partial_fit(X_train, y_train)
    # Get new performance after partial fit
    f1 = getModelPerformance(X_test, y_test)
    return f1


def writeParamsBuffer(score):
    """ Write new params to the buffer """
    global paramsBuffer, model, symmetric_key
    # Setup params dictionary
    params = {"theta": model.theta_, "var": model.var_, "var_perf": score}
    pBytes: bytes = dill.dumps(params)
    tempByteIO: BytesIO = BytesIO(pBytes)
    print(f"Size of params in bytes: {tempByteIO.getbuffer().nbytes}")
    pBuffMD5 = get_md5_checksum_from_bytesio(tempByteIO)
    print("MD5: " + pBuffMD5)
    tempByteIO.seek(0)
    # print(server_public_key)
    eBytes = encrypt_and_prepare(pBytes, symmetric_key)
    # Write new params to buffer, update MD5, set writing as complete
    paramsBuffer.write(eBytes)
    paramsBuffer.set_md5(pBuffMD5.encode())
    paramsBuffer.set_complete()

def writeKeyToBuffer(key, dummy=False):
    """ Write new params to the buffer """
    global paramsBuffer
    # Send key:
    # Write key to buffer, update MD5, set writing as complete
    if dummy:
        dummyBytes = b'1234'
        paramsBuffer.write(dummyBytes)
        paramsBuffer.set_md5(b'75be2fbcb73cbf391d8bbbdce2ab47c9')
    else:
        # Setup params dictionary
        params = {"key": key}
        pBytes: bytes = dill.dumps(params)
        tempByteIO: BytesIO = BytesIO(pBytes)
        print(f"Size of key in bytes: {tempByteIO.getbuffer().nbytes}")
        pBuffMD5 = get_md5_checksum_from_bytesio(tempByteIO)
        print("Key MD5: " + pBuffMD5)
        tempByteIO.seek(0)
        paramsBuffer.write(pBytes)
        paramsBuffer.set_md5(pBuffMD5.encode())
    paramsBuffer.set_complete()


def getModelPerformance(X_test, y_test):
    """ Valavanis - Evaluate Model"""
    global aggregationRound
    y_pred = model.predict(X_test)
    """
    Evaluate the model performance over the testing set (f1, prec. recall, ...)
    """
    # Calculate precision, recall, and F1 score
    # precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')
    # conf_matrix = confusion_matrix(y_test, y_pred)

    # roc_auc = roc_auc_score(y_test, y_pred)
    # Print results
    # print(f"-Precision: {precision:.2f}")
    print(f"-Recall: {recall}")
    print(f"-F1 Score: {f1}")
    # print(f"-Roc-auc Score: {roc_auc:.2f}")
    # Selected f1 as param to send to server
    return f1


def main(ip_address="127.0.0.1", portnum=8080):
    global mid, aggregationRound, stop_rounds, client_private_key, client_public_key, server_public_key, symmetric_key
    # Init client, with IP, portnum and Cython buffers as parameters
    client = py_fl_client(ip_address, portnum, paramsBuffer, aggregationBuffer)
    mid = client.getMachineID()
    # Generate RSA keys
    client_private_key, client_public_key = generate_rsa_keys()
    X_train, X_test, y_train, y_test = load_data()
    f1 = train_model(X_train, y_train)

    # Participate in Federated Learning using separate C++ thread
    client.participate()
    # Keep rounds
    aggregationRound = 1

    # Encrypt data:
    # Generate RSA keys
    client_private_key, client_public_key = generate_rsa_keys()

    # 1. Share public key:
    # Write public key to paramsBuffer
    writeKeyToBuffer(client_public_key)
    # Notify C++ that the params are ready
    client.setParamsReady(False)
    # Get server public key from params
    server_public_key = readParams(True)["key"]
    # Parameters read
    aggregationBuffer.clear()

    # 2. Share encrypted symmetric key:
    # Write encrypted symmetric key to paramsBuffer
    writeKeyToBuffer(b'1', dummy=True)
    # Notify C++ that the params are ready
    client.setParamsReady(False)
    encrypted_symmetric_key = readSymmetricKeys()
    # Get server public key from params
    symmetric_key = decrypt_message_rsa(encrypted_symmetric_key, client_private_key)
    # Parameters read
    aggregationBuffer.clear()

    print("Performance metrics on beginning.")
    getModelPerformance(X_test, y_test)

    # Loop the process
    while not stop_rounds:
        # Write new params to paramsBuffer
        writeParamsBuffer(f1)
        # Notify C++ that the params are ready
        client.setParamsReady(stop_rounds)
        # Get new params from the aggregation buffer and wait if they are not ready
        params = readParams()
        print("Round " + str(aggregationRound) + ": Decision to stop loop:" + str(stop_rounds))
        # Parameters read, no need to keep buffer
        aggregationBuffer.clear()
        # Partially fit the aggregated parameters
        f1 = updateModel(params, X_train, X_test, y_train, y_test)
        # Increase aggregation rounds
        aggregationRound += 1
    # Get final performance and save model
    # print("Model performance after FL:")
    # getModelPerformance(X_test, y_test)
    # Store model to disk
    dump(model, f'{DATA_PATH}/model_{mid}')
    print("Final model saved to disk...")
    return 0


if __name__ == "__main__":
    """ Valavanis - Argparser to take machine id from terminal params """
    import argparse
    parser = argparse.ArgumentParser(description="Specify parameters.")
    # parser.add_argument('--id', type=int, help='Machine ID')
    parser.add_argument('--ip', type=str, help='IP Address')
    parser.add_argument('--p', type=int, help='Port number')
    parser.add_argument('--d', type=str, default='default', help='Dataset ID to use')
    args = parser.parse_args()
    main(args.ip, args.p)
