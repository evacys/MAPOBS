from .models import *
from mapobs import settings
import django_filters
from django import forms
from django.forms import DateTimeField
import datetime
from django.db.models import Max

""" This file defines every field that will be used for the search tool """ 


def num_calderas_choices():
    """ This function get the maximum number of calderas and returns a list from 0 to this number """
    # Get the maximum number of calderas
    max_count = VolcanoInformation.objects.aggregate(result=Max('vd_inf_numcal'))['result']
    if max_count:
    # Generate a list of two-tuples for the select dropdown, from 0 to max_count
    # e.g, [(0, 0), (1, 1), (2, 2), ...]
        return zip(range(max_count+1), range(max_count+1))
    else:
        return None

class VolcanoFilter(django_filters.FilterSet):
    """ Defines the search fields for volcano objects """

    # Volcano name
    name = Volcano.objects.values_list('vd_name', flat=True)

    vd_name = django_filters.ChoiceFilter(
                                     widget=forms.Select, 
                                     label='Volcano name',
                                     field_name='vd_name',
                                     choices=zip(name,name),
                                     )
    # Volcano number of caldera
    if VolcanoInformation.objects.aggregate(result=Max('vd_inf_numcal'))['result']:
        vd_inf_numcal = django_filters.ChoiceFilter(
                                      field_name='vd_inf_vd_id__vd_inf_numcal',
                                      label='Number of calderas',
                                      choices=num_calderas_choices,
                                           )

    # We define here the possible choices for some fields
    cavw = VolcanoInformation.objects.values_list('vd_inf_cavw', flat=True).order_by('vd_inf_cavw').distinct()
    selev = VolcanoInformation.objects.values_list('vd_inf_selev', flat=True).order_by('vd_inf_selev').distinct()
    TYPE_ENUM = (("CALDE", "Caldera"),
                 ("CINDE", "Cinder cone"),
                 ("COMPL", "Complex volcano"),
                 ("COMPO", "Compound volcano"),
                 ("CONE", "Cone"),
                 ("CRATE", "Crater rows"),
                 ("EXPLO", "Explosion craters"),
                 ("FISSU", "Fissure vent"),
                 ("HYDRO", "Hydrothermal field"),
                 ("LAVAC", "Lava cone"),
                 ("LAVAD", "Lava dome"),
                 ("MAAR", "Maar"),
                 ("PUMIC", "Pumice cone"),
                 ("PYROC", "Pyroclastic cone"),
                 ("PYROS", "Pyroclastic shield"),
                 ("SCORI", "Scoria cone"),
                 ("SHIEL", "Shield volcano"),
                 ("SOMMA", "Somma volcano"),
                 ("STRAT", "Stratovolcano"),
                 ("SUBGL", "Subglacial volcano"),
                 ("SUBMA", "Submarine volcano"),
                 ("TUFFC", "Tuff cone"),
                 ("TUFFR", "Tuff ring"),
                 ("UNKNO", "Unknown"),
                 ("VOLCC", "Volcanic complex"),
                 ("VOLCF", "Volcanic field"))
    loc = VolcanoInformation.objects.values_list('vd_inf_loc', flat=True).order_by('vd_inf_loc').distinct()
    evol = VolcanoInformation.objects.values_list('vd_inf_evol', flat=True).order_by('vd_inf_evol').distinct()
    STATUS_ENUM = (("ANTHR", "Anthropology"),
                   ("AR/AR", "Ar/Ar"),
                   ("DENDR", "Dendrochronology"),
                   ("FUMAR", "Fumarolic"),
                   ("HISTO", "Historical"),
                   ("HOLO1", "Holocene"),
                   ("HOLO2", "Holocene?"),
                   ("HOTSP", "Hot Springs"),
                   ("HYDRA", "Hydration Rind"),
                   ("HYDRO", "Hydrophonic"),
                   ("ICECO", "Ice Core"),
                   ("LICHE", "Lichenometry"),
                   ("MAGNE", "Magnetism"),
                   ("PLEIS", "Pleistocene"),
                   ("POTAS", "Potassium-Argon"),
                   ("RADIO", "Radiocarbon"),
                   ("SEISM", "Seismicity"),
                   ("SURFA", "Surface Exposure"),
                   ("TEPHR", "Tephrochronology"),
                   ("THERM", "Thermoluminescence"),
                   ("UNCER", "Uncertain"),
                   ("URANI", "Uranium-series"),
                   ("VARVE", "Varve Count"),
                   ("UNKNO", "Unknown"))
    RTYPE_ENUM = (("BASAL", "Basalt"),
                  ("TETRA", "Tephrit/Trachybasalt"),
                  ("ANBAS", "Andesite/Basaltic-andesite"),
                  ("TRAAN", "Trachyandesite"),
                  ("DACIT", "Dacite"),
                  ("RHYOL", "Rhyolite"),
                  ("TRACH", "Trachyte"),
                  ("PHONO", "Phonolite"),
                  ("PHOTE", "Phonotephrite"),
                  ("FOIDI", "Foidite"),
                  ("UNKNO", "Unknown"))
    lcad_dia = VolcanoInformation.objects.values_list('vd_inf_lcad_dia', flat=True)
  
    # Volcano CAVW number
    vd_inf_cavw = django_filters.ChoiceFilter(
                                      field_name='vd_inf_vd_id__vd_inf_cavw',
                                      label='The current CAVW number',
                                      choices=zip(cavw, cavw),
                                           )

    # Volcano summit elevation
    vd_inf_selev = django_filters.ChoiceFilter(
                                      field_name='vd_inf_vd_id__vd_inf_selev',
                                      label='Summit Elevation',
                                      choices=zip(selev, selev),
                                           )

    # Volcano type
    vd_inf_type = django_filters.ChoiceFilter(
                                      field_name='vd_inf_vd_id__vd_inf_type',
                                      label='Type',
                                      choices=TYPE_ENUM,
                                           )

    # Volcano location
    vd_inf_loc = django_filters.ChoiceFilter(
                                      field_name='vd_inf_vd_id__vd_inf_loc',
                                      label='Geographic location',
                                      choices=zip(loc, loc),
                                           )
    # Volcano volume of edifice
    vd_inf_evol = django_filters.ChoiceFilter(
                                      field_name='vd_inf_vd_id__vd_inf_evol',
                                      label='Volume of edifice',
                                      choices=zip(evol, evol),
                                           )

    # Volcano status
    vd_inf_status = django_filters.ChoiceFilter(
                                      field_name='vd_inf_vd_id__vd_inf_status',
                                      label='Status',
                                      choices=STATUS_ENUM,
                                           )

    # Volcano rtype
    vd_inf_rtype = django_filters.ChoiceFilter(
                                      field_name='vd_inf_vd_id__vd_inf_rtype',
                                      label='RType',
                                      choices=RTYPE_ENUM,
                                           )

    # Diameter of volcano largest caldera
    vd_inf_lcad_dia = django_filters.ChoiceFilter(
                                      field_name='vd_inf_vd_id__vd_inf_lcad_dia',
                                      label='Diameter of largest caldera',
                                      choices=zip(lcad_dia, lcad_dia),
                                           )

    class Meta:
        model = Volcano
        fields = ['vd_name']

        


