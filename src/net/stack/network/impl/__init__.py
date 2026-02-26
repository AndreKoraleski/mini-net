"""Pacote de implementações da camada de rede."""

from __future__ import annotations


from .host import HostNetwork
from .router import RouterNetwork

__all__ = [
    "HostNetwork",
    "RouterNetwork",
]
