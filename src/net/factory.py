"""Fábrica da pilha de rede.

Utiliza Address para definir como alvo da camada física simulada e VAddress para a
camada de transporte.
"""

import socket

from net.model.address import Address, IPAddress, MACAddress, Port, VAdress, VIPAddress
from net.stack.physical.impl import UDPSimulated

# --- Client A(lice) ---
CLIENT_A_MAC = MACAddress("AA:AA:AA:AA:AA:AA")
CLIENT_A_IP = IPAddress("10.0.0.1")
CLIENT_A_VIP = VIPAddress("HOST_A")
CLIENT_A_PORT = Port(10000)
CLIENT_A_ADDRESS = Address(CLIENT_A_IP, CLIENT_A_PORT)
CLIENT_A_VADDRESS = VAdress(CLIENT_A_VIP, CLIENT_A_PORT)

# --- Client B(ob) ---
CLIENT_B_MAC = MACAddress("BB:BB:BB:BB:BB:BB")
CLIENT_B_IP = IPAddress("10.0.0.2")
CLIENT_B_VIP = VIPAddress("HOST_B")
CLIENT_B_PORT = Port(10001)
CLIENT_B_ADDRESS = Address(CLIENT_B_IP, CLIENT_B_PORT)
CLIENT_B_VADDRESS = VAdress(CLIENT_B_VIP, CLIENT_B_PORT)

# --- Servidor ---
SERVER_MAC = MACAddress("SS:SS:SS:SS:SS:SS")
SERVER_IP = IPAddress("10.0.0.3")
SERVER_VIP = VIPAddress("HOST_S")
SERVER_PORT = Port(10002)
SERVER_ADDRESS = Address(SERVER_IP, SERVER_PORT)
SERVER_VADDRESS = VAdress(SERVER_VIP, SERVER_PORT)

# --- Roteador ---
ROUTER_MAC = MACAddress("RR:RR:RR:RR:RR:RR")
ROUTER_IP = IPAddress("10.0.0.4")
ROUTER_VIP = VIPAddress("HOST_R")
ROUTER_PORT = Port(10003)
ROUTER_ADDRESS = Address(ROUTER_IP, ROUTER_PORT)
ROUTER_VADDRESS = VAdress(ROUTER_VIP, ROUTER_PORT)

# --- Tabela de mapeamento MAC -> Address (IP + Port) para a camada física simulada ---
MAC_TABLE = {
    CLIENT_A_MAC: CLIENT_A_ADDRESS,
    CLIENT_B_MAC: CLIENT_B_ADDRESS,
    SERVER_MAC: SERVER_ADDRESS,
    ROUTER_MAC: ROUTER_ADDRESS,
}


def create_udp_physical_layer(sock: socket.socket) -> UDPSimulated:
    """Cria uma instância da camada física simulada usando UDP.

    Args:
        sock (socket.socket): O socket UDP para enviar e receber dados.

    Returns:
        UDPSimulated: Uma instância da camada física simulada.
    """
    return UDPSimulated(sock, MAC_TABLE)
