"""
This file contains all the application views.
A view function is a Python function that takes a Web request and return a Web response.
"""

from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect, render
from django.contrib.gis.geos import GeometryCollection

from django.db import models
from .models import Contact, Bibliographic, Volcano, Eruption, Fissure, Cone, Tephras, Flow, Sample, MntOrtho
from .filters import * 
from django.core.serializers import serialize
import json

def index(request):
    """ This function returns the list of elements to show on the homepage """

    home_list = ['Volcano', 'Eruptions', 'Fissures', 'Flows', 'Cones', 'Tephras']
    template = loader.get_template('app/index.html')
    context = {
        'home_list': home_list,
    }
    return HttpResponse(template.render(context, request))


def search(request, feature_type, output_feature_type=''):
    """ This function filters the input parameters in the search form """ 

    if feature_type == 'volcano':
        feature_list = Volcano.objects.all()
        feature_filter = VolcanoFilter(request.GET, queryset = feature_list)

    elif feature_type == 'eruption' or output_feature_type == 'eruption':
        feature_list = Eruption.objects.all()
        feature_filter = EruptionFilter(request.GET, queryset = feature_list)

    elif feature_type == 'fissure' or output_feature_type == 'fissure':
        feature_list = Fissure.objects.all()
        feature_filter = FissureFilter(request.GET, queryset = feature_list)

    elif feature_type == 'flow' or output_feature_type == 'flow':
        feature_list = Flow.objects.all()
        feature_filter = FlowFilter(request.GET, queryset = feature_list)

    elif feature_type == 'cone' or output_feature_type == 'cone':
        feature_list = Cone.objects.all()
        feature_filter = ConeFilter(request.GET, queryset = feature_list)

    elif feature_type == 'tephras' or output_feature_type == 'tephras':
        feature_list = Tephras.objects.all()
        feature_filter = TephrasFilter(request.GET, queryset = feature_list)

    elif feature_type == 'sample' or output_feature_type == 'sample':
        feature_list = Sample.objects.all()
        feature_filter = SampleFilter(request.GET, queryset = feature_list)

    elif feature_type == 'mntortho' or output_feature_type == 'mntortho':
        feature_list = MntOrtho.objects.all()
        feature_filter = MntOrthoFilter(request.GET, queryset = feature_list)

    return render(request, 'app/search_list.html', {'filter' : feature_filter, 'feature_type': feature_type})


 
def get_related_features(request, feature_type, feature_id, output_feature_type):
    """ This function returns the features related to an given type of data """

    list_ed_id = []
    list_fissure_id = []
    list_cone_id = []
    list_tephras_id = []
    list_flow_id = []
    list_sample_id = []
    list_mntortho_id = []
    list_co_id = []

    # If the feature type is volcano
    if feature_type == 'volcano':
    # We look for related eruptions, observations
        eruptions = Eruption.objects.filter(vd_id=feature_id)
        observations = Observation.objects.filter(vd_id=feature_id)

        for e in eruptions:
            list_ed_id.append(getattr(e, "ed_id"))

        for o in observations:
            list_co_id.append(getattr(o, "co_id"))

        # For each eruption we look for related fissures
        for i in list_ed_id:
            fissures = Fissure.objects.filter(ed_id=i)
            for f in fissures:
                list_fissure_id.append(getattr(f,"fissure_id"))
    
    # If the feature type is eruption
    if feature_type == 'eruption':
        # We look for related fissures
        fissures = Fissure.objects.filter(ed_id=feature_id)
        for f in fissures:
            list_fissure_id.append(getattr(f,"fissure_id"))

    # For each fissure we look for related cones, tephras, flows
    for f in list_fissure_id:
        cones = Cone.objects.filter(fissure_id=f)
        tephras = Tephras.objects.filter(fissure_id=f)
        flows = Flow.objects.filter(fissure_id=f)
        for c in cones:
            list_cone_id.append(getattr(c, "cone_id"))
        for t in tephras:
            list_tephras_id.append(getattr(t, "teph_id"))
        for fl in flows:
            list_flow_id.append(getattr(fl, "flow_id"))

    # etc...
    if feature_type == 'fissure':
        cones = Cone.objects.filter(fissure_id=feature_id)
        tephras = Tephras.objects.filter(fissure_id=feature_id)
        flows = Flow.objects.filter(fissure_id=feature_id)

        for c in cones:
            list_cone_id.append(getattr(c, "cone_id"))
        for t in tephras:
            list_tephras_id.append(getattr(t, "teph_id"))
        for fl in flows:
            list_flow_id.append(getattr(fl, "flow_id"))



