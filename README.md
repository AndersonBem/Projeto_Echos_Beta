# Projeto Echos Beta

![Logo](caminho/para/logo.png)  
Sistema web para gerenciamento de laudos veterinários, desenvolvido em Django.

## 📌 Visão Geral
O **Projeto Echos Beta** foi criado para facilitar o gerenciamento de exames e laudos em clínicas veterinárias. Ele permite o cadastro de tutores, pacientes, veterinários e clínicas, além da geração e organização de laudos médicos.

## 🚀 Funcionalidades
- 🏥 **Cadastro e gerenciamento** de tutores, pacientes, veterinários e clínicas
- 📄 **Criação e gestão** de laudos veterinários
- 📅 **Agendamentos e envios programados**
- 🔍 **Busca e filtros avançados** para facilitar a navegação
- 📊 **Relatórios e projeções financeiras**
- 🔄 **Backup e restauração** dos dados

## 🛠️ Tecnologias Utilizadas
- **Back-end:** Django (Python)
- **Front-end:** HTML, CSS, Bootstrap
- **Banco de Dados:** SQLite (padrão) ou PostgreSQL (opcional)
- **Geração de PDFs:** WeasyPrint

## ⚙️ Como Instalar

### 1️⃣ Clonar o Repositório
```bash
$ git clone https://github.com/AndersonBem/Projeto_Echos_Beta.git
$ cd Projeto_Echos_Beta
```

### 2️⃣ Criar e Ativar um Ambiente Virtual
```bash
$ python -m venv venv
$ source venv/bin/activate  # Linux/macOS
$ venv\Scripts\activate    # Windows
```

### 3️⃣ Instalar as Dependências
```bash
$ pip install -r requirements.txt
```

### 4️⃣ Configurar o Banco de Dados
```bash
$ python manage.py migrate
$ python manage.py createsuperuser  # Criar um usuário admin
```

### 5️⃣ Rodar o Servidor
```bash
$ python manage.py runserver
```
Acesse o sistema em: `http://127.0.0.1:8000`

## 📷 Capturas de Tela
![Tela Inicial](caminho/para/tela_inicial.png)
![Lista de Tutores](caminho/para/lista_tutores.png)
![Lista de Pacientes](caminho/para/lista_pacientes.png)

## 📜 Licença
Este projeto é de código aberto e está disponível sob a licença MIT.

---
Desenvolvido por [AndersonBem](https://github.com/AndersonBem).

