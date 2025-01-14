'''
Views that provide information about collection of books. Usually this is 
a catalog of books of particular genre.
'''

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator, Page

from books.templatetags.books_extras import to_human_language
from books.models import LinkType, Tag, Language

from .utils import maybe_filter_links, active_books

TAGS_TO_SHOW_ON_MAIN_PAGE = [
    'Сучасная проза',
    'Класікі беларускай літаратуры',
    'Дзецям і падлеткам',
]

BOOKS_PER_PAGE = 16


def index(request: HttpRequest) -> HttpResponse:
    '''Index page, starting page'''
    # Getting all Tags and creating querystring objects for each to pass to template
    tags_to_render = []
    books = active_books()
    for tag in Tag.objects.filter(name__in=TAGS_TO_SHOW_ON_MAIN_PAGE):
        tags_to_render.append({
            'name':
            tag.name,
            'slug':
            tag.slug,
            'books':
            books.filter(tag=tag.id).order_by('-date'),
        })

    context = {
        'promo_books': books.filter(promoted=True),
        'recently_added_books': books.order_by('-date')[:6],
        'tags_to_render': tags_to_render,
    }

    return render(request, 'books/index.html', context)


def get_query_params_without(request: HttpRequest, param: str) -> str:
    '''Returns query string without given param'''
    params = request.GET.copy()
    if param in params:
        params.pop(param)
    if len(params) == 0:
        return ''
    return '?' + params.urlencode()


def catalog(request: HttpRequest, tag_slug: str = '') -> HttpResponse:
    '''Catalog page for specific tag or all books'''

    page = request.GET.get('page')
    tags = Tag.objects.all()
    filtered_books = maybe_filter_links(active_books(), request).distinct()

    tag = None
    if tag_slug:
        # get selected tag id
        tag = tags.filter(slug=tag_slug).first()
        # pagination for the books by tag
        filtered_books = filtered_books.filter(tag=tag.id)

    lang = request.GET.get('lang')
    if lang:
        filtered_books = filtered_books.filter(
            narrations__language=lang.upper())

    language_options = [('', 'усе', lang == None)]
    for available_lang in Language.values:
        language_options.append(
            (available_lang.lower(), to_human_language(available_lang),
             lang == available_lang.lower()))

    paid = request.GET.get('paid')
    if paid is not None:
        filtered_books = filtered_books.filter(
            narrations__paid=(request.GET.get('paid') == 'true'))

    price_options = [
        ('', 'усе', paid is None),
        ('true', 'платныя', paid == 'true'),
        ('false', 'бясплатныя', paid == 'false'),
    ]

    link = request.GET.get('links')
    link_options = [('', 'усе', lang == None)]
    for available_link in LinkType.objects.filter(
            disabled=False).order_by('caption'):
        link_options.append((available_link.name, available_link.caption,
                             link == available_link.name))

    sorted_books = filtered_books.order_by('-date')
    paginator = Paginator(sorted_books, BOOKS_PER_PAGE)
    books_per_page = max(int(request.GET.get('limit', 0)), BOOKS_PER_PAGE)
    paginator = Paginator(sorted_books, books_per_page)
    paged_books: Page = paginator.get_page(page)

    def related_page(page: int) -> str:
        params = request.GET.copy()
        if page == 1:
            params.pop('page')
        else:
            params['page'] = page
        return request.path + ('?' if len(params) > 0 else
                               '') + params.urlencode()

    related_pages = {
        'has_other': paged_books.has_other_pages(),
    }
    if paged_books.has_previous():
        related_pages['first'] = related_page(1)
        related_pages['prev'] = related_page(
            paged_books.previous_page_number())
    if paged_books.has_next():
        related_pages['last'] = related_page(paginator.num_pages)
        related_pages['next'] = related_page(paged_books.next_page_number())

    context = {
        'books': paged_books,
        'related_pages': related_pages,
        'selected_tag': tag,
        'tags': tags,
        'query_params': get_query_params_without(request, 'page'),
        'language_options': language_options,
        'price_options': price_options,
        'link_options': link_options,
    }
    return render(request, 'books/catalog.html', context)