#        for c in list_cone_id:
#            samples = Sample.objects.filter(cone_id=c)
#            for s in samples:
#                list_sample_id.append(getattr(s, "sample_id"))
#        for t in list_tephras_id:
#            samples = Sample.objects.filter(teph_id=t)
#            for s in samples:
#                list_sample_id.append(getattr(s, "sample_id"))
    for fl in list_flow_id:
#        samples = Sample.objects.filter(flow_id=fl)
        mntorthos = MntOrtho.objects.filter(flow_ids=fl)
#            for s in samples:
#                list_sample_id.append(getattr(s, "sample_id"))
        for m in mntorthos:
            list_mntortho_id.append(getattr(m, "mo_id"))


#        samples = Sample.objects.filter(sample_id__in=list_sample_id)

    if feature_type == 'flow':
        mntorthos = MntOrtho.objects.filter(flow_ids=feature_id)
        for m in mntorthos:
            list_mntortho_id.append(getattr(m, "mo_id"))

    fissures = Fissure.objects.filter(fissure_id__in=list_fissure_id).order_by('opentime')
    cones = Cone.objects.filter(cone_id__in=list_cone_id).order_by('accretion_date')
    tephras = Tephras.objects.filter(teph_id__in=list_tephras_id).order_by('accretion_date')
    flows = Flow.objects.filter(flow_id__in=list_flow_id).order_by('stime')
    mntorthos = MntOrtho.objects.filter(mo_id__in=list_mntortho_id).order_by('loaddate')

    # For each feature type we associate the right related features list

    if output_feature_type == 'eruption':
        related_features = eruptions
        template = loader.get_template('app/eruption.html')

    elif output_feature_type == 'fissure':
        related_features = fissures
        template = loader.get_template('app/fissure.html')

    elif output_feature_type == 'cone':
        related_features = cones
        template = loader.get_template('app/cone.html')

    elif output_feature_type == 'tephras':
        related_features = tephras
        template = loader.get_template('app/tephras.html')

    elif output_feature_type == 'flow':
        related_features = flows
        template = loader.get_template('app/flow.html')

    elif output_feature_type == 'mntortho':
        related_features = mntorthos
        template = loader.get_template('app/mntortho.html')
        
    elif output_feature_type == 'observation':
        related_features = observations
        template = loader.get_template('app/observation.html')

    # The title that will be displayed at the top of the page
    header = "Liste des " + output_feature_type + "s associees"

    # If the entities have geometry we return them so they can be displayed
    if [hasattr(feature, 'geometry') for feature in related_features] :
        geometries = serialize('geojson', related_features, srid=4326)
        print(json.loads(geometries))
    else:
        geometries = ""

    context = {
		'related_features': related_features,
		'output_feature_type': output_feature_type,
		'feature_type': feature_type,
		'feature_id': feature_id,
                'header': header,
                'geometries': geometries,
}

    return HttpResponse(template.render(context, request))




