import shutil
from django.conf import settings

shutil.unpack_archive('img.zip', settings.MEDIA_URL)
