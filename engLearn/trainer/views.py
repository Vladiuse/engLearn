from django.shortcuts import render


def trainer_cards(request):
    content = {

    }
    return render(request, 'trainer/trainer_cards.html', content)