def related_features_detail(request, feature_type, feature_id, output_feature_type, output_feature_id):
    """ This function allows the user to visualize the details of a selected related feature """

    att_to_display = ""
    features = []
    raster = ""
    reverse = False
    att_list = []
    att_verbose_names = []

    if output_feature_type == 'volcano':
        # We get the correct feature
        feature = get_object_or_404(Volcano, pk=output_feature_id)
        # The attribute to be displayed as a title
        att_to_display = "vd_name"
        feature_name = ""
        features = ['eruption', 'fissure', 'tephras', 'flow', 'cone', 'sample', 'mntortho', 'observation']
        att_list = ['vd_cavw', 'vd_name', 'vd_name2', 'vd_tzone', 'vd_mcont', 'vd_com', 'cc_id1', 'cc_id2', 'cc_id3', 'cc_id4', 'cc_id5', 'cc_load']

    elif output_feature_type == 'eruption':
        # We get the correct feature
        feature = get_object_or_404(Eruption, pk=output_feature_id)
        # The attribute to be displayed and the feature name to be written as a title
        att_to_display = "ed_stime"
        feature_name = ["Eruption "]
        features = ['fissure', 'tephras', 'flow', 'cone', 'mntortho']
        att_list = ['ed_code', 'ed_name', 'ed_nar', 'ed_stime', 'ed_stime_bc', 'ed_stime_unc', 'ed_etime', 'ed_etime_bc', 'ed_etime_unc', 'ed_climax', 'ed_climax_bc', 'ed_climax_unc', 'ed_com', 'vd', 'cc_id', 'cc_load_id']

    elif output_feature_type == 'fissure':
        # We get the correct feature
        feature = get_object_or_404(Fissure, pk=output_feature_id)
        # The attribute to be displayed and the feature name to be written as a title
        att_to_display = "opentime"
        feature_name = ["Fissure "]
        features = ['tephras', 'flow', 'cone', 'mntortho']
        att_list = ['opentime', 'opentime_bc', 'opentime_unc', 'com', 'com2', 'com3', 'com4', 'com5', 'com6', 'ed', 'cc_load', 'cc_pub']

    elif output_feature_type == 'tephras':
        # We get the correct feature
        feature = get_object_or_404(Tephras, pk=output_feature_id)
        # The attribute to be displayed  and the feature name to be written as a title
        att_to_display = "accretion_date"
        feature_name = ["Tephras "]
        att_list = ['accretion_date', 'accretion_date_bc', 'accretion_date_unc', 'disappearance_date', 'disappearance_date_bc', 'disappearance_date_unc', 'teph_granulometry', 'com', 'fissure', 'cc_load', 'cc_pub']

    elif output_feature_type == 'flow':
        # We get the correct feature
        feature = get_object_or_404(Flow, pk=output_feature_id)
        # The attribute to be displayed and the feature name to be written as a title
        att_to_display = "stime"
        feature_name = ["Flow "]
        features = ['mntortho']
        att_list = ['stime', 'stime_bc', 'stime_unc', 'etime', 'etime_bc', 'etime_unc', 'final_vers', 'flux', 'com', 'fissure', 'cc_load', 'cc_pub']

    elif output_feature_type == 'cone':
        # We get the correct feature
        feature = get_object_or_404(Cone, pk=output_feature_id)
        # The attribute to be displayed and the feature name to be written as a title
        att_to_display = "name"
        feature_name = ""
        att_list = ['name', 'cone_type', 'height', 'accretion_date', 'accretion_date_bc', 'accretion_date_unc', 'disappearance_date', 'disappearance_date_bc', 'disappearance_date_unc', 'crater_diameter', 'com', 'com2', 'com3', 'fissure', 'cc_load', 'cc_pub']

    elif output_feature_type == 'sample':
        # We get the correct feature
        feature = get_object_or_404(Sample, pk=output_feature_id)
        # The attribute to be displayed and the feature name to be written as a title
        att_to_display = "sampledate"
        feature_name = ["Sample "]
        att_list = ['sample_code', 'sample_location', 'sample_elevation', 'sample_date', 'sample_samplingtime', 'sample_type', 'sample_collection_method', 'sample_collection_tool', 'sample_size', 'sample_weight', 'sample_texture', 'sample_geological_age', 'sample_geological_unit', 'sample_gsn_rock', 'sample_gsn_rock', 'sample_photo', 'teph', 'cone', 'flow', 'cc_load', 'cc_pub']

    elif output_feature_type == 'mntortho':
        # We get the correct feature
        feature = get_object_or_404(MntOrtho, pk=output_feature_id)
        # The attribute to be displayed and the feature name to be written as a title
        att_to_display = "loaddate"
        feature_name = ["DTM / Orthoimage "]
        raster = getattr(feature, 'raster')
        if getattr(feature, 'flow_ids') != Null:
            reverse = True
        att_list = ['gcp_num', 'reference_altitude', 'precision', 'mo_type', 'mo_gcp_type', 'mo_software', 'com', 'flow_ids', 'am', 'cc_load', 'cc_pub']

    elif output_feature_type == 'observation':
        # We get the correct feature
        feature = get_object_or_404(Observation, pk=output_feature_id)
        # The attribute to be displayed and the feature name to be written as a title
        att_to_display = "co_stime"
        feature_name = ["Observation "]
        att_list = ['co_code', 'co_observe', 'co_stime', 'co_stime_unc', 'co_etime', 'co_etime_unc', 'co_com', 'vd', 'cc_id', 'cc_id2', 'cc_id3', 'cc_id4', 'cc_id5', 'cc_load']


    # The list of the related feature attributes
    #att_list = [field.name for field in feature._meta.fields # pylint: disable=W0212
    #            if not isinstance(field, models.ForeignKey)]

    # The attributes verbose names
    for field in feature._meta.fields:
        for att in att_list:
            if field.name == att:
                att_verbose_names.append(field.verbose_name)

    #att_verbose_names = [field.verbose_name for field in feature._meta.fields # pylint: disable=W0212
    #             if not isinstance(field, models.ForeignKey)]


   # The attributes values
    att_value = []
    
   # We display a "good" name for the related feature
    for att in att_list:
        if getattr(feature, att) != None and att.find('cc_load') == -1 and att.find('cc_id') == -1 and att.find('cc_pub') == -1 and att != 'vd' and att!= 'ed' and att != 'teph' and att != 'fissure' and att != 'flow' and att != 'cone':
            att_value.append(getattr(feature, att))
        elif getattr(feature, att) != None and (att.find('cc_load') != -1 or att.find('cc_id') != -1 or att.find('cc_pub') != -1):
            cc_load = getattr(feature,att)
            lname = getattr(cc_load,'cc_lname')
            att_value.append(lname)
        elif getattr(feature, att) != None and att == 'vd':
            vd = getattr(feature,att)
            vd_name = getattr(vd,'vd_name')
            att_value.append(vd_name)
        elif getattr(feature, att) != None and att == 'ed':
            ed = getattr(feature,att)
            ed_stime = getattr(ed,'ed_stime')
            att_value.append(ed_stime)
        elif getattr(feature, att) != None and att == 'teph':
            teph = getattr(feature,att)
            teph_date = getattr(teph,'accretion_date')
            att_value.append(teph_date)
        elif getattr(feature, att) != None and att == 'fissure':
            fissure = getattr(feature,att)
            fissure_opentime = getattr(fissure,'opentime')
            att_value.append(fissure_opentime)
        elif getattr(feature, att) != None and att == 'flow':
            flow = getattr(feature,att)
            flow_stime = getattr(flow,'stime')
            att_value.append(flow_stime)
        elif getattr(feature, att) != None and att == 'cone':
            cone = getattr(feature,att)
            cone_date = getattr(cone,'accretion_date')
            att_value.append(cone_date)
        else:
            att_value.append('')

        if att == att_to_display:
            if output_feature_type != 'cone':
                date = str(getattr(feature, att)).split(" ")[0]
                feature_name.append(date)
                feature_name = " ".join(feature_name)

            else:
                feature_name = str(getattr(feature, att))

    att = zip(att_verbose_names, att_value)

    return render(request, 'app/detail.html',
                  {'att': att, 'feature_type': feature_type, 'feature_id': feature_id, 'output_feature_id': output_feature_id, 'output_feature_type': output_feature_type, 'features': features, 'att_value': att_value, 'att_verbose_names':att_verbose_names, 'feature_name': feature_name, 'raster':raster})



