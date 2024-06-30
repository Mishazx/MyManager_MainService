from django.shortcuts import render


def result_page(request, status, message):
    return render(request, 'result_page.html', {'status': status, 'message': message,})
