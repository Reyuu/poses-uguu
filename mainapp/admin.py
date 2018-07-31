from django.contrib import admin
from mainapp.models import Devs, DoneDevs, ReportedPics, IgnoredPics, SuggestionBox, FeedbackBox
# Register your models here.

admin.site.register(Devs)
admin.site.register(DoneDevs)
admin.site.register(ReportedPics)
admin.site.register(IgnoredPics)
admin.site.register(SuggestionBox)
admin.site.register(FeedbackBox)