def get_features(request, feature_type):

    """" This function returns all the elements of a given feature type """
    if feature_type == 'volcano':
        feature_list = Volcano.objects.all()
        template = loader.get_template('app/volcano.html')

    if feature_type == 'eruption':
        feature_list = Eruption.objects.all()
        template = loader.get_template('app/eruption.html')
        
    elif feature_type == 'fissure':
        feature_list = Fissure.objects.all()
        template = loader.get_template('app/fissure.html')

    elif feature_type == 'tephras':
        feature_list = Tephras.objects.all()
        template = loader.get_template('app/tephras.html')

    elif feature_type == 'flow':
        feature_list = Flow.objects.all()
        template = loader.get_template('app/flow.html')

    elif feature_type == 'cone':
        feature_list = Cone.objects.all()
        template = loader.get_template('app/cone.html')

    elif feature_type == 'sample':
        feature_list = Sample.objects.all()
        template = loader.get_template('app/sample.html')

    elif feature_type == 'mntortho':
        feature_list = MntOrtho.objects.all()
        template = loader.get_template('app/mntortho.html')

    # If the entities have geometry we return them so they can be displayed
    if [hasattr(feature, 'geometry') for feature in feature_list]:
        geometries = serialize('geojson', feature_list, srid=4326)
        print(geometries)
    else:
        geometries = ""


    context = {
        'feature_list': feature_list,
        'feature_type': feature_type,
        'geometries': geometries,
    }
    return HttpResponse(template.render(context, request))