class EruptionFilter(django_filters.FilterSet):
    """ Defines the search fields for eruption objects """

    # Eruption name
    name = Eruption.objects.values_list('ed_name', flat=True).order_by('ed_name').distinct()

    ed_name = django_filters.ChoiceFilter(
                                     widget=forms.Select, 
                                     label='Eruption name',
                                     field_name='ed_name',
                                     choices=zip(name,name),
                                     )

    # Eruption start time
    stime = Eruption.objects.values_list('ed_stime', flat=True).order_by('ed_stime').distinct()

    ed_stime = django_filters.ChoiceFilter(
                                      widget=forms.Select, 
                                      label='Start time',
                                      field_name='ed_stime',
                                      choices=zip(stime,stime),
                                      )

    # Eruption end time
    etime = Eruption.objects.values_list('ed_etime', flat=True).order_by('ed_etime').distinct()

    ed_etime = django_filters.ChoiceFilter(
                                      widget=forms.Select, 
                                      label='End time',
                                      field_name='ed_etime',
                                      choices=zip(etime,etime),
                                      )

    # Start time year
    year_joined = django_filters.NumberFilter(name='ed_stime', lookup_expr='year')

    # Start time is greater than or equal
    date__gt =  django_filters.DateFilter(name='ed_stime', input_formats=settings.DATE_INPUT_FORMATS, lookup_expr='gte')

    # Start time is less than or equal
    date__lt =  django_filters.DateFilter(name='ed_stime', input_formats=settings.DATE_INPUT_FORMATS, lookup_expr='lte')

    # Volcano name
    name = Volcano.objects.values_list('vd_name', flat=True).order_by('vd_name').distinct()


    vd_name = django_filters.ChoiceFilter(
                                      field_name='vd_id__vd_name',
                                      label='Related volcano',
                                      choices=zip(name, name),
                                           )


    class Meta:
        model = Eruption 
        fields = ['ed_name',
                  'ed_stime', 'ed_etime', 'vd_id']

