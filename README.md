# **README – Chatbot: TransformMind**

## **1. TransformMind**

Um chatbot inteligente para responder dúvidas sobre transformação digital, maturidade digital, tecnologias emergentes e estratégias organizacionais.

---

## **2. Descrição Geral**
 
### O que?

A transformação digital tornou-se um fator determinante para a competitividade e inovação nas organizações. No entanto, avaliar o nível de maturidade digital de uma empresa ainda é um desafio complexo, que requer a análise de múltiplos fatores, como cultura organizacional, adoção de tecnologia, processos e estratégias.

Este projeto propõe o desenvolvimento de um chatbot para interagir com usuários e avaliar o nível de maturidade digital de suas organizações com base em parâmetros estruturados previamente definidos por meio de pesquisa.


### Por que?

Atualmente, a avaliação da maturidade digital é feita por diagnósticos manuais, consultorias especializadas ou questionários extensos, sendo processos custosos, demorados e subjetivos. Muitas organizações não possuem recursos ou conhecimento suficiente para realizar uma autoavaliação eficaz. Um chatbot automatiza essa tarefa, oferecendo:

 - Experiência interativa e acessível
 - Autoavaliação rápida
 - Resultados baseados em dados e ontologias validadas

### Como?

O chatbot utiliza técnicas de Processamento de Linguagem Natural (PLN), incluindo:

NLU (Natural Language Understanding) para compreensão do usuário

NLG (Natural Language Generation) para gerar respostas naturais

Seu modelo de aprendizado é treinado aplicando Machine Learning e redes neurais para melhorar a precisão da classificação.

### Objetivo 

Usar as tecnicas e ferramentas de Processamento de Linguagem Natural (PLN) para desenvolver um chatbot com o intuito de avaliar a maturidade digital dentro das organizações, por meio de interações com usuários. Avaliando o nivel de maturidade digital por meio de parametros estruturados, pois, o contexto de Transformação digital se tornou determinante para a inovação e competitividade das organizações requerindo um analise de fatores, como *cultura organizacional*, *adoção de tecnologia*, *processos* e *estratégias*. Com isso, podemos proporcionar às organizações  uma ferramenta para avaliação da maturidade digital, auxiliando na identificação de lacunas e formulação de estrategias de transformação digital.

---

## 🔧 **3. Funcionalidades**

Principais funcionalidades implementadas:

* Responder perguntas sobre transformação digital
* Classificação de intents (ex: customer experience, processos, cultura)
* Extração de entidades relevantes
* Geração de respostas contextualizadas
* Rephrase de perguntas para treinamento contínuo

---

## 🏗️ **4. Estrutura do Projeto**

Organização dos arquivos e pastas:

```
/chatbot_transformacao_digital
│
├── data/                               # Bases de conhecimento e datasets
├── documents/                      # Documentos brutos (PDFs, artigos, relatórios)
├── input/                          # Arquivos de entrada para processamento
├── output/                         # Resultados processados e datasets finais
│
├── model_train/                        # Diretório de modelos treinados organizados
│   ├── model_train_category/
│   │   └── versions/                   # Versões de modelos de classificação de categoria
│   ├── model_train_intent/
│   │   └── versions/                   # Versões de modelos de classificação de intents
│   └── model_train_maturity_score/
│       └── versions/                   # Versões de modelos de maturidade digital
│
├── image/                              # Imagens geradas, plots de treinamento e resultados
│   ├── model_train_category/
│   │   └── versions/                   # Gráficos do treinamento do modelo de categoria
│   ├── model_train_intent/
│   │   └── versions/                   # Gráficos do treinamento do modelo de intents
│   └── model_train_maturity_score/
│       └── versions/                   # Gráficos do treinamento do modelo de maturidade digital
│
├── log/                                # Logs de execução e treinamentos
│
├── src/                                # Código-fonte principal
│   ├── dao/                            # Data Access Objects (interfaces com banco de dados)
│   ├── helpers/                        # Funções utilitárias gerais para o projeto
│   ├── model/                          # Scripts de treinamento e avaliação de modelos
│   ├── resource/                       # Arquivos de configuração, dicionários, mappings
│   ├── utils/                          # Funções utilitárias específicas (ex: logs, formatação)
│   ├── main.py                        # Script principal para execução geral do projeto (como extração de dados, treinamento dos modelos e teste das interações com os modelos)
│   └── main_chatbot.py                # Script principal com a interface gráfica do chatbot (integrado o o streamlit)
│
├── requirements.txt                   # Dependências do projeto
├── README.md                          # Documentação geral
└── LICENSE                            # Licença de uso

```

