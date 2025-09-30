# Projeto Integrador 3 - Fatec Ipiranga (Pastor Éneas Tognini)

## 👥 Integrantes da Equipe

- Thiago Cardoso Davi (RA: 2041382421015)
- Lucas Antonio Evangelista Dos Santos (RA: 2041382411010)
- Daniel Fernando Dos Santos (RA: 2041382421027)
- Murilo Santos Da Silva (RA: 2041382411043)
- Pablo Roberto Da Silva Costa (RA: 2041382421005)
- William Nunes Vilany (RA: 2041382421030)

# 🏞️ Tour4Friends - Aplicação de Planejamento de Viagens

## 📋 Sobre o Projeto

Aplicativo web para planejamento de viagens em grupo, focado no Caminho de Santiago. Esta versão simplificada utiliza Flask no backend e JavaScript puro no frontend, proporcionando uma experiência direta e eficiente para os usuários.

## 🎯 Objetivo

Utilizando a análise de Big Data, nosso objetivo é mergulhar no comportamento e nas preferências dos viajantes para oferecer pacotes de viagem totalmente personalizados. A meta é clara:

- Aumentar a satisfação do cliente, criando experiências únicas.
- Otimizar a receita da empresa de turismo com ofertas direcionadas.
- Prever tendências de mercado, garantindo decisões estratégicas mais eficientes e proativas.

## 🚀 Funcionalidades

- ✅ Autenticação segura de usuários
- 📅 Visualização detalhada de itinerários diários
- 🗺️ Mapa interativo com rotas e pontos de interesse
- 💬 Chat de suporte integrado
- 📱 Design responsivo para todos os dispositivos

## 🛠️ Tecnologias Utilizadas

### Frontend
- HTML5, CSS3, JavaScript puro (Vanilla JS)
- Google Maps JavaScript API (para visualização de rotas)
- Font Awesome (ícones)
- Design responsivo com CSS Flexbox/Grid

### Backend
- Python 3.8+
- Flask (framework web leve)
- JWT para autenticação segura
- SQLite para armazenamento de dados
- CORS para requisições entre domínios

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Navegador web moderno (Chrome, Firefox, Edge, Safari)
- Conexão com a internet (para carregar as APIs externas)
- Git (opcional, para clonar o repositório)

## 🚀 Guia Rápido de Execução

Siga estes passos para executar o projeto localmente:

### 1. Terminal 1 - Iniciar o Backend

```bash
# Navegue até a pasta do projeto
cd "Projeto 10 - Projeto Integrador 3"

# Crie e ative o ambiente virtual (apenas na primeira vez)
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instale as dependências
pip install -r backend/requirements.txt

# Inicie o servidor backend
cd backend
python app.py
```

### 2. Terminal 2 - Iniciar o Frontend

Abra um novo terminal e execute:

```bash
# Navegue até a pasta do projeto (se necessário)
cd "Projeto 10 - Projeto Integrador 3"

# Inicie um servidor web simples para o frontend
# Opção 1: Usando Python (recomendado)
cd frontend
python -m http.server 8000

# Ou Opção 2: Abra diretamente o arquivo HTML no navegador
# (pode ter restrições de CORS)
# Clique com o botão direito em frontend/index.html e abra com o navegador
```

### 3. Acesse a Aplicação

1. Abra seu navegador e acesse:
   - Frontend: `http://localhost:8000` (ou o caminho local do arquivo)
   - Backend API: `http://localhost:5000`

2. Faça login com as credenciais de teste:
   - **Email:** `admin@example.com`
   - **Senha:** `senha123`

### ⚠️ Solução de Problemas Comuns

- **Erro de CORS**: Se encontrar erros de CORS, certifique-se de acessar o frontend através de um servidor web (não diretamente pelo arquivo).
- **Porta em uso**: Se a porta 5000 ou 8000 estiver em uso, altere a porta no comando respectivo.
- **Dependências faltando**: Se houver erros de importação, verifique se todas as dependências foram instaladas corretamente com `pip install -r backend/requirements.txt`.

## 🗂️ Estrutura do Projeto

```
.
├── backend/               # Código do servidor
│   ├── app.py            # Aplicação principal Flask
│   ├── requirements.txt  # Dependências do Python
│   └── instance/         # Pasta para o banco de dados SQLite
├── frontend/             # Código da interface
│   ├── index.html        # Página principal
│   └── js/               # Código JavaScript
│       └── app.js        # Lógica da aplicação
└── README.md             # Este arquivo
```

## 🌐 API Endpoints

### Autenticação
- `POST /api/auth/login` - Autenticação de usuário
  ```json
  // Request
  {
    "email": "admin@example.com",
    "password": "senha123"
  }
  
  // Response
  {
    "access_token": "seu_token_jwt_aqui",
    "user": {
      "id": 1,
      "email": "admin@example.com",
      "name": "Admin"
    }
  }
  ```

### Itinerário
- `GET /api/itinerary` - Lista o itinerário completo
- `GET /api/days/<day_id>/map` - Detalhes do mapa para um dia específico
  - Inclui a rota (polyline) e pontos de interesse

### Chat
- `GET /api/chat/messages` - Lista as mensagens do chat
- `POST /api/chat/messages` - Envia uma nova mensagem
  ```json
  // Request
  {
    "text": "Olá, preciso de ajuda com meu roteiro."
  }
  ```

## 🔒 Segurança

- Todas as rotas da API (exceto login) requerem autenticação via JWT
- O token JWT deve ser enviado no header `Authorization: Bearer <token>`
- O token expira após 12 horas

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🙋‍♂️ Suporte

Em caso de dúvidas ou problemas, abra uma issue no repositório do projeto.
 
### Variáveis de Ambiente
- Backend (`backend/.env`):
  - `SECRET_KEY`, `JWT_SECRET_KEY` (obrigatório trocar em produção)
  - `DATABASE_URL` (padrão: `sqlite:///tour4friends.db`)
  - `CORS_ORIGINS` (ex.: `http://localhost:5173`)
=======



>>>>>>> 73c66f3c6e8b2e92adaa24569814e065d57a573d
