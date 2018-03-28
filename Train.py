import re
import json
import argparse
import sys
import os

class Model:
    
    def __init__(self, n=1):
        """
        :n: n в n-грамме.
        :data: массив словарей(индекс - n-грамма, 
            значение - словарь(ключ - слово, значение - количество его вхождений)
        :__wnc: ключ в словаре для каждого индекса. 
            Его значение - Сумма количеств свсех слов для данного ключа.
        """
        self.n = n + 1  # тут лучше объяснить почему + 1
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
                    if len(cur_ngram) < self.n:  # вот отсюда и ниже избыточный и не очень понятный код
                        # давай избавимся от повторяющихся строк кода, от лишних if/else конструкций 
                        # и сделаем это все чуть читабельнее
                        if lc:  # вот эта штука повторяется, да и написана не самым красивым образом 
                            cur_ngram.append(word.lower())
                        else:
                            cur_ngram.append(word)
                        continue  # вот это мне совсем не нравится
                    else:
                        cur_ngram = cur_ngram[1:]  # а куда тут девается самое первое слово из строки? зачем его выкидывать?
                        if lc:
                            cur_ngram.append(word.lower())
                        else:
                            cur_ngram.append(word)
                    for i in range(self.n - 1):  
                        key = tuple(cur_ngram[i:-1])  
                        value = cur_ngram[-1]
                        if key not in self.data.keys():  # тут во-первых можно (и нужно) не вызывать keys(), а просто 
                            # if key not in self.data, потому что в твоем случае он перебирает весь массив ключей за O(n)
                            # а в моем ищет по хэшу за O(1)
                            # а во-вторых, используя defaultdict можно убрать эти строчки отсюда
                            self.data[key] = dict() 
                            self.data[key][self.__wnc] = 0
                        if value not in self.data[key]: 
                            self.data[key][value] = 0
                        # и до сюда
                        # используй это
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
            buffer[" ".join(list(key))] = self.data[key]
        open(file_name, 'w').write(json.dumps(buffer))

        
# весь код отсюда и ниже в функцию main, которая будет вызывать при условии 
# if __name__ == "__main__":
# погугли что это такое

n = 1  # это в аргументы надо добавить
m = Model(n)

parser = argparse.ArgumentParser()
parser.add_argument("--input-dir", help="path to the directory containing the document collection")
parser.add_argument("--model", help="the path to the file to which the model is saved")
parser.add_argument("--lc", action='store_true', help="Allow the texts to lowercase")

args = parser.parse_args()

if args.input_dir:
    files = os.listdir(args.input_dir) 
    for i in files:
        m.fit_by_file(namespace.input_dir + '/' + i, args.lc)
        m.to_file(args.model)
else:
    file = open('file.stdin', 'w')
    for line in sys.stdin:
        file.write(line + '/n')
    file.close()
    m.fit_by_file('file.stdin', args.lc)
    m.to_file(args.model)
