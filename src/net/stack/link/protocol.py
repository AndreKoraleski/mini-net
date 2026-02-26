"""Interface para a camada de enlace."""

from __future__ import annotations


from typing import Protocol, runtime_checkable

from net.base import Packet
from net.model import VirtualIPAddress


@runtime_checkable
class Link(Protocol):
    """Interface para a camada de enlace."""

    def send(self, packet: Packet, destination: VirtualIPAddress) -> None:
        """Envia um pacote para o endereço virtual de destino.

        Args:
            packet (Packet): O pacote a ser enviado.
            destination (VirtualIPAddress): O endereço virtual de destino.
        """
        ...

    def receive(self) -> Packet | None:
        """Recebe um pacote da camada de enlace.

        Returns:
            Packet | None: O pacote recebido, ou None se descartado por
                erro de integridade.
        """
        ...