class FissureFilter(django_filters.FilterSet):
    """ Defines the search fields for fissure objects """

    # Fissure opentime
    """opentime = django_filters.ModelChoiceFilter(
                                     queryset=Fissure.objects.values_list('opentime', flat=True),
                                      widget=forms.Select,
                                      label='Open time',
                                      to_field_name='opentime',
                                      distinct=False,
                                      )
    """
    #opentime1 = Fissure.objects.values_list('opentime', flat=True).distinct()
    opentime1 = Fissure.objects.values_list('opentime', flat=True).order_by('opentime').distinct()

    opentime = django_filters.ChoiceFilter(field_name='opentime',
                                           label = 'Open time',
                                           choices=zip(opentime1, opentime1),
                                           )

    # Year of opening
    year_joined = django_filters.NumberFilter(name='opentime', lookup_expr='year')

    # Opentime is greater than or equal
    date__gt =  django_filters.DateFilter(name='opentime', input_formats=settings.DATE_INPUT_FORMATS, lookup_expr='gte')

    # Opentime is less than or equal
    date__lt =  django_filters.DateFilter(name='opentime', input_formats=settings.DATE_INPUT_FORMATS, lookup_expr='lte')

    # Related eruptions
    stime = Eruption.objects.values_list('ed_stime', flat=True).order_by('ed_stime').distinct()

    ed_stime = django_filters.ChoiceFilter(
                                      field_name='ed_id__ed_stime',
                                      label='Related eruption',
                                      choices=zip(stime, stime),
            #                          lookup_expr='contains',
                                           )

    class Meta:
        model = Fissure
        fields = ['opentime']



class FlowFilter(django_filters.FilterSet):
    """ Defines the search fields for flow objects """

    # Flow id
    flow_id = django_filters.ModelChoiceFilter(
                                     queryset=Flow.objects.values_list('flow_id', flat=True),
                                     widget=forms.Select, label='Flow id',
                                     to_field_name='flow_id',
                                     )

    # Flow start time
    stime1 = Flow.objects.values_list('stime', flat=True).order_by('stime').distinct()

    stime = django_filters.ChoiceFilter(
                                     widget=forms.Select,
                                     label='Start time',
                                     field_name='stime',
                                     choices=zip(stime1,stime1)
                                     )

    # Flow end time
    etime1 = Flow.objects.values_list('etime', flat=True).order_by('etime').distinct()

    etime = django_filters.ChoiceFilter(
                                     widget=forms.Select,
                                     label='End time',
                                     field_name='etime',
                                     choices=zip(etime1,etime1),
                                     )

    # Start time year
    year_joined = django_filters.NumberFilter(name='stime', lookup_expr='year')

    # Start time is greater than or equal
    date__gt =  django_filters.DateFilter(name='stime', input_formats=settings.DATE_INPUT_FORMATS, lookup_expr='gte')

    # Start time is less than or equal
    date__lt =  django_filters.DateFilter(name='stime', input_formats=settings.DATE_INPUT_FORMATS, lookup_expr='lte')

    # Related fissures
    otime = Fissure.objects.values_list('opentime', flat=True).order_by('opentime').distinct()

    opentime = django_filters.ChoiceFilter(
                                      field_name='fissure_id__opentime',
                                      label='Related fissure',
                                      choices=zip(otime, otime),
                                           )

    # Flow volume
    volume = Volume.objects.values_list('value_measured', flat=True).order_by('value_measured').distinct()

    value_measured = django_filters.ChoiceFilter(
                                      field_name='volume_flow_id__value_measured',
                                      label='Volume',
                                      choices=zip(volume, volume),
                                      )

    # Flow gcp number 
    num = MntOrtho.objects.values_list('gcp_num', flat=True).order_by('gcp_num').distinct()

    gcp_num = django_filters.ChoiceFilter(
                                      field_name='mntortho__gcp_num',
                                      label='Gcp number',
                                      choices=zip(num, num),
                                      )


    class Meta:
        model = Flow
        fields = ['flow_id', 'stime', 'etime']


