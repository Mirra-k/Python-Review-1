import re
import json
import argparse
import sys
import os
import pickle
from collections import defaultdict

class Model:
    
    def __init__(self, n=1):
        """
        :n: n в n-грамме.
        :data: массив словарей(индекс - n-грамма, 
            значение - словарь(ключ - слово, значение - количество его вхождений)
        :__wnc: ключ в словаре для каждого индекса. 
            Его значение - Сумма количеств свсех слов для данного ключа.
        """
        self.n = n + 1 # для создания n-граммы мы берем строку из n+1 слова. n слов для ключа и 1 для значения
        self.data = {}
        self.__wnc = '_total_word_num'
    
    def fit_by_file(self, file_name, lc):
        """
        Построчно считывает файл.
        Создает из строки (1-n)-граммы.
        Создает масив из словарей для n-грамм.
        Для каждой n-граммы подсчитываем какие слова идут после нее, 
        и сколько раз такие словосочетания встречаются.
        :file_name: имя файла, из которого мы берем информацию.
        :lc: флаг, будет ли весь текст в нижнем регистре.
        :word: слово из текста.
        :cur_ngram: наша n-грамма.
        :return: nothing
        """
        cur_ngram = []
        with open(file_name) as file:
            for line in file:
                for word in re.split('[^a-zA-Zа-яА-Я]+', line):
                    if lc:
                        cur_ngram.append(word.lower())
                    else:
                        cur_ngram.append(word)
                    if len(cur_ngram) > self.n: 
                        cur_ngram = cur_ngram[1:] # в предыдущей итерации мы внесли n-грамму в словарь.
                        #на этой мы создаем новую n-грамму из n-1 предыдущего слова и одного нового,
                        #добавленного выше
                        for i in range(self.n - 1):
                            key = tuple(cur_ngram[i:-1])
                            value = cur_ngram[-1]
                            if key not in self.data:
                                self.data[key] = defaultdict(int)
                                self.data[key][self.__wnc] = 0
                            self.data[key][value] += 1
                            self.data[key][self.__wnc] += 1
                            
    def to_file(self, file_name):
        """
        Записывает полученный словарь в файл
        :file_name: имя файла
        :return: nothing
        """
        buffer = dict()
        for key in self.data.keys():
            buffer[key] = self.data[key]
        with open(file_name, 'wb') as file:
            pickle.dump(buffer, file)

if __name__ == "__main__":
    
    

    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", help="path to the directory containing the document collection")
    parser.add_argument("--model", default="model.txt", help="the path to the file to which the model is saved")
    parser.add_argument("--lc", action='store_true', help="Allow the texts to lowercase")

    n = 1
    m = Model(n)
    
    args = parser.parse_args()

    if args.input_dir:
        files = os.listdir(args.input_dir) 
        for i in files:
            m.fit_by_file(args.input_dir + '/' + i, args.lc)
            m.to_file(args.model)
    else:
        file = open('file.stdin', 'w')
        for line in sys.stdin:
            file.write(line + '/n')
        file.close()
        m.fit_by_file('file.stdin', args.lc)
        m.to_file(args.model)
