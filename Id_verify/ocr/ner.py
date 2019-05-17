import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()
doc = nlp('C.K.G. HIGH SCHOOL (CBSE AFFILIATED) Gnvali. Ta. Jhagadia. Dist. Bharuch. %%§ Ph. : 02645-227623 0 Email : ckgschool@yahoo.com "WWW" Name: Kishan H. Vadav Class: IV 0.0.8.: 13-08-2001 Address: Sultanpura. Jhagadia Dist. Bharuch P-e‘xtrgﬁ Ph.: Moh.: 9427145671 Principal')
print([(X.text, X.label_) for X in doc.ents])
