# A Mini Net

![Python](https://img.shields.io/badge/python-3.11%2B-3776AB?logo=python&logoColor=white)
![LICENSE](https://img.shields.io/badge/licen%C3%A7a-MIT-22c55e)
![INF-UFG](https://img.shields.io/badge/INF--UFG-Redes%202025%2F4-f97316)

Projeto integrador da disciplina de **Redes de Computadores – INF-UFG 2025/4**.

**Autores:** Andre Koraleski &amp; Henrick Souza

O produto final é uma aplicação de **chat** que funciona sobre um canal
propositalmente defeituoso (perda de pacotes, corrupção de bits, latência
variável), implementando do zero todas as garantias que normalmente delegaríamos
ao TCP.

O Manual do Projeto indica quatro fases, começando pela aplicação e terminando na camada de enlace. 

No entanto, como a estrutura é a de uma pilha, nós preferimos ir pelo exato contrário, começando pela base que todos acima dependem e então encapsulando. Isso pode ser visto no histórico de *commits* do projeto.

Esta é a terceira e derradeira versão do repositório, com uma estrutura mais intuitiva, maneira mais simples de se executar e uma narrativa embutida em seus metadados enquanto (tentando) esconder grande parte do processo sujo de desenvolvimento rápido realizado por nós dois em um repositório privado.

```
┌─────────────┐
│  Aplicação  │  <- Quinto Implementado
├─────────────┤
│  Transporte │  <- Quarto Implementado
├─────────────┤
│    Rede     │  <- Terceiro Implementado
├─────────────┤
│   Enlace    │  <- Segundo Implementado
├─────────────┤
│   Física    │  <- Primeiro Implementado
├─────────────┤
│  UDP real   │
└─────────────┘
```

## Topologia

```mermaid
graph LR
    A["Alice<br/>HOST_A · :10000"]
    B["Bob<br/>HOST_B · :10001"]
    S["Servidor<br/>HOST_S · :10002"]
    R["Roteador<br/>HOST_R · :10003"]

    A -- ARP: DD:DD --> R
    B -- ARP: DD:DD --> R
    S -- ARP: DD:DD --> R

    R -- ARP: AA:AA --> A
    R -- ARP: BB:BB --> B
    R -- ARP: CC:CC --> S
```

Todos os nós rodam em `127.0.0.1`, diferenciados pela porta. Hosts enxergam o
Roteador como único vizinho via ARP. O Roteador conhece todos diretamente.

| Host     | VIP    | MAC               | Porta |
| -------- | ------ | ----------------- | ----- |
| Alice    | HOST_A | AA:AA:AA:AA:AA:AA | 10000 |
| Bob      | HOST_B | BB:BB:BB:BB:BB:BB | 10001 |
| Servidor | HOST_S | CC:CC:CC:CC:CC:CC | 10002 |
| Roteador | HOST_R | DD:DD:DD:DD:DD:DD | 10003 |

## Código fornecido pelo professor

O módulo [`net.base.protocol`](src/net/base/protocol.py) é fornecido pronto e não deve
ser modificado. Ele define as três PDUs da pilha — `Segmento`, `Pacote` e
`Quadro` — bem como a função `enviar_pela_rede_ruidosa`, que injeta perda,
corrupção de bits e latência variável antes de chamar `sock.sendto`. Todo o
resto do projeto consome essas abstrações mas não as reimplementa.

## Estrutura do Código

```
src/net/
├── base/
│   └── protocol.py *            <- PDUs (Segmento, Pacote, Quadro) + enviar_pela_rede_ruidosa
├── model/
│   └── address.py               <- Port, IPAddress, VirtualIPAddress, MACAddress
├── stack/
│   ├── factory.py               <- build_*_layer(), tabelas ARP/MAC/roteamento
│   ├── physical/
│   │   ├── protocol.py
│   │   └── impl/udp_simulated.py
│   ├── link/
│   │   ├── protocol.py
│   │   └── impl/simple.py
│   ├── network/
│   │   ├── protocol.py
│   │   └── impl/  host.py · router.py
│   └── transport/
│       ├── protocol.py
│       └── impl/  reliable_connection.py · reliable_transport.py
└── application/
    ├── client.py · server.py · router.py
    ├── chat/  codec.py · text.py · file.py · system.py
    └── ui/  protocol.py · impl/  console.py · gui.py

* Fornecido pelo professor — não modificado.
```

## Ordem de Desenvolvimento

### 0 — Endereços

[`model/address.py`](src/net/model/address.py)

Classes que padronizam e validam os tipos de endereço usados em toda a pilha:
`Port`, `IPAddress`, `VirtualIPAddress`, `MACAddress`, `Address` e `VirtualAddress`.

### 1 — Camada Física · `UDPSimulated`

[`physical/protocol.py`](src/net/stack/physical/protocol.py) · [`physical/impl/udp_simulated.py`](src/net/stack/physical/impl/udp_simulated.py)

`UDPSimulated` abre um socket UDP, usa `enviar_pela_rede_ruidosa` (professor)
para enviar e `sock.recvfrom` para receber, resolvendo o MAC de destino numa
tabela estática para obter o endereço UDP real. `build_physical_layer(name)`
cria o socket e faz `bind` antes de retornar.

### 2 — Camada de Enlace · `SimpleLink`

[`link/protocol.py`](src/net/stack/link/protocol.py) · [`link/impl/simple.py`](src/net/stack/link/impl/simple.py)

`SimpleLink` encapsula pacotes em `Frame` (professor), delega o envio à camada
física e, na recepção, verifica a integridade via CRC (professor). A resolução
de endereços físicos é feita por tabela ARP estática: Alice, Bob e Servidor
apontam apenas para o Roteador. O Roteador conhece todos.
`build_link_layer(name)` compõe a camada física internamente.

### 3 — Camada de Rede · `HostNetwork` / `RouterNetwork`

[`network/protocol.py`](src/net/stack/network/protocol.py) · [`network/impl/host.py`](src/net/stack/network/impl/host.py) · [`network/impl/router.py`](src/net/stack/network/impl/router.py)

- **`HostNetwork`** — hosts comuns. `send()` consulta a tabela de roteamento e
  delega ao enlace. `receive()` bloqueia até um pacote endereçado ao VIP local
  e devolve o `Segment` interno.

- **`RouterNetwork`** — roteador. `receive()` decrementa o TTL, descarta se
  expirado e reencaminha via enlace. Sempre retorna `None`.

`build_network_layer(name)` escolhe a implementação correta e compõe as camadas
inferiores.

### 4 — Camada de Transporte · `ReliableConnection` / `ReliableTransport`

[`transport/protocol.py`](src/net/stack/transport/protocol.py) · [`transport/impl/reliable_connection.py`](src/net/stack/transport/impl/reliable_connection.py) · [`transport/impl/reliable_transport.py`](src/net/stack/transport/impl/reliable_transport.py)

- **`ReliableConnection`** — Stop-and-Wait para um par de endereços. `send()`
  fragmenta em chunks de MSS e retransmite até receber ACK. `receive()`
  reagrupa até `more=False`. `close()` envia FIN unilateral e aguarda ACK.
  `dispatch()` é chamado pelo transport para rotear segmentos às filas internas.

- **`ReliableTransport`** — multiplexador com thread daemon que lê
  continuamente da rede e despacha para a conexão correta pela chave
  `(remote_vip, remote_port, local_port)`. `connect()` abre uma conexão
  de saída; `accept()` bloqueia até uma entrada ser detectada.

`build_transport_layer(name)` monta a pilha completa e retorna o transport já
ativo. Não aceita o roteador.

### 5 — Camada de Aplicação · `Server` / `Client`

[`application/server.py`](src/net/application/server.py) · [`application/client.py`](src/net/application/client.py) · [`application/router.py`](src/net/application/router.py) · [`application/chat/`](src/net/application/chat) · [`application/ui/`](src/net/application/ui)

- **`Server`** — servidor centralizado que aceita conexões de clientes,
  gerencia a lista de usuários online e retransmite mensagens entre pares. Ao
  conectar, cada cliente recebe automaticamente a lista de usuários já online.
  Suporta **shutdown gracioso**: ao receber `Ctrl+C`, transmite `__SHUTDOWN__`
  para todos os clientes e aguarda cada um fechar sua conexão (FIN) antes de
  encerrar, sem descartar mensagens já enfileiradas.

- **`Client`** — conecta ao servidor assim que é iniciado. A UI sobe
  imediatamente enquanto a conexão TCP é estabelecida em background. Ao receber `__SHUTDOWN__`, fecha a conexão sozinho. Suporta duas interfaces intercambiáveis via protocolo `UI`:
  - **`ConsoleUI`** — stdin/stdout com comando `/file <caminho>` para envio de
    arquivos.
  - **`GUI`** — interface Tkinter com área de chat, lista de usuários online e
    barra de status.

  A seleção da UI é automática: sem TTY ou com `--gui`, usa a GUI.

**Protocolo de mensagens (JSON):**

Todas as mensagens são serializadas em JSON com os campos `type`, `sender`,
`recipient` e `timestamp`. Mensagens de texto incluem `content`. Mensagens de
arquivo adicionam `name`, `mime`, `size` e `data` (Base64). Mensagens de
sistema são notificações internas sem remetente.

## Instalação

Clone o repositório e instale o pacote em modo editável.

**Com uv (recomendado):**

```bash
uv sync
```

**Com pip:**

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .
```

## Como executar

Inicie os componentes na seguinte ordem:

**1. Roteador** (necessário para comunicação entre hosts):

```bash
uv run router
# Com ambiente ativo: router
```

**2. Servidor** (centraliza as conexões):

```bash
uv run server
# Com ambiente ativo: server
```

**3. Clientes** (Alice e Bob):

```bash
# Alice - interface automática (console se TTY disponível)
uv run alice
# Com ambiente ativo: alice

# Alice - forçar interface gráfica
uv run alice -- --gui
# Com ambiente ativo: alice --gui

# Bob - interface automática
uv run bob
# Com ambiente ativo: bob

# Bob - forçar interface gráfica
uv run bob -- --gui
# Com ambiente ativo: bob --gui
```

**Comandos no console:**

- Digite texto e pressione Enter para enviar mensagem
- `/file <caminho>` para enviar arquivo
- `Ctrl+C` para sair

**Interface gráfica:**

- Digite na caixa de texto e pressione Enter ou clique "Enviar"
- Botão "Arquivo" para selecionar e enviar arquivo
- Lista de usuários online atualizada em tempo real
- Barra de status mostra conexão

Todos os arquivos recebidos são salvos em `downloads/<destinatário>/`.
