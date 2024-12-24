import requests
import jwt
import time
from django.conf import settings
from django.core.cache import cache
from app import models

def get_centrifugo_info(user_id):
    secret = settings.CENTRIFUGO_SECRET_KEY
    claims = {"sub": str(user_id), "exp": int(time.time()) + 5 * 60}
    token = jwt.encode(claims, secret, algorithm='HS256') 
    return {"token": token, "ws_url": settings.CENTRIFUGO_WS_URL}

def get_popular_tags():
    tags = cache.get("popular_tags")
    if tags is None:
        
        tags = models.Tag.objects.get_popular_tags_last_3_months()
        
        cache.set("popular_tags", tags, timeout= 3 * 30 * 24 * 60 * 60)
        print(tags)
    return tags

def get_best_users():
    profiles = cache.get("best_profiles")
    if profiles is None:
        profiles = models.Profile.objects.get_top_profiles_last_week()

        cache.set("best_profiles", profiles, timeout= 7 * 24 * 60 * 60)
        print(profiles)
    return profiles

def global_settings(request):
    tags = get_popular_tags()
    profiles = get_best_users()
    return {"popular_tags": tags,
            "best_profiles": profiles,
            **get_centrifugo_info(request.user.id)}
