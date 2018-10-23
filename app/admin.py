from django.contrib import admin

from .models import Contact, Bibliographic, Volcano, Observation, VolcanoInformation, Fissure, Cone, Tephras, Flow, Volume, Sample, Petrology, Composition,  MntOrtho, SatelliteAirplane, AcquisitionMethod, AcquisitionTool, Eruption, SeismicEvent 
from leaflet.admin import LeafletGeoAdmin
from django import forms

admin.site.register(Contact, LeafletGeoAdmin)
admin.site.register(Bibliographic, LeafletGeoAdmin)
admin.site.register(Volcano, LeafletGeoAdmin)
admin.site.register(Observation, LeafletGeoAdmin)
admin.site.register(VolcanoInformation, LeafletGeoAdmin)
admin.site.register(Fissure, LeafletGeoAdmin)
admin.site.register(Cone, LeafletGeoAdmin)
admin.site.register(Tephras, LeafletGeoAdmin)
admin.site.register(Flow, LeafletGeoAdmin)
admin.site.register(Volume, LeafletGeoAdmin)
admin.site.register(Sample, LeafletGeoAdmin)
admin.site.register(Petrology, LeafletGeoAdmin)
admin.site.register(Composition, LeafletGeoAdmin)
admin.site.register(MntOrtho, LeafletGeoAdmin)
admin.site.register(SatelliteAirplane, LeafletGeoAdmin)
admin.site.register(AcquisitionMethod, LeafletGeoAdmin)
admin.site.register(AcquisitionTool, LeafletGeoAdmin)
admin.site.register(Eruption, LeafletGeoAdmin)
admin.site.register(SeismicEvent, LeafletGeoAdmin)

