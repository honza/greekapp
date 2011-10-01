import json
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from bible import Bible


def index(request):
    return render_to_response('base.html', {},
        context_instance=RequestContext(request))


def verse(request, book, chapter, verse):
    bible = Bible()
    verse = bible.get_verse(book, chapter, verse)
    return HttpResponse(json.dumps(verse), mimetype='application/json')
