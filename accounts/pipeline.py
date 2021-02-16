from accounts.models import Profile
from social_core.backends.google import GoogleOAuth2
from urllib.request import urlopen
from django.template.defaultfilters import slugify
from django.core.files.base import ContentFile


def save_profile(backend, details, response, uid,user, *args, **kwargs):
      if backend.__class__ == GoogleOAuth2:
        profile, is_created = Profile.objects.get_or_create(user =user)
        if profile.profile_image.url=="/media/"+"profile/profile.png":
          url = response['picture']
          avatar = urlopen(url)
          profile.profile_image.save(slugify(user.username + " social") + '.jpg',
          ContentFile(avatar.read()))
          profile.save()
        if not profile.fullname:
          profile.fullname = response['name']
          profile.save()   