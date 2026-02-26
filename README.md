# A Mini Net

 Simulação de pilha de protocolos de rede (Enlace, Rede, Transporte e Aplicação) sobre UDP, implementada como projeto integrador da disciplina de Redes de Computadores.


## Ordem de Desenvolvimento

1. Adicionadas classes para padronizar e validar os endereços de `Porta`, `IP`, `VIP`, `MAC`, etc.
2. Implementada a **Camada Física** (`UDPSimulated`) sobre UDP real, com simulação de perda, corrupção de bits e latência variável, todos fornecidos. A fábrica (`factory.py`) expõe `build_physical_layer(name)` para montar a camada com socket já vinculado.
