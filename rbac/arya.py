from arya.service import sites
from . import models
sites.site.register(models.User)
sites.site.register(models.Role)
sites.site.register(models.Permission)
sites.site.register(models.Menu)