from words.models import Word
import csv
Word.objects.all().delete()
words_to_create = list()
with open('../_h/clean.csv') as file:
    csv_reader = csv.reader(file)
    for i, row in enumerate(csv_reader):
        number_in_dict, eng, ru = row
        new_number_in_dict = i + 1
        # print(new_number_in_dict,number_in_dict, eng, ru)
        word = Word(number_in_dict=new_number_in_dict, ru=ru, eng=eng)
        words_to_create.append(word)

Word.objects.bulk_create(words_to_create)
print(Word.objects.count())
