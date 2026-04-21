import socket, ssl, json, subprocess, time, logging, base64, os, threading

HOST, PORT = "0.0.0.0", 5000

USERS = {"admin": "password123"} //your wish

logging.basicConfig(
    filename="audit.log",
    level=logging.INFO,
    format="%(asctime)s %(message)s"
)

def run_cmd(cmd):
    start = time.time()
    try:
        out = subprocess.check_output(
            cmd, shell=True,
            stderr=subprocess.STDOUT,
            text=True
        )
    except subprocess.CalledProcessError as e:
        out = e.output
    return out, time.time() - start


def handle_client(conn, addr):

    try:
        print(f" Handling client: {addr}")

        #  Authentication
        data = conn.recv(4096).decode()
        req = json.loads(data)

        if USERS.get(req.get("username")) != req.get("password"):
            conn.send(json.dumps({"status": "AUTH_FAIL"}).encode())
            print(f" Authentication failed from {addr}")
            conn.close()
            return

        conn.send(json.dumps({"status": "AUTH_OK"}).encode())
        logging.info(f"{req['username']} connected from {addr}")
        print(f" {req['username']} logged in from {addr}")

        # Handle client requests
        while True:

            data = conn.recv(65536)
            if not data:
                break

            req = json.loads(data.decode())

            #  Execute command
            if req["action"] == "EXEC":

                print(f"Executing: {req['command']} from {addr}")

                output, t = run_cmd(req["command"])

                conn.send(json.dumps({
                    "status": "OK",
                    "output": output,
                    "execution_time": t
                }).encode())

                logging.info(f"{req['command']} executed ({t:.4f}s)")


            # Upload file
            elif req["action"] == "UPLOAD":

                filename = req["filename"]
                print(f" Upload request: {filename} from {addr}")

                filedata = base64.b64decode(req["data"])

                with open(filename, "wb") as f:
                    f.write(filedata)

                conn.send(json.dumps({"status": "UPLOAD_OK"}).encode())
                logging.info(f"Uploaded {filename}")


            #  Download file
            elif req["action"] == "DOWNLOAD":

                filename = req["filename"]
                print(f"Download request: {filename} from {addr}")

                if not os.path.exists(filename):
                    conn.send(json.dumps({"status": "NOT_FOUND"}).encode())
                    print(f" File not found: {filename}")
                    continue

                with open(filename, "rb") as f:
                    filedata = base64.b64encode(f.read()).decode()

                conn.send(json.dumps({
                    "status": "OK",
                    "filename": filename,
                    "data": filedata
                }).encode())

                logging.info(f"Downloaded {filename}")


            #  Exit
            elif req["action"] == "EXIT":
                print(f" Client requested disconnect: {addr}")
                break

    except Exception as e:
        print("Error:", e)

    finally:
        conn.close()
        print(f"Client disconnected: {addr}")


# TLS setup
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

# Server setup
server = socket.socket()
server.bind((HOST, PORT))
server.listen(5)

print(" Secure Multi-Client Server Running...")
print(" Waiting for clients...\n")

#  Accept clients
while True:
    client, addr = server.accept()

    print(f" New connection from: {addr}")   #  CONNECTION INDICATION

    conn = context.wrap_socket(client, server_side=True)

    threading.Thread(target=handle_client, args=(conn, addr)).start()
