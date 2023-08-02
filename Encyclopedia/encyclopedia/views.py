from django.shortcuts import render, redirect
from random import randint
from . import util
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, title):
    if util.get_entry(title):
        return render(request, "encyclopedia/search.html", {
            "entry": markdown2.markdown(util.get_entry(title)),
            "title": title
        })
    else:
        memory = util.list_entries()
        entries = []
        for entry in memory:
            if title.lower() in entry.lower():
                entries.append(entry)
        return render(request, "encyclopedia/noEntry.html", {
                      "title": title,
                      "entries": entries
        })


def search(request):
    query = request.GET.get('q', '')
    if util.get_entry(query):
        return render(request, "encyclopedia/search.html", {
            "entry": markdown2.markdown(util.get_entry(query)),
            "title": query
        })
    else:
        memory = util.list_entries()
        entries = []
        for entry in memory:
            if query.lower() in entry.lower():
                entries.append(entry)
        return render(request, "encyclopedia/noEntry.html", {
            "title": query,
            "entries": entries
        })

def random(request):
    entries = util.list_entries()
    random_entry = entries[randint(0, len(entries) - 1)]
    return redirect('wiki', title=random_entry)

def add(request):
    if request.method == 'GET':
        return render(request, "encyclopedia/add.html")
    else:
        title = request.POST.get('title')
        text = request.POST.get('markdown')
        entries = util.list_entries()
        for entry in entries:
            if title.lower() == entry.lower():
                return render(request, "encyclopedia/exists.html")

        util.save_entry(title, text)
        return redirect('wiki', title=title)

def edit(request):
    if request.method == 'GET':
        return render(request, "encyclopedia/edit.html", {
            "title": request.GET.get('title'),
            "markdown": util.get_entry(request.GET.get('title'))
        })
    else:
        text = request.POST.get('markdown')
        title = request.POST.get('title')
        entries = util.list_entries()
        for entry in entries:
            if title == entry:
                util.save_entry(title, text)
                return redirect('wiki', title=title)
        return redirect('wiki', title=title)