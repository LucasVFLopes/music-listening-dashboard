# 🎧 Music Listening Dashboard

Dashboard interativo para explorar padrões de escuta musical ao longo do tempo, construído a partir do histórico pessoal do Last.fm e enriquecido com classificação semântica de artistas utilizando Large Language Models (LLMs).

🔗 **Aplicação online:**  
👉 https://music-listening-dashboard.streamlit.app

---

## 📌 Objetivo do projeto

Este projeto nasceu inicialmente como uma exploração pessoal de dados, com o objetivo de:

- trabalhar com dados reais de consumo musical
- aprender a coletar dados via APIs
- estruturar um pipeline simples de dados
- transformar dados brutos em visualizações interativas

Ao longo do desenvolvimento, o projeto evoluiu para um **dashboard completo**, com foco em **análise comportamental**, priorizando clareza, interatividade e decisões metodológicas explícitas.

---

## 🧠 O que é analisado

A partir do histórico de scrobbles do Last.fm (2023 em diante), o dashboard permite explorar:

- 🎵 Total de scrobbles em qualquer período
- 🎤 Artistas, álbuns e músicas mais escutados
- 🎶 Fluxo temporal de gêneros, moods e energia (streamgraph)
- 🕒 Heatmaps de escuta por hora e dia da semana
- ⚡ Energia dominante por período
- 🌈 Mood predominante por período

Todas as visualizações são **interativas**, com filtros por:

- intervalo de datas
- atalhos rápidos por ano
- gênero musical

---

## 🔍 Metodologia e decisões de projeto

Este projeto não teve como objetivo apenas visualizar dados, mas também **tomar decisões conscientes ao longo do pipeline**, equilibrando fidelidade dos dados, custo computacional e valor analítico.

As principais escolhas metodológicas estão descritas abaixo.

---

## 📊 Definição do dataset

O histórico completo de escuta contém mais de **50 mil scrobbles**, distribuídos ao longo de milhares de artistas diferentes.

Para tornar o projeto viável e analiticamente mais consistente, foi adotada uma abordagem baseada no **princípio de Pareto (80/20)**:

- Foram selecionados os **1.000 artistas mais escutados**
- Esse grupo representa aproximadamente **85% de todos os scrobbles**
- Os demais artistas aparecem de forma muito esparsa, com baixo impacto estatístico

Esse recorte permitiu:

- reduzir ruído
- melhorar a qualidade da classificação
- controlar custos computacionais
- manter alta representatividade do comportamento musical real

---

## 🧠 Classificação semântica com LLMs

Uma das etapas centrais do projeto foi o **enriquecimento semântico** do dataset, atribuindo a cada artista:

- macro gênero musical
- subgênero
- mood predominante
- nível de energia

Em vez de utilizar bases fixas ou tags inconsistentes, foi adotada uma abordagem baseada em **Large Language Models (LLMs)**.

### Por que usar LLMs?

- Tags musicais tradicionais são altamente inconsistentes
- O mesmo artista pode receber dezenas de rótulos conflitantes
- APIs públicas raramente oferecem uma taxonomia estável

O uso de LLMs permitiu:

- padronizar classificações
- controlar o vocabulário
- incorporar contexto musical
- manter consistência entre artistas

---

## 🎯 Estratégia de classificação (nível de artista)

A classificação foi realizada **no nível do artista**, e não da faixa individual.

Essa decisão envolve um trade-off consciente:

- ❌ perda de fidelidade em músicas atípicas
- ✅ maior coerência global
- ✅ redução drástica no volume de chamadas à API
- ✅ melhor alinhamento com padrões reais de escuta

Na prática, artistas tendem a manter uma identidade musical consistente ao longo do tempo, tornando essa abordagem adequada para análises comportamentais.

---

## ⚙️ Enriquecimento e engenharia de atributos

Além da classificação semântica, o dataset passou por etapas adicionais de enriquecimento:

- normalização de nomes de artistas e faixas
- ajuste de timezone para horário local
- extração de:
  - hora do dia
  - dia da semana
  - mês e ano
- consolidação em um dataset final otimizado para visualização

O resultado é um dataset pronto para análises temporais e comportamentais, utilizado diretamente pelo dashboard.

---
## 🧱 Estrutura do projeto

```text
music-listening-dashboard/
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── raw/              # dados brutos (Last.fm)
│   └── processed/        # dados tratados e enriquecidos
│
├── notebooks/
│   ├── Lastfmdataset.ipynb         # coleta via API
│   └── 02_scrobbles_enriched.ipynb # limpeza e enriquecimento
│
└── scripts/
    ├── classify_artists.py         # classificação via IA
    └── test_openai.py
```

---

## 🛠️ Tecnologias utilizadas

- Python
- Pandas — tratamento e agregação de dados
- Streamlit — dashboard interativo
- Plotly — visualizações
- Last.fm API — coleta de dados
- OpenAI API — classificação semântica de artistas
- Git & GitHub — versionamento
- Streamlit Cloud — hospedagem

---

## ⚖️ Limitações conhecidas

Algumas limitações são reconhecidas e fazem parte do escopo atual do projeto:

- Classificação por artista não captura variações entre faixas
- Mood e energia são categorias discretas
- Não há métricas acústicas (BPM, valence, danceability)

Essas limitações foram consideradas aceitáveis dado o objetivo do projeto e abrem espaço para evoluções futuras.

---

## 🚀 Possíveis evoluções

- Integração com Spotify API para métricas acústicas
- Classificação em nível de faixa
- Modelagem contínua de energia (ex: BPM)
- Comparação entre períodos (antes/depois)
- Geração automática de insights textuais

---

## 👤 Autor

Projeto desenvolvido por Lucas Lopes, como exploração pessoal com foco em dados, visualização e tomada de decisão metodológica.

🔗 GitHub: https://github.com/LucasVFLopes

🔗 LinkedIn: https://www.linkedin.com/in/lucasvflopes/
