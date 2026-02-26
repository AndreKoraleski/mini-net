"""Modulo contendo tipos de dados que servem como modelos para o projeto."""

from .address import (
    Address,
    IPAddress,
    MACAddress,
    Port,
    VirtualAddress,
    VirtualIPAddress,
)

__all__ = [
    "Address",
    "IPAddress",
    "MACAddress",
    "Port",
    "VirtualAddress",
    "VirtualIPAddress",
]
