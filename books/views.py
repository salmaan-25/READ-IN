# Create your views here.
import requests
from django.shortcuts import redirect, render
from .models import FavoriteBook
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth import logout

# Search Page
def search_books(request):
    query = request.GET.get('query')
    results = []

    if query:
        res = requests.get(f'https://gutendex.com/books/?search={query}')
        if res.status_code == 200:
            data = res.json()['results']
            for book in data:
                if 'text/html; charset=utf-8' in book['formats']:
                    results.append(book)  # ✅ Only if HTML is available

    return render(request, 'books/search.html', {'results': results, 'query': query})


# Read Book Page
def read_book(request, book_id):
    res = requests.get(f'https://gutendex.com/books/{book_id}')
    book = res.json()
    html_url = None

    # Get HTML version
    for fmt, url in book['formats'].items():
        if fmt == 'text/html; charset=utf-8':
            html_url = url
            break

    if html_url:
        content = requests.get(html_url).text
    else:
        content = "<p>This book is not available in HTML format.</p>"

    return render(request, 'books/read.html', {
        'book': book,
        'content': content
    })

#save book
@login_required
def save_book(request, book_id):
    res = requests.get(f'https://gutendex.com/books/{book_id}')
    data = res.json()

    title = data['title']
    author = data['authors'][0]['name'] if data['authors'] else 'Unknown'
    cover = data['formats'].get('image/jpeg', '')

    FavoriteBook.objects.get_or_create(
        user=request.user,
        book_id=book_id,
        defaults={
            'title': title,
            'author': author,
            'cover_url': cover,
        }
    )

    return redirect('read_book', book_id=book_id)

@login_required
def my_books(request):
    books = FavoriteBook.objects.filter(user=request.user)
    return render(request, 'books/my_books.html', {'books': books})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log the user in after successful signup
            return redirect('search_books')  # redirect to homepage or dashboard
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


def custom_logout(request):
    logout(request)
    return redirect('login')  # or 'search_books' if you prefer

