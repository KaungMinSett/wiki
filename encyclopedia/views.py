from django.shortcuts import render

from . import util
import markdown2

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
        'content': util.covert_to_html(title)

    })

def search(request):
    entries =[]
    if request.method == 'POST':
      
        q = request.POST.get('q')
        if util.get_entry(q) == None:
            for entry in util.list_entries():
                content = util.covert_to_html(entry)
                if q in content:
                    entries.append(entry)
            return render(request, "encyclopedia/search_result.html", {"entries": entries})
        else:
            return render(request, "encyclopedia/entry.html", {
            'content': util.covert_to_html(q)

    })


    

def create_page(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if util.get_entry(title) == None:
            util.save_entry(title, content)
            return render(request, "encyclopedia/entry.html", {
            'content': util.covert_to_html(title)
        })
        else:
            return render(request, "encyclopedia/new_page.html",{
                "message": "Title already exists, Please change the title."
            })
    else:
        return render(request, "encyclopedia/new_page.html")