class ConeFilter(django_filters.FilterSet):
    """ Defines the search fields for cone objects """

    # Cone id
    cone_id = django_filters.ModelChoiceFilter(
                                     queryset=Cone.objects.values_list('cone_id', flat=True),
                                     widget=forms.Select, label='Cone id',
                                     to_field_name='cone_id',
                                     )

    # Cone type
    TYPE_ENUM1 = (("STRAT", "Stratocone"),
                 ("SPATT", "Spatter cone"),
                 ("TUFFC", "Tuff cones"),
                 ("CINDE", "Cinder cone"),
                 ("ROOTL", "Rootless cones"))

    cone_type = django_filters.ChoiceFilter(
                                      field_name='cone_type',
                                      label='Type',
                                      choices=TYPE_ENUM1,                                       
                                      )

    # Cone accretion date
    accretion_date1 = Cone.objects.values_list('accretion_date', flat=True).order_by('accretion_date').distinct()

    accretion_date = django_filters.ChoiceFilter(
                                      widget=forms.Select,
                                      label='Date of accretion',
                                      field_name='accretion_date',
                                      choices=zip(accretion_date1, accretion_date1),
                                      )

    # Cone disappearance date
    disappearance_date1 = Cone.objects.values_list('disappearance_date', flat=True).order_by('disappearance_date').distinct()

    disappearance_date = django_filters.ChoiceFilter(
                                      widget=forms.Select,
                                      label='Date of disappearance',
                                      field_name='disappearance_date',
                                      choices=zip(disappearance_date1,disappearance_date1)
                                      )

    # Year of accretion
    year_joined = django_filters.NumberFilter(name='accretion_date', lookup_expr='year')

    # Accretion date is greater than or equal
    date__gt =  django_filters.DateFilter(name='accretion_date', input_formats=settings.DATE_INPUT_FORMATS, lookup_expr='gte')

    # Accretion date is less than or equal
    date__lt =  django_filters.DateFilter(name='accretion_date', input_formats=settings.DATE_INPUT_FORMATS, lookup_expr='lte')


    # Crater diameter
    diameter = Cone.objects.values_list('crater_diameter', flat=True).order_by('crater_diameter').distinct()

    crater_diameter = django_filters.ChoiceFilter(
                                      widget=forms.Select,
                                      label='Crater diameter',
                                      field_name='crater_diameter',
                                      choices=zip(diameter,diameter),
                                      )

    # Related fissure
    otime = Fissure.objects.values_list('opentime', flat=True).order_by('opentime').distinct()

    opentime = django_filters.ChoiceFilter(
                                      field_name='fissure_id__opentime',
                                      label='Related fissure',
                                      choices=zip(otime, otime),
                                           )

    # Cone volume
    volume = Volume.objects.values_list('value_measured', flat=True).order_by('value_measured').distinct()

    value_measured = django_filters.ChoiceFilter(
                                      field_name='volume_cone_id__value_measured',
                                      label='Volume',
                                      choices=zip(volume, volume),
                                      )

    class Meta:
        model = Cone
        fields = ['cone_id']

class TephrasFilter(django_filters.FilterSet):
    """ Defines the search fields for tephras objects """

    # Tephras id
    teph_id = django_filters.ModelChoiceFilter(
                                      queryset=Tephras.objects.values_list('teph_id', flat=True),
                                      widget=forms.Select,
                                      label='Tephras_identifier',
                                      to_field_name='teph_id',
                                      )

    # Tephras accretion date
    accretion_date1 = Tephras.objects.values_list('accretion_date', flat=True).order_by('accretion_date').distinct()

    accretion_date = django_filters.ChoiceFilter(
                                      widget=forms.Select,
                                      label='Date of accretion',
                                      field_name='accretion_date',
                                      choices=zip(accretion_date1, accretion_date1),
                                      )


    # Tephras disappearance date
    disappearance_date1 = Tephras.objects.values_list('disappearance_date', flat=True).order_by('disappearance_date').distinct()

    disappearance_date = django_filters.ChoiceFilter(
                                      widget=forms.Select,
                                      label='Date of disappearance',
                                      field_name='disappearance_date',
                                      choices=zip(disappearance_date1, disappearance_date1),
                                      )


    # Year of accretion
    year_joined = django_filters.NumberFilter(name='accretion_date', lookup_expr='year')

    # Accretion date is greater than or equal
    date__gt =  django_filters.DateFilter(name='accretion_date', input_formats=settings.DATE_INPUT_FORMATS, lookup_expr='gte')

    # Accretion date is less than or equal
    date__lt =  django_filters.DateFilter(name='accretion_date', input_formats=settings.DATE_INPUT_FORMATS, lookup_expr='lte')

    # Tephras granulometry
    GRANULO_ENUM = (("", ""),
                    ("", ""))

    teph_granulometry = django_filters.ChoiceFilter(
                                      field_name='teph_id__teph_granulometry',
                                      label='Granulometry',
                                      choices=GRANULO_ENUM,
                                           )

    # Related fissure
    otime = Fissure.objects.values_list('opentime', flat=True).order_by('opentime').distinct()

    opentime = django_filters.ChoiceFilter(
                                      field_name='fissure_id__opentime',
                                      label='Related fissure',
                                      choices=zip(otime, otime),
                                      )

    # Tephras volume
    volume = Volume.objects.values_list('value_measured', flat=True)

    value_measured = django_filters.ChoiceFilter(
                                      field_name='volume_teph_id__value_measured',
                                      label='Volume',
                                      choices=zip(volume, volume),
                                      )



    class Meta:
        model = Tephras
        fields = ['teph_id', 'accretion_date', 'disappearance_date', 'teph_granulometry']