def detail(request, feature_type, feature_id):
    """ This function returns the details for a given entity """

    # The attribute to display on the presenting page
    att_to_display = ""
    output_feature_type = ''
    # These 2 are used to be able to get back to the previous feature object
    reverse_feature_type = ''
    reverse_feature_id = 0
    raster = ""
    reverse = False
    att_list = []
    att_verbose_names = []

    # features is the list of related features to access
    features = []

    if feature_type == 'volcano':
        feature = get_object_or_404(Volcano, pk=feature_id)
        att_to_display = "vd_name"
        feature_name = ""
        features = ['eruption', 'fissure','tephras', 'flow', 'cone', 'sample', 'mntortho', 'observation']
        att_list = ['vd_cavw', 'vd_name', 'vd_name2', 'vd_tzone', 'vd_mcont', 'vd_com', 'cc_id1', 'cc_id2', 'cc_id3', 'cc_id4', 'cc_id5', 'cc_load']


    elif feature_type == 'eruption':
        feature = get_object_or_404(Eruption, pk=feature_id)
        att_to_display = "ed_stime"
        feature_name = ["Eruption "]
        reverse_feature_type = 'volcano'
        reverse_feature_id = getattr(feature, 'vd_id')
#        reverse_feature_id = getattr(reverse_feature_id, 'vd_id')
        features = ['fissure', 'tephras', 'flow', 'cone', 'mntortho']
        att_list = ['ed_code', 'ed_name', 'ed_nar', 'ed_stime', 'ed_stime_bc', 'ed_stime_unc', 'ed_etime', 'ed_etime_bc', 'ed_etime_unc', 'ed_climax', 'ed_climax_bc', 'ed_climax_unc', 'ed_com', 'vd', 'cc_id', 'cc_load_id']

    elif feature_type == 'fissure':
        feature = get_object_or_404(Fissure, pk=feature_id)
        feature = Fissure.objects.get(fissure_id=feature_id)
        att_to_display = "opentime"
        feature_name = ["Fissure "]
        reverse_feature_type = 'eruption'
        reverse_feature_id = getattr(feature, 'ed_id')
#        reverse_feature_id = getattr(reverse_feature_id, 'ed_id')
        features = ['tephras', 'flow', 'cone', 'mntortho']
        att_list = ['opentime', 'opentime_bc', 'opentime_unc', 'com', 'com2', 'com3', 'com4', 'com5', 'com6', 'ed', 'cc_load', 'cc_pub']

    elif feature_type == 'tephras':
        feature = get_object_or_404(Tephras, pk=feature_id)
        att_to_display = "accretion_date"
        feature_name = ["Tephras "]
        reverse_feature_type = 'fissure'
        reverse_feature_id = getattr(feature, 'fissure_id')
#        reverse_feature_id = getattr(reverse_feature_id, 'fissure_id')
        att_list = ['accretion_date', 'accretion_date_bc', 'accretion_date_unc', 'disappearance_date', 'disappearance_date_bc', 'disappearance_date_unc', 'teph_granulometry', 'com', 'fissure', 'cc_load', 'cc_pub']

    elif feature_type == 'flow':
        feature = get_object_or_404(Flow, pk=feature_id)
        att_to_display = "stime"
        feature_name = ["Flow "]
        reverse_feature_type = 'fissure'
        reverse_feature_id = getattr(feature, 'fissure_id')
#        reverse_feature_id = getattr(reverse_feature_id, 'fissure_id')
        features = ['mntortho']
        att_list = ['stime', 'stime_bc', 'stime_unc', 'etime', 'etime_bc', 'etime_unc', 'final_vers', 'flux', 'com', 'fissure', 'cc_load', 'cc_pub']

    elif feature_type == 'cone':
        feature = get_object_or_404(Cone, pk=feature_id)
        att_to_display = "stime"
        feature_name = ["Cone "]
        reverse_feature_type = 'fissure'
        reverse_feature_id = getattr(feature, 'fissure_id')
