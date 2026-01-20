# WhatsApp TIP (Template Instance Provider)

Este sistema utiliza o Evolution API para gerenciamento e envio massivo de mensagens via WhatsApp, oferecendo uma interface amigável e robusta para gerenciar múltiplas instâncias do WhatsApp de forma automatizada.

> **⚡ Integração com ChatGPT**: Esta versão do projeto integra o ChatGPT para aprimorar o envio de mensagens, permitindo a geração inteligente e personalização automática de conteúdo antes de enviar as mensagens via WhatsApp.

## 🚀 Tecnologias Utilizadas

- **Python 3.x**
- **Django 5.2.4** - Framework web
- **Django REST Framework 3.16.0** - Para construção da API REST
- **Celery 5.5.3** - Para processamento assíncrono de tarefas
- **MySQL** - Banco de dados (via mysqlclient 2.2.7)
- **Pandas 2.3.1** - Para manipulação de dados
- **Gunicorn 23.0.0** - Servidor WSGI para produção
- **WhiteNoise 6.9.0** - Para servir arquivos estáticos
- **python-dotenv** - Para gerenciamento de variáveis de ambiente
- **Evolution API** - API para integração com WhatsApp
- **OpenAI/ChatGPT** - Para processamento inteligente e personalização de mensagens

## 📁 Estrutura do Projeto

```
whats_tip/
├── instancias/                  # App para gerenciamento de instâncias do WhatsApp
├── instancias_utils/            # Utilitários e serviços para instâncias
│   ├── services/               # Serviços de negócio
│   └── views/                  # Views específicas para operações de instância
├── pages/                      # App para páginas estáticas
├── setup/                      # Configurações principais do projeto
├── static/                     # Arquivos estáticos (CSS, JS, etc.)
├── templates/                  # Templates HTML
│   ├── historico/
│   ├── index/
│   └── login/
└── users/                      # App para gestão de usuários
```

## 🔧 Apps Principais

### instancias
Gerencia o ciclo de vida das instâncias do WhatsApp, incluindo:
- Criação de novas instâncias
- Monitoramento de status
- Gerenciamento de instâncias ativas e encerradas

### instancias_utils
Contém utilitários e serviços para:
- Manipulação de banco de dados
- Serviços de evolução
- Utilitários gerais
- Views específicas para operações como:
  - Busca de instâncias
  - Criação de instâncias
  - Geração de QR Code
  - Envio de mensagens

### users
Gerenciamento de usuários do sistema, incluindo:
- Autenticação
- Autorização
- Perfis de usuário

## 🤖 Integração com ChatGPT

A partir desta versão, o projeto incorpora ChatGPT para aprimorar significativamente o envio de mensagens:

- **Geração de Conteúdo Inteligente**: O ChatGPT é utilizado para gerar ou otimizar mensagens automaticamente antes do envio
- **Personalização de Mensagens**: Adapta dinamicamente o conteúdo das mensagens com base em parâmetros e contexto
- **Serviço GPT**: Implementado em `instancias_utils/services/gpt_service.py` para fácil integração e extensão
- **Envio Automatizado**: As mensagens processadas pelo ChatGPT são enviadas automaticamente via WhatsApp através do Evolution API

Esta integração permite criar campanhas de mensagens mais personalizadas e relevantes, mantendo a automatização em larga escala.

## 💻 Como Executar o Projeto

1. Clone o repositório
2. Crie um ambiente virtual Python:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente em um arquivo `.env`

5. Execute as migrações:
```bash
python manage.py migrate
```

6. Inicie o servidor de desenvolvimento:
```bash
python manage.py runserver
```

7. Para produção, use o Gunicorn:
```bash
gunicorn setup.wsgi:application
```

### Configurações importantes para instâncias Baileys no Evolution API

Ao criar ou testar uma instância Baileys, algumas variáveis de ambiente são cruciais para garantir que o QR code seja gerado corretamente e que a sessão funcione sem problemas:

- `DEL_INSTANCE=true`  
  Garante que a instância seja criada do zero, sem resquícios de sessões antigas, evitando travamentos ou problemas de QR code.

- `CONFIG_SESSION_PHONE_CLIENT=Evolution API`  
  Nome do cliente que aparecerá nos logs e na identificação da sessão.

- `CONFIG_SESSION_PHONE_NAME=Chrome`  
  Define o "browser" simulado pelo Baileys. Normalmente, manter como `Chrome` evita incompatibilidades.

- `CONFIG_SESSION_PHONE_VERSION=2.3000.1029423425`  
  Versão específica do Baileys usada na sessão. Essencial para compatibilidade com esta versão do Evolution API.

- `CACHE_REDIS_ENABLED=false`  
  Desativa o cache em Redis, garantindo que a sessão seja inicializada do zero.  
  ⚠️ Útil para testes ou quando o QR code não está sendo gerado devido a instâncias antigas no cache.  
  Em produção, pode ser ativado (`true`) para persistência de sessões entre reinícios do container.

> 💡 Dica: sempre que houver problemas com QR code ou instâncias presas em `"connecting"`, verifique essas variáveis e considere limpar o cache do Redis.



## 🔄 Celery e RabbitMQ

O projeto está em processo de migração do processamento assíncrono via threads para um sistema de filas utilizando Celery com RabbitMQ. Atualmente, as seguintes configurações já foram implementadas:

### Configurações Atuais (28/10/2025):

1. **Arquivo `setup/celery.py`**:
   - Configuração básica do Celery
   - Integração com as configurações do Django
   - Descoberta automática de tasks (`autodiscover_tasks`)

2. **Configurações no `settings.py`**:
   - Integração com RabbitMQ configurada
   - Variáveis de ambiente para credenciais do RabbitMQ
   - Configurações de broker e backend:
     ```python
     CELERY_BROKER_URL = 'amqp://{user}:{password}@{host}:{port}/{vhost}'
     CELERY_RESULT_BACKEND = 'rpc://'
     CELERY_TASK_TRACK_STARTED = True
     CELERY_TASK_ACKS_LATE = True
     ```

### Para Iniciar o Worker:
```bash
celery -A setup worker -l info
```

### Próximos Passos:
- Implementar tasks assíncronas para processamento de mensagens
- Configurar monitoramento de filas
- Implementar retry policies para tasks falhas
- Adicionar tasks periódicas (se necessário)

