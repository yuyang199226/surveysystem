from arya.service import sites
from . import models
class SurveyConf(sites.AryaConfig):
    list_display = ['title','theme','create_time']
sites.site.register(models.Survey)

sites.site.register(models.Profile)
sites.site.register(models.Department)
sites.site.register(models.Qitem)