#        reverse_feature_id = getattr(reverse_feature_id, 'fissure_id')
        att_list = ['name', 'cone_type', 'height', 'accretion_date', 'accretion_date_bc', 'accretion_date_unc', 'disappearance_date', 'disappearance_date_bc', 'disappearance_date_unc', 'crater_diameter', 'com', 'com2', 'com3', 'fissure', 'cc_load', 'cc_pub']

    elif feature_type == 'sample':
        feature = get_object_or_404(Sample, pk=feature_id)
        att_to_display = "sampledate"
        feature_name = ["Sample "]
        att_list = ['sample_code', 'sample_location', 'sample_elevation', 'sample_date', 'sample_samplingtime', 'sample_type', 'sample_collection_method', 'sample_collection_tool', 'sample_size', 'sample_weight', 'sample_texture', 'sample_geological_age', 'sample_geological_unit', 'sample_gsn_rock', 'sample_gsn_rock', 'sample_photo', 'teph', 'cone', 'flow', 'cc_load', 'cc_pub']

    elif feature_type == 'mntortho':
        feature = get_object_or_404(MntOrtho, pk=feature_id)
        att_to_display = "loaddate"
        feature_name = ["DTM / Orthoimage "]
        reverse_feature_type = 'flow'
        if (getattr(feature, 'flow_ids') is None):
            reverse = True
            reverse_feature_id = getattr(feature, 'flow_ids')
#        reverse_feature_id = getattr(reverse_feature_id, 'flow_ids')
        raster = getattr(feature, 'raster')
        att_list = ['gcp_num', 'reference_altitude', 'precision', 'mo_type', 'mo_gcp_type', 'mo_software', 'com', 'flow_ids', 'am', 'cc_load', 'cc_pub']

    elif feature_type == 'observation':
        feature = get_object_or_404(Observation, pk=feature_id)
        att_to_display = "co_stime"
        feature_name = ["Observations "]
        att_list = ['co_code', 'co_observe', 'co_stime', 'co_stime_unc', 'co_etime', 'co_etime_unc', 'co_com', 'vd', 'cc_id', 'cc_id2', 'cc_id3', 'cc_id4', 'cc_id5', 'cc_load']

    # The list of the feature attributes
    #att_list = [field.name for field in feature._meta.fields # pylint: disable=W0212
#                if not isinstance(field, models.ForeignKey)
#               ]

    # The attributes verbose names
    for field in feature._meta.fields:
        for att in att_list:
            if field.name == att:
                att_verbose_names.append(field.verbose_name)


    #att_verbose_names = [field.verbose_name for field in feature._meta.fields # pylint: disable=W0212
