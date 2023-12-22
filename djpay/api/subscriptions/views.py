from django.http import JsonResponse

# from django.shortcuts import request


def index(request):
    return JsonResponse({"message": "Hi"}, safe=True)
