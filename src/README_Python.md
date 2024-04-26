# Server:

### Modules and Libraries

- **Standard Libraries:** `hashlib`, `datetime`, `os`, `sys` for utility functions; `threading`, `queue` for concurrent operations; `dill` for object serialization; `argparse` for command-line argument parsing.
- **Cython Imports:** `FL_cpp_server.py_fl_server`, `PyServerBuffer`, `PyBufferManager` to handle server functionalities and buffer management.
- **Numerical Operations:** `numpy` for numerical computations.
- **Utility Scripts:** `helper` contains utility functions for cryptographic operations and data handling.

### Constants

- None explicitly defined, but server settings such as port numbers and number of clients are configured through command-line arguments or function parameters.

### Global Variables

- **Buffer Management:** Handles data sent to and from clients.
- **Security Keys:** Public and private keys for RSA, and symmetric keys for AES encryption.
- **Performance Tracking:** Variables to track scores from clients to determine the convergence of the learning process.

### Main Functions

- **`read_params`**:
    - Retrieves and decrypts parameters sent by clients.
    - Can optionally read encryption keys if specified.
- **`aggregate_model`**:
    - Aggregates parameters received from multiple clients.
    - Calculates the new average performance and determines if the learning process should continue based on a threshold comparison.
- **`send_public_key`** and **`send_symmetric_keys`**:
    - Distributes the server's public key and symmetric keys to clients, ensuring subsequent communications are encrypted.
- **`checkScoreDiff`**:
    - Compares the difference between current and previous performance scores to decide if further iterations are needed.

### Workflow Functions

- **`main`**:
    - Initializes and configures the server.
    - Manages the key exchange and data aggregation in a loop until the performance criterion stops the rounds or the maximum number of iterations is reached.

### Command-Line Interface (CLI)

- Configures the server through command-line arguments such as port number, number of clients, and number of iterations.

# 

* * *

Client:

### Modules and Libraries

- **Standard Libraries:** `time`, `io.BytesIO` for stream operations.
- **Cython Imports:** `FL_cpp_client.py_fl_client`, `PyClientBuffer` for handling low-level operations and buffer management with Cython.
- **Machine Learning Libraries:** `sklearn` for model training and evaluation, `joblib` for model serialization.
- **Utility Scripts:** `helper` contains utility functions for operations like checksum calculation and encryption.

### Constants

- `DATA_PATH`: Path to the dataset directory.

### Global Variables

- Model instance and training data variables.
- Buffers for managing data aggregation and parameter sharing.
- Keys for encryption and decryption.
- Control variables for the learning rounds.

### Main Functions

- **`load_data`**:
    - Loads data from a CSV file.
    - Splits the data into training and test datasets.
- **`train_model`**:
    - Trains the Gaussian Naive Bayes model on the provided dataset.
    - Returns the training score (F1 score).
- **`readParams`** and **`readSymmetricKeys`**:
    - Reads and decrypts parameters from the aggregation buffer.
    - Handles secure transmission of symmetric keys and parameters.
- **`updateModel`**:
    - Updates the model parameters from the received values and recalculates its performance.
- **`writeParamsBuffer`** and **`writeKeyToBuffer`**:
    - Serializes and writes new parameters or keys to the buffer.
- **`getModelPerformance`**:
    - Evaluates the model's performance on the test set using metrics like recall and F1 score.
- **`main`**:
    - Initializes the client with server connection details.
    - Manages the flow of model training, key exchange, and parameter updates in a federated learning cycle.
- **CLI Handling**:
    - Parses command-line arguments for IP address, port number, and dataset ID.

# 

* * *

Helper:

### Modules and Libraries

- **Standard Libraries:** `hashlib`, `datetime`, `os`, `sys`, `time` for general programming utilities; `threading` for multithreaded operations; `io.BytesIO` for in-memory binary streams; `base64` for encoding binary data.
- **Data Handling Libraries:** `numpy` and `pandas` for data manipulation.
- **Cryptography Libraries:** `cryptography.hazmat` for cryptographic functions including RSA and AES encryption/decryption, key generation, and serialization.

### Helper Functions

- **`get_md5_checksum`**:
    - Computes the MD5 checksum for the contents of a specified file.
- **`get_md5_checksum_from_bytesio`**:
    - Calculates the MD5 checksum for data stored in a `BytesIO` object, ensuring data integrity.
- **`parse_header`**:
    - Extracts and decodes metadata from a received header, typically used to store and verify data transmission details such as MD5 checksums and machine identifiers.
- **`generate_rsa_keys`**:
    - Generates a pair of RSA private and public keys used for asymmetric encryption, with best practices for key size and public exponent.
- **`generate_aes_key`**:
    - Creates a 256-bit symmetric key for AES encryption, providing strong security for data encryption.
- **`encrypt_message_rsa`** and **`decrypt_message_rsa`**:
    - Encrypts and decrypts messages using RSA public and private keys respectively, employing OAEP padding and SHA-256 for enhanced security.
- **`encrypt_and_prepare`** and **`receive_and_decrypt`**:
    - Functions for AES encryption and decryption that handle initialization vector (IV) generation, data padding, and base64 encoding/decoding to facilitate secure data storage and transmission.