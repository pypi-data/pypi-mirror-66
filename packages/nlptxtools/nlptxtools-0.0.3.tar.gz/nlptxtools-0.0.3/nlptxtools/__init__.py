from nltk import word_tokenize
from pymorphy2 import MorphAnalyzer
from multiprocessing import Process, Manager, cpu_count
import pandas as pd


class TxTools:
    def __init__(self, stop_words=[], allowed_punctuation=['.', '-', '?'],
                 restricted_punctuation=[':', ',', ';', '<', '>', '(', ')'], no_lemma=['нем']):
        """
        no_lemma if set excepts list of words from lemmatization process
        """
        self.stop_words = stop_words
        self.allowed_punctuation = allowed_punctuation
        self.restricted_punctuation = restricted_punctuation
        self.no_lemma = no_lemma

    def transform_(self, documents, job_no, transform_results):
        transform_results[job_no] = [self.clean_text(doc) for doc in documents]

    def transform(self, documents, n_jobs=1):
        manager = Manager()
        transform_results = manager.dict()

        if n_jobs == -1:
            n_jobs = cpu_count()

        threads = {}

        n_docs = len(documents)
        if n_docs >= n_jobs:
            # number of elements for every process
            n_elements = int(n_docs / n_jobs)

            for job in range(n_jobs):
                if job == n_jobs-1:
                    doc = documents[n_elements * job:]
                else:
                    doc = documents[n_elements * job:n_elements * (job + 1)]
                thread = Process(target=self.transform_, args=(doc, job, transform_results))
                thread.start()
                threads[job] = thread
        else:
            job = 0
            for doc in documents:
                thread = Process(target=self.transform_, args=(doc, job, transform_results))
                thread.start()
                threads[job] = thread
                job += 1

        # wait for all threads and sum results
        result = []
        for key, value in threads.items():
            value.join()
            result += transform_results[key]

        return result

    def clean_text(self, text):
        """
        Divide text on words. Lemmatize them. Rebuild text
        :return: normalized text
        """
        if pd.isna(text):
            return text

        parts = word_tokenize(text)
        result = ''
        space = ''
        for part in parts:
            # check if it is not allowed char
            if part not in self.restricted_punctuation:
                # if it is punctuation
                if part in self.allowed_punctuation:
                    word = part
                # lemmatize
                else:
                    # получаем лемму
                    _lemma = self.lemma(part)

                    # проверяем ее вхождение в словарь стоп слов
                    if _lemma in self.stop_words:
                        # пропускаем, если слова в стопе
                        word = ''
                    else:
                        word = space + _lemma
                        space = ' '
                result += word

        return result

    def lemma(self, word):
        if word not in self.no_lemma:
            morph = MorphAnalyzer()
            p = morph.parse(word)[0]
            return p.normal_form
        else:
            return word
