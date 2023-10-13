# VitaLab_PSW - Sistema de Gerenciamento de Exames Médicos

Bem-vindo ao repositório do VitaLab_PSW, uma aplicação web desenvolvida durante o Intensivão Django. Este sistema oferece funcionalidades essenciais para o gerenciamento de exames médicos, incluindo o cadastro e login de usuários (clientes) para solicitação de exames, pedidos de exames e o gerenciamento completo para usuários administradores, como secretárias.

## Funcionalidades Principais

- **Cadastro e Login de Usuários (Clientes):** Os clientes podem se cadastrar e fazer login na aplicação para acessar as funcionalidades oferecidas pelo sistema.

- **Solicitação de Exames:** Os clientes podem solicitar exames médicos, fornecendo informações relevantes para a realização dos exames.

- **Gerenciamento de Pedidos de Exames:** Os administradores do sistema, como secretárias, têm a capacidade de gerenciar os pedidos de exames dos clientes, acompanhar o status e fornecer atualizações aos clientes.

- **Cadastro de Tipos de Exames:** Os administradores podem cadastrar diferentes tipos de exames no sistema, facilitando o processo de solicitação e organização.

- **Geração de Senha de Acesso:** Uma funcionalidade importante é a geração de senhas de acesso aos resultados dos exames dos clientes, garantindo a privacidade e a segurança das informações.

## Tecnologias Utilizadas

- **Django:** A aplicação foi desenvolvida utilizando o framework Django, conhecido por sua simplicidade e robustez no desenvolvimento de aplicações web.

- **HTML/CSS:** A interface do usuário foi projetada com HTML e estilizada com CSS para uma experiência agradável e amigável.

- **Banco de Dados:** Utilizamos um banco de dados Mysql para armazenar informações de usuários, pedidos de exames e resultados de exames de forma segura e organizada.

## Como Executar o Projeto

Para executar o projeto localmente, siga os passos abaixo:

### Passo 1: Instalar o Python
Certifique-se de ter o Python instalado em sua máquina. Você pode baixá-lo em python.org e seguir as instruções de instalação apropriadas para o seu sistema operacional.

### Passo 2: Instalar o pip (Gerenciador de Pacotes do Python)
O pip é o gerenciador de pacotes do Python e é usado para instalar bibliotecas e frameworks, incluindo o Django. Instale com o camando: python -m ensurepip --default-pip

### Passo 3: Instalar o Django 
Agora você pode usar o pip para instalar o Django. Execute o seguinte comando: pip install Django


Depois, segue os seguintes passos para rodar o projeto:

   ```bash

    #Clone o repositório na máquina
    https://github.com/saviodev23/VitaLab_PSW.git

    #ao entrar na pasta do projeto, execute os comandos abaixo.
    python -m venv venv
    source venv/bin/activate  
    # No Windows, use venv\Scripts\activate
    
    #migra as classes para o BD 
    python manage.py migrate
    
    #Rode o servidor do projeto
    python manage.py runserver

