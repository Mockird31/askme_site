from django.core.management.base import BaseCommand, CommandError
from app import models
from django.core.cache import cache
import random

class Command(BaseCommand):
    help = 'Update cache'

    def handle(self, *args, **options):
        tags = models.Tag.objects.get_popular_tags_last_3_months()
        cache.set("popular_tags", tags, timeout= 3 * 30 * 24 * 60 * 60)

