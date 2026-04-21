import socket, ssl, json, base64, os

# CHANGE THIS to server IP when using another laptop
HOST = "xx.xx.xx.xxx"  
PORT = 5000

# TLS (no verification for self-signed cert)
context = ssl._create_unverified_context()

print("Connecting to server...")

sock = socket.socket()
conn = context.wrap_socket(sock, server_hostname=HOST)
conn.connect((HOST, PORT))

print("Connected to server!")


# Authentication
username = input("Username: ")
password = input("Password: ")

conn.send(json.dumps({
    "username": username,
    "password": password
}).encode())

res = json.loads(conn.recv(4096).decode())

if res["status"] != "AUTH_OK":
    print("Authentication Failed")
    conn.close()
    exit()

print("Authentication Successful")


#  Main Menu
while True:

    print("\n====== MENU ======")
    print("1. Execute Command")
    print("2. Upload File")
    print("3. Download File")
    print("4. Exit")

    choice = input("Enter choice: ")

    # COMMAND EXECUTION
    if choice == "1":

        cmd = input("Enter command: ")

        conn.send(json.dumps({
            "action": "EXEC",
            "command": cmd
        }).encode())

        res = json.loads(conn.recv(65536).decode())

        print("\n----- OUTPUT -----")
        print(res["output"])
        print("------------------")
        print("Execution time:", res["execution_time"], "seconds")


    # FILE UPLOAD
    elif choice == "2":

        path = input("Enter file path to upload: ")

        if not os.path.exists(path):
            print("File not found")
            continue

        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode()

        conn.send(json.dumps({
            "action": "UPLOAD",
            "filename": os.path.basename(path),
            "data": data
        }).encode())

        response = conn.recv(4096).decode()
        print("Server:", response)


    #  FILE DOWNLOAD
    elif choice == "3":

        name = input("Enter file name (on server): ")

        conn.send(json.dumps({
            "action": "DOWNLOAD",
            "filename": name
        }).encode())

        res = json.loads(conn.recv(65536).decode())

        if res["status"] == "OK":

            save_path = input("Enter path to save file (press Enter for current folder): ")

            if save_path == "":
                save_file = res["filename"]
            else:
                save_file = os.path.join(save_path, res["filename"])

            with open(save_file, "wb") as f:
                f.write(base64.b64decode(res["data"]))

            print(f" File saved at: {save_file}")

        else:
            print(" File not found on server")


    # EXIT
    elif choice == "4":

        conn.send(json.dumps({"action": "EXIT"}).encode())
        print("Disconnected from server")
        break


    else:
        print(" Invalid choice")


conn.close()
