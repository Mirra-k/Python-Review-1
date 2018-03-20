import re
import json
import numpy as np

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
        with open(file_name) as file1:
            buffer = json.load(file1)
        self.data = {}
        for key in buffer.keys():
            self.data[tuple(key.split(' '))] = buffer[key]
        self.n = len(list(self.data.keys())[:1])
      
    def _preprocess(self):
        """
        Для каждого значения для n-граммы считает вероятность вхождения слова.
        (нормирует частоты)
        :b: значение __wnc для каждой n-граммы.
        :predata: массив, в котором хранятся слова и вероятность их вхождения для каждой n-граммы.
        :return: nothing
        """
        self.predata = {}
        for ngr in self.data.keys():
            self.predata[ngr] = []
            self.predata[ngr].append(list(self.data[ngr].keys()))
            b = self.data[ngr][self.__wnc]
            self.data[ngr][self.__wnc] = 0
            self.predata[ngr].append(np.array(list(self.data[ngr].values())))
            self.predata[ngr][1] = self.predata[ngr][1] / np.int(b)
        
    
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
        st = word
        cur_ngram = [word]
        self.preprocess()
        for i in range(1, text_len):
            word = self._get_random_after(cur_ngram)
            st += " " + word
            if len(cur_ngram) < self.n - 1:
                cur_ngram.append(word)
            else:
                cur_ngram = cur_ngram[1:]
                cur_ngram.append(word)
            
        return st

n = 1
m = Model(n)
    
parser = argparse.ArgumentParser()
parser.add_argument("--model", help="path to the file from which the model is loaded")
parser.add_argument("--seed", help="The initial word")
parser.add_argument("--length", type=int, help="length of the generated sequence")
parser.add_argument("--output", help="The file to which the result will be written")

args = parser.parse_args()

m.load(args.output)

if args.output:
    open(file_name, 'w').write(json.dumps(getText(args.seed), args.length)) 
else:
    print(getText(args.seed), args.length)
