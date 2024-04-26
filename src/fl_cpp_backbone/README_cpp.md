# FL Server-Client Module

## Net\_lib - Common Helper Methods and Constants

#### Constants:

- `const char* ackMessage = "ACK";`
    - **Description**: A predefined acknowledgment message used in server-client communication.

#### Methods:

##### `int stringToInt(const std::string& str)`

- **Purpose**: Parses an integer from a String
- **Parameters**:
    - `str`: Reference to the string

- **Returns**: The parsed integer

##### `std::string setupHeader(const std::string md5_checksum, int machine_id, int64_t file_size)`

- **Purpose**: Constructs a header string with MD5 checksum, machine ID, and file size.
- **Parameters**:
    - `md5_checksum`: The MD5 checksum of the file.
    - `machine_id`: The identifier for the machine.
    - `file_size`: The size of the file in bytes.
- **Returns**: A formatted header string.

##### `void parseHeader(const std::string& header, std::string& receivedMD5, std::string& machineID, int64_t& fileSize)`

- **Purpose**: Parses the header string into individual components.
- **Parameters**:
    - `header`: The received header string.
    - `receivedMD5`: Extracted MD5 checksum.
    - `machineID`: Extracted machine ID.
    - `fileSize`: Extracted file size.

##### `void printError(int sock, const std::string& errorMessage)`

- **Purpose**: Prints an error message and closes the socket.
- **Parameters**:
    - `sock`: The socket descriptor.
    - `errorMessage`: The error message to be printed.

##### `std::string sanitizeMID(const std::string& input)`

- **Purpose**: Removes newline characters from the machine ID.
- **Parameters**:
    - `input`: The machine ID string.
- **Returns**: The sanitized machine ID.

##### `int getFileSize(const std::string filename)`

- **Purpose**: Determines the size of a file.
- **Parameters**:
    - `filename`: The name of the file.
- **Returns**: The size of the file in bytes.

##### `void receiveFileSock(int socket, std::string filename, int64_t fileSize)`

- **Purpose**: Receives a file from a socket and writes it to disk.
- **Parameters**:
    - `socket`: The socket descriptor.
    - `filename`: The name of the file to write to.
    - `fileSize`: The expected size of the file.

##### `void sendFileSock(int socket, std::string filename, int64_t fileSize)`

- **Purpose**: Reads file from disk and sends it over a socket.
- **Parameters**:
    - `socket`: The socket descriptor.
    - `filename`: The name of the file to send.
    - `fileSize`: The size of the file.

##### `void sendBufferSock(int socket, char* dataBuffer, int64_t bufferSize)`

- **Purpose**: Sends data from a buffer over a socket.
- **Parameters**:
    - `socket`: The socket descriptor.
    - `dataBuffer`: The data buffer to send.
    - `bufferSize`: The size of the buffer.

##### `void receiveBufferSock(int socket, char* dataBuffer, int64_t bufferSize)`

- **Purpose**: Receives data from a socket into a buffer.
- **Parameters**:
    - `socket`: The socket descriptor.
    - `dataBuffer`: The buffer to store the received data.
    - `bufferSize`: The size of the buffer.

##### `std::string receiveHeaderSTR(int sock)`

- **Purpose**: Receives a header string from a socket.
- **Parameters**:
    - `sock`: The socket descriptor.
- **Returns**: The received header string.

  

## Shared Buffer ( Shared Buffer class in shared\_buffer.h, shared\_buffer.cpp )

#### Methods:

#### `void write(const char* data, size_t length)`

- **Purpose**: Appends data to the end of the internal buffer.
- **Parameters**:
    - `data`: Pointer to the data to be written.
    - `length`: The number of bytes to write.
- **Behavior**: Method to append `length` bytes from `data` to the buffer.

#### `void read(char* output, size_t length, size_t offset)`

- **Purpose**: Reads data from the buffer into the provided output array.
- **Parameters**:
    - `output`: Pointer to the output buffer where the data will be copied.
    - `length`: Number of bytes to read.
    - `offset`: Starting position in the buffer from where to begin reading.
- **Behavior**: Method to copy `length` bytes from the buffer to `output`, starting at `offset`. Prints an error if the read operation exceeds buffer bounds.

