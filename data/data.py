import pandas as pd
from os.path import join

data = {
    "text": [
        # Tecnologia (Intenção: assess_technology)
        "Quais ferramentas de TI sua empresa utiliza diariamente?",
        "Vocês usam soluções em nuvem como AWS ou Azure?",
        "Como é feita a gestão de segurança de dados aqui?",
        "A empresa tem estratégia para adoção de inteligência artificial?",
        "Há monitoramento em tempo real dos sistemas de TI?",
        
        # Processos (Intenção: assess_processes)
        "Como são gerenciados os fluxos de trabalho entre departamentos?",
        "Vocês utilizam metodologias ágeis como Scrum ou Kanban?",
        "Existe padronização de processos operacionais?",
        "Como é feita a integração entre sistemas legados e novas plataformas?",
        "Há automação de tarefas repetitivas?",
        
        # Cultura (Intenção: assess_culture)
        "Os colaboradores são incentivados a propor novas ideias?",
        "Há programas de treinamento em competências digitais?",
        "Como a empresa lida com falhas durante inovações?",
        "Existe resistência à mudança na equipe?",
        "Há colaboração entre equipes de TI e negócios?",
        
        # Estratégia (Intenção: assess_strategy)
        "Existe um roadmap claro para transformação digital?",
        "Como os líderes acompanham as métricas de maturidade digital?",
        "Há alinhamento entre a estratégia digital e os objetivos de negócio?",
        "A empresa investe em parcerias com startups de tecnologia?",
        "Vocês realizam benchmarks com concorrentes?",
        
        # Dados (Intenção: assess_data)
        "Como são tomadas decisões baseadas em dados na empresa?",
        "Vocês usam ferramentas de BI como Power BI ou Tableau?",
        "Há uma governança de dados estruturada?",
        "Os dados são integrados em um único repositório?",
        "A empresa realiza análises preditivas?"
    ],
    "intent": [
        "assess_technology", "assess_technology", "assess_technology", "assess_technology", "assess_technology",
        "assess_processes", "assess_processes", "assess_processes", "assess_processes", "assess_processes",
        "assess_culture", "assess_culture", "assess_culture", "assess_culture", "assess_culture",
        "assess_strategy", "assess_strategy", "assess_strategy", "assess_strategy", "assess_strategy",
        "assess_data", "assess_data", "assess_data", "assess_data", "assess_data"
    ],
    "entities": [
        # Tecnologia
        [("ferramentas de TI", "TECNOLOGIA")],
        [("nuvem", "TECNOLOGIA"), ("AWS", "TECNOLOGIA"), ("Azure", "TECNOLOGIA")],
        [("segurança de dados", "TECNOLOGIA")],
        [("inteligência artificial", "TECNOLOGIA")],
        [("monitoramento em tempo real", "TECNOLOGIA")],
        
        # Processos
        [("fluxos de trabalho", "PROCESSO")],
        [("metodologias ágeis", "PROCESSO"), ("Scrum", "PROCESSO"), ("Kanban", "PROCESSO")],
        [("padronização", "PROCESSO")],
        [("sistemas legados", "PROCESSO")],
        [("automação", "PROCESSO")],
        
        # Cultura
        [("propor novas ideias", "CULTURA")],
        [("treinamento", "CULTURA"), ("competências digitais", "CULTURA")],
        [("falhas durante inovações", "CULTURA")],
        [("resistência à mudança", "CULTURA")],
        [("colaboração", "CULTURA")],
        
        # Estratégia
        [("roadmap", "ESTRATÉGIA"), ("transformação digital", "ESTRATÉGIA")],
        [("métricas de maturidade", "ESTRATÉGIA")],
        [("objetivos de negócio", "ESTRATÉGIA")],
        [("parcerias com startups", "ESTRATÉGIA")],
        [("benchmarks", "ESTRATÉGIA")],
        
        # Dados
        [("decisões baseadas em dados", "DADOS")],
        [("Power BI", "DADOS"), ("Tableau", "DADOS")],
        [("governança de dados", "DADOS")],
        [("repositório único", "DADOS")],
        [("análises preditivas", "DADOS")]
    ],
    "maturity_score": [
        # Tecnologia (0-5, onde 5 = máximo)
        3, 4, 2, 1, 4,
        # Processos
        2, 4, 3, 1, 5,
        # Cultura
        3, 2, 4, 1, 3,
        # Estratégia
        2, 3, 4, 5, 2,
        # Dados
        3, 4, 2, 1, 5
    ],
    "category": [
        "technology", "technology", "technology", "technology", "technology",
        "processes", "processes", "processes", "processes", "processes",
        "culture", "culture", "culture", "culture", "culture",
        "strategy", "strategy", "strategy", "strategy", "strategy",
        "data", "data", "data", "data", "data"
    ],
    "metadata": [
        # Exemplo de metadados (opcional)
        {"industry": "manufacturing", "company_size": "large"},
        {"industry": "tech", "company_size": "sme"},
        {"industry": "finance", "company_size": "large"},
        {"industry": "retail", "company_size": "sme"},
        {"industry": "healthcare", "company_size": "medium"},
        # Repetir padrão para outras linhas...
    ]
}

data["metadata"] += [{"industry": None, "company_size": None}] * (len(data["text"]) - len(data["metadata"]))

path = "C:\Projetos\chatbot_with_pln\src\data"

df = pd.DataFrame(data)
df.to_csv(join(path, "digital_maturity_dataset.csv"), index=False)