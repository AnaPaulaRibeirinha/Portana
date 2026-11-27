# Portana

Sistema de controle de acesso inteligente para portaria e moradores.

## Arquitetura inicial

O backend será organizado por responsabilidade, com o domínio protegido de detalhes de FastAPI, banco, Socket.IO e Firebase:

```text
backend/
└── app/
    ├── api/            # Rotas HTTP, dependências e schemas de entrada/saída
    ├── application/    # Casos de uso e portas (interfaces)
    ├── domain/         # Entidades, enums e regras centrais de acesso
    ├── infrastructure/ # SQLAlchemy, JWT, Socket.IO e Firebase
    └── main.py         # Composição da aplicação
```

Fluxo principal:

```text
Flutter
  │ HTTP / WebSocket
  ▼
FastAPI ── autenticação ── caso de uso de acesso
                              │
              ┌───────────────┼────────────────┐
              ▼               ▼                ▼
          PostgreSQL       Socket.IO          FCM
          (persistência)   (monitoramento)    (alertas)
```

O banco oficial do projeto é PostgreSQL. Para subir uma instância local, use o serviço `postgres` do [docker-compose.yml](./docker-compose.yml) e configure `DATABASE_URL=postgresql+psycopg://portana:portana@localhost:5432/portana`. Os testes unitários usam SQLite em memória para serem rápidos e isolados.

## Executar localmente

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
cd ..
docker compose up -d postgres
cd backend
uvicorn app.main:app --reload
```

Documentação da API: <http://localhost:8000/docs>.

## Escopo do MVP backend

1. Autenticação JWT e perfis `ADMIN`, `PORTEIRO` e `MORADOR` (`POST /api/v1/auth/login`).
2. Cadastro de usuários protegido por perfil (`POST /api/v1/users`) e consulta do perfil atual (`GET /api/v1/users/me`).
3. Regras de horário por dia da semana e ponto de acesso.
4. Simulação de passagem com registro imutável do resultado.
5. Evento `access_attempt.created` para o painel ao vivo.
6. Porta para notificações push, com Firebase como adaptador posterior.

As evoluções de offline-first, QR Code, MQTT, visão computacional e geofencing ficam fora do MVP e devem consumir os casos de uso existentes, sem colocar regra de negócio nas rotas.
