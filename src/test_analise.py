from sentence_transformers import SentenceTransformer
from helpers.classification_score_intent import map_score_to_label
from model.comprehensive_evaluator import ComprehensiveEvaluator
from helpers.chatbot_interection import conversation_chatbot, load_resources
from resource.test_data import test_data
from dao import connection_bd
import pandas as pd

from pathlib import Path
base_path = Path(__file__).resolve().parents[2]

# # Inicialize os pipelines (uma vez)
# model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')

def test_chatbot_responses(test_dataset):

    # 2. Inicializar o avaliador
    evaluator = ComprehensiveEvaluator(test_dataset)

    # 3. Executar avaliação automática para todas as perguntas
    auto_results = evaluator.run_automatic_evaluation()

    # 4. Executar avaliação humana para uma amostra (5 respostas com pior desempenho)
    human_results = evaluator.run_human_evaluation(sample_size=5)

    # 5. Gerar e salvar relatório completo
    report_path = evaluator.save_full_report()

    # 6. Analisar resultados
    # print("\nRESUMO DE DESEMPENHO:")
    # print(f"Similaridade Semântica Média: {evaluator.results[0]['summary']['auto_metrics_avg']['cosine_similarity']:.2f}")
    # print(f"Relevância Média (Humana): {evaluator.results[0]['summary']['human_metrics_avg']['relevance']:.2f}/5")

    # print("\nÁREAS QUE PRECISAM DE MELHORIA:")
    # for point in evaluator.results[0]['weak_points']['low_semantic_similarity'][:3]:
    #     print(f"- Pergunta: {point['question']} (Score: {point['score']:.2f})")



if __name__=="__main__":
    test_chatbot_responses(test_data)