from words.models import Word, IrregularVerb
import csv

IrregularVerb.objects.all().delete()

verbs_to_create = list()
with open('../_h/verbs.csv') as file:
    reader = csv.reader(file, quotechar='"')
    for row in reader:
        first_form, second_form, third_form = row
        word = Word.objects.get(eng=first_form)
        i_verb = IrregularVerb(
            first_form=word,
            second_form=second_form,
            third_form=third_form,
        )
        verbs_to_create.append(i_verb)
IrregularVerb.objects.bulk_create(verbs_to_create)
print(IrregularVerb.objects.count())
