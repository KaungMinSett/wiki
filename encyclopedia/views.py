from django.shortcuts import render

from . import util
import random
from django.core.files.storage import default_storage
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        
    })

def show_entry(request, title):
    # return error if no title exists
    if util.get_entry(title) == None:
        return render(request, "encyclopedia/error.html", {
            "title": title
        })
    else:
        return render(request, "encyclopedia/entry.html", {
        'content': util.covert_to_html(title),
        'title': title

    })

def search(request):
    entries =[] # list to store the search results
    if request.method == 'POST':
      
        q = request.POST.get('q').lower() # get the search query in lower
        if util.get_entry(q) == None:  # if no such title exists then search for the query in the content
            for entry in util.list_entries(): # loop through all the entries
                content = util.covert_to_html(entry) # convert the entry to html
                if q in content.lower(): # if query is in the content in lower case then append the entry to the search result list
                    entries.append(entry)
            return render(request, "encyclopedia/search_result.html", {"entries": entries}) # pass search result list to template
        else:
            return render(request, "encyclopedia/entry.html", { # if title exists then return the entry
            'content': util.covert_to_html(q),
            'title': q

    })


    

def create_page(request):
    if request.method == 'POST':
        title = request.POST.get('title')
       
        content = request.POST.get('content')
        if util.get_entry(title) == None and title.strip()!='' or not title: # not such title exists then save the entry
            util.save_entry(title, content)
            return render(request, "encyclopedia/entry.html", {
            'content': util.covert_to_html(title),
            'title': title
        })
        else:
            return render(request, "encyclopedia/new_page.html",{ #if title exists then return error message
                "message": "Title already exists, or title can't be blank."
            })
    else:
        return render(request, "encyclopedia/new_page.html")

def edit_page(request, title):
    if request.method == 'POST':
        content = request.POST.get('content')
        title = request.POST.get('title')
        util.save_entry(title, content)

        return render(request, "encyclopedia/entry.html", {
            'content': util.covert_to_html(title),
            'title': title
        })
    else:
         f = default_storage.open(f"entries/{title}.md")
         f = f.read().decode("utf-8")

         return render(request, "encyclopedia/edit_page.html", {

            'content': f,
            'title': title
        
        })

def get_random(request):
   
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return render(request, "encyclopedia/entry.html", {
        'content': util.covert_to_html(random_entry),
        'title': random_entry
    })