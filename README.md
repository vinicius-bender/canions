## 🌐 Acesso à Plataforma em Produção

A aplicação está disponível publicamente no seguinte endereço:

🔗 **[https://faunasul.com.br/](https://faunasul.com.br/)**

---

# 🌿 Plataforma de Ciência Cidadã – FaunaSul
Este projeto é uma plataforma web colaborativa desenvolvida como parte do Trabalho de Conclusão de Curso (TCC) do curso de Sistemas de Informação da UFSM. Seu objetivo é permitir que cidadãos contribuam com registros da fauna observada no território do Geoparque Caminhos dos Cânions do Sul.

## 📌 Objetivo

Facilitar a coleta, armazenamento e análise de dados sobre fauna local por meio da ciência cidadã, promovendo o engajamento da comunidade e subsidiando ações de conservação ambiental.

## 🔍 Funcionalidades

- Cadastro de observações com fotos, vídeos e localização geográfica
- Avaliação e validação por especialistas
- Registro de informações taxonômicas (família, gênero, espécie)
- Listagem de espécies e histórico de observações
- Painel administrativo com controle de usuários e dados
- Mecanismo de promoção de usuários para o papel de especialista

## 🧰 Tecnologias Utilizadas

- **Backend**: Python, Django
- **Frontend**: HTML, CSS, JavaScript
- **Banco de Dados**: PostgreSQL
- **Mapas**: OpenStreetMap + Leaflet.js
- **Hospedagem**: Ubuntu VPS com Docker e Nginx (produção)

## 🗺️ Público-Alvo

Cidadãos, turistas, pesquisadores, ambientalistas e gestores do Geoparque Caminhos dos Cânions do Sul.

## 👤 Contas de Teste 

Você pode utilizar as seguintes credenciais para acessar a plataforma com diferentes perfis de usuário (não é necessário criar um usuário para relatar uma observação na plataforma):

| Tipo de Usuário       | Email                          | Senha  |
|-----------------------|--------------------------------|--------|
| Usuário Comum         | usuarioteste@example.com       | 123    |
| Especialista          | usuarioespecialista@example.com| 123    |
| Cientista             | usuariocientista@example.com   | 123    |
| Admin (staff)         | admin@example.com              | admin  |

---

## 🧩 Painel Administrativo Personalizado

Também está disponível um painel administrativo integrado à própria aplicação:

🔗 **[https://faunasul.com.br/painel_administrador](https://faunasul.com.br/painel_administrador)**

Neste painel é possível:
- Cadastrar cadeias taxonômicas (família, gênero, espécie);
- Visualizar e avaliar observações pendentes;
- Promover usuários a papéis como especialista ou cientista.

---

## 🐾 Fluxo da Aplicação

1. O **administrador cadastra as cadeias taxonômicas** no painel.
2. Os **usuários realizam observações**, incluindo arquivos de mídia, localização e descrição.
3. As observações ficam com status **"Pendente"**.
4. O **admin, especialista ou cientista** avalia a observação (aprovando ou rejeitando).
5. Se aprovada, a observação será exibida em:
   - **"Todas Observações"**
   - **"Minhas Observações"** (somente para o autor)
   - **Mapa interativo** na página inicial

Desenvolvido por Vinicius Rodolfo Bender Carlson como parte do TCC do curso de Sistemas de Informação da UFSM (Universidade Federal de Santa Maria).
