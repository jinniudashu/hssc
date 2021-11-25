from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify

from django.contrib.auth.models import Group, User

from time import time
from django.utils import timezone

from icpc.models import *
from dictionaries.enums import *
from core.models import Staff, Customer


def gen_slug(s):
    slug = slugify(s, allow_unicode=True)
    return slug + f'-{int(time())}'