---

## 🧠 **5. Tecnologias e Ferramentas**

As principais tecnologias utilizadas:

* **Linguagem:** Python 3.9.13
* **Bibliotecas:**
---

1. ### **Pacotes de NLP e Transformers**

   * `accelerate==1.4.0`
   * `transformers==4.41.0`
   * `sentence-transformers==3.4.1`
   * `sentencepiece==0.2.0`
   * `keybert==0.9.0`
   * `deep-translator==1.11.4`
   * `langid==1.1.6`
   * `langcodes==3.5.0`
   * `huggingface-hub==0.29.1`
   * `datasets==3.3.2`

2. ### **Spacy e modelos**

   * `spacy==3.8.7`
   * `en-core-web-sm`
     [Baixar modelo](https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl)
   * `pt-core-news-sm`
     [Baixar modelo](https://github.com/explosion/spacy-models/releases/download/pt_core_news_sm-3.8.0/pt_core_news_sm-3.8.0-py3-none-any.whl)
   * `spacy-legacy==3.0.12`
   * `spacy-loggers==1.0.5`

3. ### **Pré-processamento e NLP Clássico**

   * `nltk==3.9.1`
   * `regex==2024.11.6`

4. ### **Machine Learning**

   * `scikit-learn==1.6.1`
   * `scipy==1.10.1`
   * `joblib==1.4.2`
   * `torch==2.3.0`

5. ### **Visualização de Dados**

   * `matplotlib==3.9.4`
   * `matplotlib-inline==0.1.7`
   * `seaborn==0.13.2`
   * `plotly==5.22.0`
   * `pyLDAvis==3.4.1`

6. ### **Manipulação de Dados**

   * `numpy==1.26.4`
   * `pandas==2.2.3`

7. ### **Streamlit e Utilitários Web**

   * `streamlit==1.36.0`
   * `python-dotenv==1.0.1`

8. ### **Outros Utilitários**

   * `decorator==5.2.1`
   * `python-json-logger==3.2.1`
   * `python-dateutil==2.9.0.post0`
   * `pytz==2025.1`
   * `pyparsing==3.2.3`
   * `PyPDF2==3.0.1`
   * `pymongo==4.13.0`
   * `language_data==1.3.0`

---

* **Modelos:**

    * `Vamsi/T5_Paraphrase_Paws`
    * `google/flan-t5-base`
    * `paraphrase-mpnet-base-v2`
    * `all-MiniLM-L6-v2`
    * `BERT`

* **Outros:** Git e VSCode.

---

## 🚀 **6. Como Executar o Projeto**

Passo a passo para execução local:

1. Clone o repositório

   ```bash
   git clone https://github.com/CharlesVilela/project_pnl.git
   cd chatbot_transformacao_digital
   ```
2. Crie um ambiente virtual

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```
3. Instale as dependências

   ```bash
   pip install -r requirements.txt
   ```
4. Execute a aplicação

   ```bash
   streamlit run src/app.py
   ```

---

## 🧪 **7. Exemplos de Uso**

Exemplos reais de interação:

> **Usuário:** O que é transformação digital?<br>
> **Chatbot:** Transformação digital é a integração de tecnologias digitais em todas as áreas de um negócio, mudando fundamentalmente como você opera e entrega valor aos clientes...

---

## ☁ **8. O armazenamento**
Para o armazenamento dos dados foi utilizado o banco de dados **MongoDB Atlas**. Por conta:

  1. **Escalabilidade e Flexibilidade:**
    MongoDB Atlas oferece escalabilidade horizontal automática, permitindo o armazenamento de grandes volumes de dados não estruturados ou semiestruturados sem restrições rigidas de esquema

  2. **Modelo de dados Natural para documentos NLP:**
    Utiliza o formato JSON-like (BSON), que se adapta a documentos de conhecimento, resultados de inferências, classificações de intents e entities, eliminando a necessidade de múltiplas tabelas relacionais complexas.

  3. **Fácil integração com aplicações Python:**
    Com bibliotecas como pymongo e conectores nativos, a integração com o pipeline de processamento de linguagem natural é direta, permitindo armazenar e consultar resultados de forma rápida.
  4. **Disponibilidade Multi-Cloud:**
    Permite deploy em diferentes provedores e regiões, aumentando a flexibilidade e aderência a estratégias corporativas multicloud.

O banco de dados se divide em dois tipos de dados: o primeiro utilizado para o treinamento do modelo e consulta do contexto para a geração de resposta do chatbot; e o segundo que armazena um cache de interações dos usuários que é utilizado para otimizar o tempo de resposta do chatbot.

### 💾 **1. Dataset - Treinamento do modelo**

Como não foi encontrada uma base pública pronta, foi criada uma **base de dados própria** utilizando:

### 🔎 **Fontes**

1. **Artigos acadêmicos**

   * *Exemplo:* **Digital transformation: What we have learned (thus far) and what is next** – Consensus

---

### 🌐 **Sites consultados**

* [Google Academico](https://scholar.google.com/?hl=pt-BR)
* [Consensus](https://consensus.app/search/)

---

#### 🗃️ **Estrutura da base de dados**

| **Campo**        | **Descrição**                                                    |
| ---------------- | ---------------------------------------------------------------- |
| `text`           | Pergunta, afirmação ou trecho relevante extraído                 |
| `intent`         | Intenção comunicativa do texto                                   |
| `maturity_score` | Grau de maturidade digital (0 a 1)                               |
| `entities`       | Lista de entidades nomeadas (ex: organizações, pessoas, locais)  |
| `category`       | Classificação geral (ex: arquitetura organizacional, estratégia) |
| `metadata`       | Informações adicionais (fonte, data, autor, etc)                 |


### 🔄 **2. Dataset - Cache das interações**

O objetivo da utilização do cache de interações é otimizar o tempo de resposta levado para o chatbot consegui retornar uma resposta para o usuário.

#### **Estrutura do Cache de Interações**

| **Campo**        | **Descrição**                                                    |
| ---------------- | ---------------------------------------------------------------- |
| `user_input`           | Pergunta do usuário                |
| `response`         | Resposta gerada pelo chabot                                    |
| `userid` | Identificador da sessão, ou seja, para cada sessão iniciada é gerado um uuid daquela sessão                                |
| `timeresponse`       | Tempo que o chatbot leva para gerar uma resposta  |
| `datetime`       | Data e hora da interação |
| `isQuestionAudio`       | Indica se a pergunta do usuário foi em audio                |
| `isResponseAudio`       | Indica se a resposta do chatbot foi em audio                |


---

## 📊 **9. Metodologia**

- A base de dados foi criada manualmente por meio de artigos baseados em Maturidade digital. Com isso, o sistema conta com uma base de conhecimento fundamental em maturidade digital, que foi aprimorado com tecnicas de aprendizado de maquina (ML) e redes neurais para melhorar a classificação do modelo.
  
- Utilizado para o desenvolvimento desse chatbot:
  - Natural Lanaguage Undestanding - (NLU)
  - Natural Language Generation - (NLG) 

 Abordagem explicada:

* Pré-processamento (tokenização, stopwords)
* Vetorização ou embeddings utilizados
* Algoritmos de classificação ou geração de texto
* Métricas de avaliação e resultados

---

## 👥 **10. Contribuidores**

Os membros do projeto:

* **Charles Vilela** – [GitHub](https://github.com/charlesvilela) | [LinkedIn](https://linkedin.com/in/charlesvilela)
* **Gabriel Lima** – [GitHub](https://github.com/Gabs19) | [LinkedIn](https://www.linkedin.com/in/gabriel-lima-861181168/)

---

## 💡 **11. Futuras Implementações**

Melhorias ou próximos passos:

* Treinar modelos maiores para geração de resposta
* Deploy em nuvem (AWS, GCP)
* Melhorar integração com plataformas de atendimento ao cliente
* Dashboard de analytics de interação

---

