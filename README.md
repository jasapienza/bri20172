# bri20172

# Trabalho final da cadeira de BRI 2017 2 - Prof. Xexéo
# Aluno José Augusto Sapienza Ramos

Para rodar o código, coloque o conteúdo da pasta "data" na mesma pasta dos arquivos .py
A ordem que os arquivos .py devem ser rodados e suas respectivas funções:
1) cleanRAWUrls.py :: processa o arquivo rawurls.txt com as URLS aleatórias fornecidas pelo site URoulette e gera o arquivo urls_non_source.csv.
2) getURLContents.py :: processa os arquivos urls_non_source.csv and urls_source.csv para pegar os conteúdos dos documentos na web e gera o arquivo urlContent.xml.
3) generateBOWs.py :: processa o arquivo urlContent.xml, faz todo o processo para gerar as bag of words de treino e de teste do SVM. Salva nos arquivos BOW_test.xml e BOW_training.xml.
4) analyzingBOW.py :: processa os xmls gerados no passo anterior para construir a matriz de termo documento e outros dados acessórios. Salva os resultados nos arquivos: freq_in_docs.csv, freq_terms_in_corpus.csv, vector_sum_cols_term_doc.csv e matrix_term_doc.csv.
5) SVM.py :: processa todos os arquivos gerados no passo anterior, treina e testa o SVM. O resultado de acurácia e outras estatísticas são impressos na tela.
