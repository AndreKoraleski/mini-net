"""Interface para a camada física."""

from __future__ import annotations


from typing import Protocol, runtime_checkable


@runtime_checkable
class Physical(Protocol):
    """Interface para a camada física."""

    def send(self, data: bytes) -> None:
        """Envia dados pela camada física.

        Args:
            data (bytes): Os dados a serem enviados.
        """
        ...

    def receive(self) -> bytes:
        """Recebe dados da camada física.

        Returns:
            bytes: Os dados recebidos.
        """
        ...
