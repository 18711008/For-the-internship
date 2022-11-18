# -*- coding: utf-8 -*-

import jieba
from gensim import models, corpora
import numpy as np
import pandas as pd

content = None
stopwords = None
with open('E:\实验\lda', 'r', encoding='utf-8') as f:
    content = f.readlines()
content = list(map(lambda x: x.strip(), content))
with open('E:\实验\lda') as f:
    stopwords = f.readlines()
stopwords.append('')
stopwords.append(' ')
stopwords.append('\n')
  
texts = [[word for word in jieba.cut(document, cut_all=False) if word not in stopwords] for document in content]
dictionary=corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

lda = models.ldamodel.LdaModel(corpus, id2word=dictionary,num_topics=10,minimum_probability=0)
topic_words = lda.print_topics(-1)
topic_str = [y[1] for y in topic_words]
topics = np.array(list(map(lambda x: x.split(' + '), topic_str)))
df1 = pd.DataFrame(topics)

topic_doc = list(map(lambda x: lda.get_document_topics(x), corpus))
topic_matrix = np.array(list(map(lambda x: [y[1] for y in x], topic_doc)))
df2 = pd.DataFrame(topic_matrix)

writer = pd.ExcelWriter('E:\实验\lda\outcomes.xlsx')
df1.to_excel(writer, '文档主题词')
df2.to_excel(writer, '文档主题分布')
writer.save()