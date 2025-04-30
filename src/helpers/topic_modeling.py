# # 2. Modelagem de Tópicos (LDA)
#     print("\n🧠 Executando modelagem de tópicos...")
#     id2word = corpora.Dictionary(processed_tokens)
#     corpus = [id2word.doc2bow(text) for text in processed_tokens]
    
#     lda_model = gensim.models.LdaModel(
#         corpus=corpus,
#         id2word=id2word,
#         num_topics=3,
#         random_state=42,
#         passes=15
#     )
    
#     # Cálculo de coerência
#     coherence_model = CoherenceModel(
#         model=lda_model,
#         texts=processed_tokens,
#         dictionary=id2word,
#         coherence='c_v'
#     )