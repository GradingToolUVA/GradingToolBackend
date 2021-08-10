from django.shortcuts import render
from .parser import Parser
import urllib.parse
from django.http import JsonResponse
# Create your views here.

# source: https://stackoverflow.com/a/52189270

def current_page_only(request):
    print("---")
    print("---")
    encoded_url = request.GET['encoded_url']
    url = urllib.parse.unquote(encoded_url)
    print(url)
    p = Parser()
    head, header, main = p.parse(url)
    output = str(head) + str(main)
    # print(output)
    # url = urllib.parse.unquote
    res = {"content": [{"html": output}]}
    return JsonResponse(res)
    

def all_linked_pages(request):
    encoded_url = request.GET['encoded_url']
    url = urllib.parse.unquote(encoded_url)
    p = Parser()
    res = {"content": p.parse_all(url)}

    return JsonResponse(res)

def test(request):
    print(request.GET['input'])
    return