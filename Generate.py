import re
import argparse
import numpy as np
import random
import pickle

class Model:
    
    def __init__(self, n=1):
        """
        :n: n в n-грамме.
        :data: массив словарей(индекс - n-грамма, 
            значение - словарь(ключ - слово, значение - количество его вхождений)
        :__wnc: ключ в словаре для каждого индекса. 
            Его значение - Сумма количеств свсех слов для данного ключа.
        """
        self.n = n + 1
        self.data = {}
        self.__wnc = '_total_word_num'
        
    def load(self, file_name):
        """
        Загружает массив словарей из текста в data.
        :file_name: имя файла, из которого мы берем информацию.
        :return: nothing
        """
        with open(file_name, 'rb') as file1:
            buffer = pickle.load(file1)
        self.data = {}
        for key in buffer.keys():
            self.data[tuple(key.split(' '))] = buffer[key]
        self.n = len(list(self.data.keys())[:1])
      
    def _preprocess(self):
        """
        Для каждого значения для n-граммы считает вероятность вхождения слова.
        (нормирует частоты)
        :summa: значение __wnc для каждой n-граммы.
        :predata: массив, в котором хранятся слова и вероятность их вхождения для каждой n-граммы.
                    в одной куче, потому что это удобно для np.random.choice
        :return: nothing
        """
        self.predata = {}
        for ngramm, ngramm_value in self.data.items():
            self.predata[ngramm] = []
            self.predata[ngramm].append(list(ngramm_value.keys()))#добовляем список слов
            summa = ngramm_value[self.__wnc]# запоминаем общую сумму для н-граммы
            ngramm_value[self.__wnc] = 0# обнуляем общую сумму, чтобы она не мешала рассчету вероятностей
            self.predata[ngramm].append(np.array(list(ngramm_value.values())))#добовляем список количества вхождений
            self.predata[ngramm][1] = self.predata[ngramm][1] / np.int(summa) #в 1 лежали количества вхождений слова
            # и мы их поделили на общую сумму вхождений слов. Получили список вероятностей
        
    
    def _get_random_after(self, ngr):
        """
        С помощью np.random.choice выдает случайное слово.
        :ngr: n-грамма, для которой мы ищем следующее слово.
        :return: слово для заданной n-граммы. 
        """
        return np.random.choice(self.predata[tuple(ngr)][0], p=self.predata[tuple(ngr)][1])
            
    def getText(self, word, text_len):
        """
        По заданному слову генерирует последовательность заданной длины.
        :word: начальное слово.
        :text_len: длина последовательности.
        :st: Необходимая последовательность
        :cur_ngram: n-грамма, по которой ищем следующее слово.
        :return: последовательность заданной длины. 
        """
        string = word
        cur_ngram = [word]
        self._preprocess()
        for i in range(1, text_len):
            word = self._get_random_after(cur_ngram)
            string += " " + word
            if len(cur_ngram) < self.n - 1:
                cur_ngram.append(word)
            else:
                cur_ngram = cur_ngram[1:]
                cur_ngram.append(word)
            
        return string
    
    def getRandomWord(self):
        return random.choice(data.values().keys)

    
if __name__ == "__main__":
    n = 1
    m = Model(n)

    parser = argparse.ArgumentParser()
    parser.add_argument("--model", help="path to the file from which the model is loaded")
    parser.add_argument("--seed", help="The initial word")
    parser.add_argument("--length", type=int, default=1 ,help="length of the generated sequence")
    parser.add_argument("--output", help="The file to which the result will be written")

    args = parser.parse_args()

    m.load(args.output)

    if args.seed:
        word = getText(args.seed)
    else:
        word = m.getRandomWord

    if args.output:
        open(file_name, 'w').write(json.dumps(word, args.length)) 
    else:
        print(word, args.length)