#### `size_t size() const`

- **Purpose**: Returns the current size of the buffer.
- **Returns**: The number of bytes currently stored in the buffer.
- **Behavior**: Method to obtain the buffer's size.

#### `char* getBufferPtr()`

- **Purpose**: Provides direct access to the internal buffer.
- **Returns**: A pointer to the beginning of the internal buffer.
- **Behavior**: Method to obtain a raw pointer to the buffer data.

#### `void clear()`

- **Purpose**: Clears the buffer, removing all data.
- **Behavior**: Method to erase all contents of the buffer, resetting its size to zero.

#### `void setComplete()`

- **Purpose**: Sets writing complete condition to true, signifying that the data is ready to be accessed
- **Behavior**: Method to set a bool flag to true

#### `void checkComplete()`

- **Purpose**: Checks writing complete condition to see if the data is ready to be accessed
- **Behavior**: Read a boolean

#### `void resetComplete()`

- **Purpose**: Resets writing complete condition to false, signifying that the buffer has not yet received the expected data
- **Behavior**: Method to set a bool flag to false

#### `void setMD5()`

- **Purpose**: Stores MD5 checksum of written data to a public variable
- **Behavior**: Method to set the MD5 checksum buffer variable

- **Parameters**:
    - `data`: The given md5 checksum

  

## Buffer Manager ( Buffer Manager class in shared\_buffer.h, shared\_buffer.cpp )

Manages SharedBuffer objects, used for server side data storage

#### Constructor: `BufferManager()`

- **Purpose**: Initializes a new instance of the `BufferManager` class.
- **Behavior**: Sets up the internal structures required to manage multiple `SharedBuffer` objects.

#### Methods:

#### `void createBuffers(int count)`

- **Purpose**: Allocates and initializes a specified number of `SharedBuffer` objects.
- **Parameters**:
    - `count`: The number of `SharedBuffer` instances to create.
- **Behavior**: Dynamically creates `count` instances of `SharedBuffer` and stores them for later access.

#### `SharedBuffer* getBuffer(int index)`

- **Purpose**: Retrieves a pointer to a `SharedBuffer` object at a specified index.
- **Parameters**:
    - `index`: The index of the buffer to retrieve.
- **Returns**: A pointer to the `SharedBuffer` object at the specified index, or `nullptr` if the index is out of bounds.
- **Behavior**: Provides access to a specific `SharedBuffer` managed by the `BufferManager`, ensuring thread safety during access.

#### `size_t size() const`

- **Purpose**: Returns the number of `SharedBuffer` objects managed by the `BufferManager`.
- **Returns**: The total count of `SharedBuffer` instances currently managed.
- **Behavior**: Allows querying the number of buffers currently available without modifying any internal state.

#### Destructor: `~BufferManager()`

- **Purpose**: Cleans up allocated resources upon the destruction of the `BufferManager` instance.
- **Behavior**: Iterates through all managed `SharedBuffer` objects, safely deletes them, and clears the internal container to prevent memory leaks.

  

## Barrier (class in barrier.h, barrier.cpp )

A class that emulates c++20 barrier for c++11, used in the server for thread synchronisation. Specifically, the barrier awaits for all the client connections (handleClient thread) to reach a specific point, in order to either start the aggregation, when all client data is received or reset the aggregation condition for the training loop to restart.

#### Constructor: `Barrier(std::size_t count, std::function<void()> completionFunction)`

- **Purpose**: Initializes a new instance of the `Barrier` class.
- **Behavior**: Sets up a barrier, meaning a specific point in which the threads wait until a certain number of them arrive.
- **Parameters**:
    - `count`: The number of threads required for the barrier to continue.
    - `completionFunction`: A function given as void pointer argument, that runs after the barrier is reached by `count` number of threads, before continuing.

#### Methods:

#### `void wait(int count)`

- **Purpose**: Waits for a certain number of threads, calls completion function once, continues code execution
- **Parameters**:
    - `count`: The number of threads required for the barrier to continue.
- **Behavior**: Use a condition variable on the generation variable to proceed only when generation increases, meaning that the barrier has been passed.

####   

## Server (`FL_Server` class in `server.cpp`)

