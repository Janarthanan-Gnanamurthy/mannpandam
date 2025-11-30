import os
import threading
import socket
import select
from urllib.parse import quote_plus
import logging
from dotenv import load_dotenv
import paramiko

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# SSH details
SSH_HOST = os.getenv("SSH_HOST")
SSH_PORT = int(os.getenv("SSH_PORT", 22))
SSH_USERNAME = os.getenv("SSH_USERNAME")
SSH_PKEY = os.getenv("SSH_PKEY")          # Path to .pem file
SSH_PASSWORD = os.getenv("SSH_PASSWORD")  # If not using .pem

# DB details
DB_HOST = os.getenv("DB_HOST")            # RDS private endpoint
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

ssh_client = None
forward_thread = None
local_forward_port = None


# ---------------------------------------------------------
# SSH Port Forwarding (Paramiko)
# ---------------------------------------------------------

class ForwardServer (socket.socket):
    pass


class Handler:
    def __init__(self, channel, local_socket):
        self.channel = channel
        self.local_socket = local_socket

    def start(self):
        while True:
            r, w, x = select.select([self.channel, self.local_socket], [], [])
            if self.local_socket in r:
                data = self.local_socket.recv(1024)
                if len(data) == 0:
                    break
                self.channel.send(data)
            if self.channel in r:
                data = self.channel.recv(1024)
                if len(data) == 0:
                    break
                self.local_socket.send(data)

        self.channel.close()
        self.local_socket.close()


def forward_tunnel(local_port, remote_host, remote_port, transport):
    """Forward local_port → remote_host:remote_port"""
    logger.info(f"Forwarding 127.0.0.1:{local_port} → {remote_host}:{remote_port}")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', local_port))
    server_socket.listen(100)
    logger.info("Tunnel ready.")

    global forward_thread

    def accept_connections():
        while True:
            client_socket, addr = server_socket.accept()
            logger.info(f"Tunnel connection from {addr}")

            channel = transport.open_channel(
                "direct-tcpip",
                (remote_host, remote_port),
                client_socket.getsockname(),
            )

            handler = Handler(channel, client_socket)
            handler.start()

    forward_thread = threading.Thread(target=accept_connections)
    forward_thread.daemon = True
    forward_thread.start()


def create_ssh_tunnel():
    """Establish SSH connection and port forward without sshtunnel"""
    global ssh_client, local_forward_port

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    logger.info(f"Connecting to SSH: {SSH_USERNAME}@{SSH_HOST}:{SSH_PORT}")

    if SSH_PKEY:
        key = paramiko.RSAKey.from_private_key_file(SSH_PKEY)
        ssh_client.connect(SSH_HOST, SSH_PORT, SSH_USERNAME, pkey=key)
    else:
        ssh_client.connect(SSH_HOST, SSH_PORT, SSH_USERNAME, password=SSH_PASSWORD)

    transport = ssh_client.get_transport()

    # Get free local port
    sock = socket.socket()
    sock.bind(('', 0))
    local_forward_port = sock.getsockname()[1]
    sock.close()

    forward_tunnel(local_forward_port, DB_HOST, DB_PORT, transport)

    logger.info(f"SSH tunnel active on 127.0.0.1:{local_forward_port}")

    return local_forward_port


# ---------------------------------------------------------
# SQLAlchemy Setup
# ---------------------------------------------------------

def get_database_url():
    global local_forward_port

    if not local_forward_port:
        local_forward_port = create_ssh_tunnel()

    encoded_user = quote_plus(DB_USER)
    encoded_password = quote_plus(DB_PASSWORD)

    return (
        f"postgresql://{encoded_user}:{encoded_password}"
        f"@127.0.0.1:{local_forward_port}/{DB_NAME}"
    )


try:
    DATABASE_URL = get_database_url()
    engine = engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True, 
    pool_recycle=150  
)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    logger.info("Database engine created successfully.")
except Exception as e:
    logger.error(f"Database connection failed: {e}")
    raise


Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def close_ssh_tunnel():
    if ssh_client:
        ssh_client.close()
        logger.info("SSH tunnel closed.")
