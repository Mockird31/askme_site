from django.core.paginator import Paginator
from app import models
from django.db.models import Count

def paginate(object_list, request, per_page=10):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(object_list, per_page)
    try:
        page_num = int(page_num)
    except ValueError:
        page_num = paginator.num_pages
    page = paginator.get_page(page_num)
    return page


def find_page_with_tag(QUESTIONS, tag_name):
    tag_questions = []
    for question in QUESTIONS:
        for tag in question.tags.all():
            if tag_name == tag.tag_name:
                tag_questions.append(question)

    if len(tag_questions) == 0:
        return []
    else:
        return tag_questions
    
    