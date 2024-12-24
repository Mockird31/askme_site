from django.core.management.base import BaseCommand, CommandError
from app import models
from django.core.cache import cache
import random

class Command(BaseCommand):
    help = 'Update cache'

    def handle(self, *args, **options):
        profiles = models.Profile.objects.get_top_profiles_last_week()
        cache.set("best_profiles", profiles, timeout= 7 * 24 * 60 * 60)