class SampleFilter(django_filters.FilterSet):
    """ Defines the search fields for sample objects """

    # Sample id
    sample_id = django_filters.ModelChoiceFilter(
                                      queryset=Sample.objects.values_list('sample_id', flat=True),
                                      widget=forms.Select,
                                      label='Sample identifier',
                                      to_field_name='sample_id',
                                      distinct=True,
                                      )

    # Related tephras
    adate = Tephras.objects.values_list('accretion_date', flat=True).order_by('accretion_date').distinct()

    accretion_date = django_filters.ChoiceFilter(
                                      field_name='teph_id__accretion_date',
                                      label='Related tephras',
                                      choices=zip(adate, adate),
                                      )

    # Related cone
    nme = Cone.objects.values_list('name', flat=True).order_by('name').distinct()

    name = django_filters.ChoiceFilter(
                                      field_name='cone_id__name',
                                      label='Related cone',
                                      choices=zip(nme, nme),
                                      )

    # Related flow
    s_time = Flow.objects.values_list('stime', flat=True).order_by('stime').distinct()

    stime = django_filters.ChoiceFilter(
                                      field_name='flow_id__stime',
                                      label='Related flow',
                                      choices=zip(s_time, s_time),
                                      )

    class Meta:
        model = Sample
        fields = '__all__'



class MntOrthoFilter(django_filters.FilterSet):
    """ Defines the search fields for MNT/Ortho objects """

    # DTM/ ORTHO id
    mo_id = django_filters.ModelChoiceFilter(
                                      queryset=MntOrtho.objects.values_list('mo_id', flat=True),
                                      widget=forms.Select,
                                      label='MNT / Ortho identifier',
                                      to_field_name='mo_id',
                                      )

    # DTM/ ORTHO type
    mo_type1 = MntOrtho.objects.values_list('mo_type', flat=True).order_by('mo_type').distinct()

    mo_type = django_filters.ChoiceFilter(
                                      widget=forms.Select,
                                      label='Type',
                                      field_name='mo_type',
                                      choices=zip(mo_type1,mo_type1),
                                      )

    # GCP type
    gcp_type = queryset=MntOrtho.objects.values_list('mo_gcp_type', flat=True).order_by('mo_gcp_type').distinct()

    mo_gcp_type = django_filters.ChoiceFilter(
                                      widget=forms.Select,
                                      label='Type',
                                      field_name='mo_gcp_type',
                                      choices=zip(gcp_type, gcp_type),
                                      )

    # Software used
    SOFTWARE_ENUM = (("PHOTO", "PhotoScan"),
                     ("MICMA", "MicMac"),
                     ("ERDAS", "ERDAS"),
                     ("ARCVI", "ArcView"),
                     ("POIVI", "Poivillier"),
                     ("ENVI", "Envi"),
                     ("GLOBM", "Global Mapper"),
                     ("CLOUD", "Cloud Compare"))


    mo_software = django_filters.ChoiceFilter(
                                      field_name='mo_software',
                                      label='Software',
                                      choices=SOFTWARE_ENUM,
                                      )

    # Related flow
    s_time = Flow.objects.values_list('stime', flat=True).order_by('stime').distinct()

    stime = django_filters.ChoiceFilter(
                                      field_name='flow_ids__stime',
                                      label='Related flow',
                                      choices=zip(s_time, s_time),
                                      )
    # Acquisition method
    VECTOR_ENUM = (("SATEL", "Satellite"),
                   ("AIRPL", "Airplane"),
                   ("WALK", "Walk"),
                   ("ULM", "Ulm"),
                   ("DRONE", "Drone"))


    am_vector = django_filters.ChoiceFilter(
                                      field_name='am_mo_id__am_vector',
                                      label='Acquisition method',
                                      choices=VECTOR_ENUM,
                                      )

    class Meta:
        model = MntOrtho
        fields = ['mo_id']

