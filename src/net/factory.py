"""Fábrica da pilha de rede.

Utiliza Address para definir como alvo da camada física simulada e VAddress para a
camada de transporte.
"""

import socket

from net.model.address import (
    Address,
    IPAddress,
    MACAddress,
    Port,
    VirtualAddress,
    VirtualIPAddress,
)
from net.stack.physical.impl import UDPSimulated

# --- Client A(lice) ---
CLIENT_A_NAME = "Alice"
CLIENT_A_MAC = MACAddress("AA:AA:AA:AA:AA:AA")
CLIENT_A_IP = IPAddress("10.0.0.1")
CLIENT_A_VIP = VirtualIPAddress("HOST_A")
CLIENT_A_PORT = Port(10000)
CLIENT_A_ADDRESS = Address(CLIENT_A_IP, CLIENT_A_PORT)
CLIENT_A_VADDRESS = VirtualAddress(CLIENT_A_VIP, CLIENT_A_PORT)

# --- Client B(ob) ---
CLIENT_B_NAME = "Bob"
CLIENT_B_MAC = MACAddress("BB:BB:BB:BB:BB:BB")
CLIENT_B_IP = IPAddress("10.0.0.2")
CLIENT_B_VIP = VirtualIPAddress("HOST_B")
CLIENT_B_PORT = Port(10001)
CLIENT_B_ADDRESS = Address(CLIENT_B_IP, CLIENT_B_PORT)
CLIENT_B_VADDRESS = VirtualAddress(CLIENT_B_VIP, CLIENT_B_PORT)

# --- Servidor ---
SERVER_NAME = "Servidor"
SERVER_MAC = MACAddress("CC:CC:CC:CC:CC:CC")
SERVER_IP = IPAddress("10.0.0.3")
SERVER_VIP = VirtualIPAddress("HOST_S")
SERVER_PORT = Port(10002)
SERVER_ADDRESS = Address(SERVER_IP, SERVER_PORT)
SERVER_VADDRESS = VirtualAddress(SERVER_VIP, SERVER_PORT)

# --- Roteador ---
ROUTER_NAME = "Roteador"
ROUTER_MAC = MACAddress("DD:DD:DD:DD:DD:DD")
ROUTER_IP = IPAddress("10.0.0.4")
ROUTER_VIP = VirtualIPAddress("HOST_R")
ROUTER_PORT = Port(10003)
ROUTER_ADDRESS = Address(ROUTER_IP, ROUTER_PORT)
ROUTER_VADDRESS = VirtualAddress(ROUTER_VIP, ROUTER_PORT)

# --- Tabela de mapeamento MAC -> Address (IP + Port) para a camada física simulada ---
MAC_TABLE = {
    CLIENT_A_MAC: CLIENT_A_ADDRESS,
    CLIENT_B_MAC: CLIENT_B_ADDRESS,
    SERVER_MAC: SERVER_ADDRESS,
    ROUTER_MAC: ROUTER_ADDRESS,
}


# --- Registro de hosts Nome -> (MAC, Address físico, VirtualAddress) ---
HOST_REGISTRY: dict[str, tuple[MACAddress, Address, VirtualAddress]] = {
    CLIENT_A_NAME: (CLIENT_A_MAC, CLIENT_A_ADDRESS, CLIENT_A_VADDRESS),
    CLIENT_B_NAME: (CLIENT_B_MAC, CLIENT_B_ADDRESS, CLIENT_B_VADDRESS),
    SERVER_NAME: (SERVER_MAC, SERVER_ADDRESS, SERVER_VADDRESS),
    ROUTER_NAME: (ROUTER_MAC, ROUTER_ADDRESS, ROUTER_VADDRESS),
}


def build_physical_layer(name: str) -> UDPSimulated:
    """Cria e vincula a camada física simulada para o host informado.

    Cria um socket UDP, faz bind no endereço físico do host e devolve
    a camada física pronta para uso.

    Args:
        name (str): Nome do host conforme definido neste módulo

    Returns:
        UDPSimulated: Camada física com socket já vinculado.

    Raises:
        KeyError: Se `name` não existir no registro de hosts.
    """
    if name not in HOST_REGISTRY:
        available = list(HOST_REGISTRY)
        raise KeyError(f"Host desconhecido: {name!r}. Disponíveis: {available}")

    _, address, _ = HOST_REGISTRY[name]
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((str(address.ip), int(address.port)))
    return UDPSimulated(sock, MAC_TABLE)