#                 if not isinstance(field, models.ForeignKey)
#               ] 

    # The attributes values
    att_value = []
    # These two are used if the feature type is volcano to display VolcanoInformation table attributes
    att_list2 = []
    att_verbose_names2 = []

    if feature_type == 'volcano':
        # We get some VolcanoInfoamtion attributes
        if VolcanoInformation.objects.filter(vd_id=feature_id):
            obj = VolcanoInformation.objects.filter(vd_id=feature_id)[0]
            att_list2 = [field.name for field in obj._meta.fields # pylint: disable=W0212
                if not isinstance(field, models.ForeignKey)
               ][1:14]

            # We get VolcanoInformation attibutes verbose names
            att_verbose_names2 = [field.verbose_name for field in obj._meta.fields # pylint: disable=W0212
                if not isinstance(field, models.ForeignKey)
               ][1:14]

            # We had VolcanoInformation fields verbose names at the end of verbose names list
            for name in att_verbose_names2:
                att_verbose_names.append(name)

        for att in att_list:
            if getattr(feature, att) != None and att.find('cc_load') == -1 and att.find('cc_id') == -1 and att.find('cc_pub') == -1 and att != 'vd' and att!= 'ed' and att != 'teph' and att != 'fissure' and att != 'flow' and att != 'cone':
                att_value.append(getattr(feature, att))
            elif getattr(feature, att) != None and (att.find('cc_load') != -1 or att.find('cc_id') != -1 or att.find('cc_pub') != -1):
                cc_load = getattr(feature,att)
                lname = getattr(cc_load,'cc_lname')
                att_value.append(lname)
            elif getattr(feature, att) != None and att == 'vd':
                vd = getattr(feature,att)
                vd_name = getattr(vd,'vd_name')
                att_value.append(vd_name)
            elif getattr(feature, att) != None and att == 'ed':
                ed = getattr(feature,att)
                ed_stime = getattr(ed,'ed_stime')
                att_value.append(ed_stime)
            elif getattr(feature, att) != None and att == 'teph':
                teph = getattr(feature,att)
                teph_date = getattr(teph,'accretion_date')
                att_value.append(teph_date)
            elif getattr(feature, att) != None and att == 'fissure':
                fissure = getattr(feature,att)
                fissure_opentime = getattr(fissure,'opentime')
                att_value.append(fissure_opentime)
            elif getattr(feature, att) != None and att == 'flow':
                flow = getattr(feature,att)
                flow_stime = getattr(flow,'stime')
                att_value.append(flow_stime)
            elif getattr(feature, att) != None and att == 'cone':
                cone = getattr(feature,att)
                cone_date = getattr(cone,'accretion_date')
                att_value.append(cone_date)
            else:
                att_value.append('')


            if att == att_to_display:
                feature_name = getattr(feature, att)

        # We had VolcanoInformation fields at the end of the attribute list
        if att_list2:
            for att in att_list2:
                att_value.append(getattr(obj, att))
        

    else:
        for att in att_list:
            if getattr(feature, att) != None and att.find('cc_load') == -1 and att.find('cc_id') == -1 and att.find('cc_pub') == -1 and att != 'vd' and att!= 'ed' and att != 'teph' and att != 'fissure' and att != 'flow' and att != 'cone':
                att_value.append(getattr(feature, att))
            elif getattr(feature, att) != None and (att.find('cc_load') != -1 or att.find('cc_id') != -1 or att.find('cc_pub') != -1):
                cc_load = getattr(feature,att)
                lname = getattr(cc_load,'cc_lname')
                att_value.append(lname)
            elif getattr(feature, att) != None and att == 'vd':
                vd = getattr(feature,att)
                vd_name = getattr(vd,'vd_name')
                att_value.append(vd_name)
            elif getattr(feature, att) != None and att == 'ed':
                ed = getattr(feature,att)
                ed_stime = getattr(ed,'ed_stime')
                att_value.append(ed_stime)
            elif getattr(feature, att) != None and att == 'teph':
                teph = getattr(feature,att)
                teph_date = getattr(teph,'accretion_date')
                att_value.append(teph_date)
            elif getattr(feature, att) != None and att == 'fissure':
                fissure = getattr(feature,att)
                fissure_opentime = getattr(fissure,'opentime')
                att_value.append(fissure_opentime)
            elif getattr(feature, att) != None and att == 'flow':
                flow = getattr(feature,att)
                flow_stime = getattr(flow,'stime')
                att_value.append(flow_stime)
            elif getattr(feature, att) != None and att == 'cone':
                cone = getattr(feature,att)
                cone_date = getattr(cone,'accretion_date')
                att_value.append(cone_date)
            else:
                att_value.append('')


            if att == att_to_display:
                date = str(getattr(feature, att)).split(" ")[0]
                feature_name.append(date)
                feature_name = " ".join(feature_name)

    att = zip(att_verbose_names, att_value)

    return render(request, 'app/detail.html',
                  {'att': att, 'feature_type': feature_type, 'feature_id': feature_id, 'output_feature_type': output_feature_type, 'reverse_feature_type': reverse_feature_type, 'reverse_feature_id': reverse_feature_id, 'att_value': att_value, 'att_verbose_names': att_verbose_names, 'feature_name': feature_name, 'features': features, 'raster': raster, 'reverse': reverse})


def admin(request):
    """ This function redirects to the admin pannel """

    return redirect("http://195.83.188.45:8000/admin/")


def add(request, feature_type):
    """ This function redirects to the "add feature" page """

    return redirect("http://195.83.188.45:8000/admin/app/"+ feature_type +"/add/")


def modify(request, feature_type, feature_id, output_feature_type='', output_feature_id=0):
    """ This function redirects to the "modify feature" page """

    url = ["http://195.83.188.45:8000/admin/app/" +str(feature_type) + "/", str(feature_id), "/change/"]
    return redirect(" ".join(url))


