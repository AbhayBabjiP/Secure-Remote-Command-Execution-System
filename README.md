Secure Remote Command Execution System

Overview:
This project implements a **secure client-server system** that allows authenticated clients to execute commands remotely and transfer files over a secure TLS connection.

The system supports:
* Remote command execution
* File upload and download
* Multi-client connections
* Secure communication using TLS

System Architecture

Client → TLS Socket → Server
↓
JSON Requests
↓
Server Processing
↓
JSON Responses

---

Design Choices & Implementation

* **TCP Sockets** → Reliable communication
* **TLS (SSL)** → Secure encrypted transmission
* **JSON Protocol** → Structured message exchange
* **Threading** → Supports multiple clients simultaneously
* **Subprocess Module** → Executes system commands
* **Base64 Encoding** → Handles file transfer
* **Logging Module** → Maintains audit logs

Features

* Secure TLS communication
* Authentication mechanism
* Remote command execution
* File upload (client → server)
* File download (server → client)
* Structured JSON protocol
* Audit logging
* Multi-client support
* Performance measurement



 Setup Instructions

 1️⃣ Install Requirements

* Python 3.x
* OpenSSL

---

2️⃣ Generate SSL Certificate

Run:

```bash
openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout key.pem
```

---

3️⃣ Run Server

```bash
python server.py
```

Output:

```
Secure Multi-Client Server Running...
Waiting for clients...
```

---

4️⃣ Run Client

```bash
python client.py
```

---

 Login Credentials

```
Username: admin
Password: password123
```

---

Usage Instructions

After login:

## 1. Execute Command

* Enter system command
* Example: `ls`, `dir`, `whoami`

---

 ## 2. Upload File

* Enter file path from client system
* Example:

```
C:\Users\Name\Desktop\file.txt
```

---

## 3. Download File

* Enter file name from server
* Choose save location

---

## 4. Exit

* Closes connection

---

## 🔐 Security Features

* TLS encryption for secure communication
* Authentication system
* Audit logging of all activities

---

## 📜 Audit Logging

Logs stored in:

```
audit.log
```

Includes:

* User login
* Commands executed
* File uploads/downloads

---

## Performance Evaluation

* Command execution is fast (milliseconds)
* File transfer time increases with file size
* Multi-client support using threading
* Slight delay with more clients

---

## Optimization & Fixes

* Improved error handling
* Handled invalid JSON inputs
* Managed client disconnections
* Fixed file transfer issues
* Optimized buffer usage

---

## Observations

* Efficient command execution
* Linear file transfer behavior
* Scalable system with threading

---

## Limitations

* Uses self-signed certificates
* No command restriction
* Command-line interface only

---

##  Future Enhancements

* GUI interface
* Command filtering
* Role-based authentication
* Better SSL validation

---

## Conclusion

This project demonstrates a **secure, scalable client-server system** integrating networking, security, and system programming concepts.

---

##  Author

Abhay Babji P
Prarthana Herur
Nikshep Gowda