#### Constructor: `FL_Server(int port, int numOfClients, BufferManager* agg_bm, BufferManager* clientBufferManager)`

- **Purpose**: Initializes the FL server with specified port, number of clients, aggregation buffer, and client buffer manager.
- **Parameters**:
    - `port`: Port number for the server to listen on.
    - `numOfClients`: Maximum number of clients the server will handle.
    - `agg_bm`: Pointer to a `BufferManager` for aggregated data buffer manager.
    - `clientBufferManager`: Pointer to a `BufferManager` managing buffers for each client's data.

#### Methods:

#### `void run()`

- **Purpose**: Starts the server to listen for incoming connections and handles them.
- **Behavior**: The server listens on the specified port and accepts incoming client connections up to the specified maximum number of clients. Each client connection is managed by a separate thread.

#### `void handleClientConnection(int clientSocket, int cCount)`

- **Purpose**: Manages individual client connections in separate threads.
- **Parameters**:
    - `clientSocket`: Socket descriptor for the connected client.
    - `cCount`: Count of the client being handled.
- **Behavior**: Receives data from the client, including a header and file data, processes it, and sends an acknowledgment back to the client. Waits for aggregation to complete before sending aggregated data back to the client.

#### `void aggregationDone()`

- **Purpose**: Notifies all waiting threads that aggregation is complete.
- **Behavior**: Sets the aggregation flag to true and wakes up all threads waiting on this condition.

#### Destructor: `~FL_Server()`

- **Purpose**: Cleans up resources upon server destruction.
- **Behavior**: Closes the server and client sockets, ensuring a clean shutdown.

  

## Client (`FL_Client` class in `client.cpp`)

#### Constructor: `TCPClient(const char* server_ip, int server_port, SharedBuffer* paramsBuffer, SharedBuffer* aggregationBuffer)`

- **Purpose**: Initializes the FL client with the server's IP address and port.
- **Parameters**:
    - `server_ip`: IP address of the server to connect to.
    - `server_port`: Port number of the server.
    - `paramsBuffer` : Buffer that contains the params to send
    - `aggregationBuffer` : Buffer that contains the aggregated data received from the server

- **Behavior**: Sets up the client socket and connects to the server.

#### Method: `void participate()`

- **Purpose**: Sends a file to the server along with its metadata.

- **Behavior**: Prepares and sends a header with data metadata, waits for acknowledgment, sends the data, and handles the server's response including receiving aggregated data. Repeat this process until convergeance.

#### Destructor: `~FL_Client()`

- **Purpose**: Ensures proper cleanup when the client object is destroyed.
- **Behavior**: Closes the client socket to ensure a clean shutdown.

  

  

## Sources:

- [https://www.geeksforgeeks.org/socket-programming-in-cpp/](https://www.geeksforgeeks.org/socket-programming-in-cpp/ "https://www.geeksforgeeks.org/socket-programming-in-cpp/")

- [https://www.geeksforgeeks.org/socket-programming-cc/](https://www.geeksforgeeks.org/socket-programming-cc/ "https://www.geeksforgeeks.org/socket-programming-cc/")

- [https://www.geeksforgeeks.org/socket-programming-in-cc-handling-multiple-clients-on-server-without-multi-threading/](https://www.geeksforgeeks.org/socket-programming-in-cc-handling-multiple-clients-on-server-without-multi-threading/ "https://www.geeksforgeeks.org/socket-programming-in-cc-handling-multiple-clients-on-server-without-multi-threading/")

- [https://github.com/RedAndBlueEraser/c-multithreaded-client-server/](https://github.com/RedAndBlueEraser/c-multithreaded-client-server/ "https://github.com/RedAndBlueEraser/c-multithreaded-client-server/")

- [https://www.youtube.com/watch?v=Pg\_4Jz8ZIH4&t=177s](https://www.youtube.com/watch?v=Pg_4Jz8ZIH4&t=177s "https://www.youtube.com/watch?v=Pg_4Jz8ZIH4&t=177s")
- [](https://cython.readthedocs.io/en/latest/src/userguide/index.html "https://cython.readthedocs.io/en/latest/src/userguide/index.html")[https://cython.readthedocs.io/en/latest/src/userguide/index.html](https://cython.readthedocs.io/en/latest/src/userguide/index.html)