#-*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.gis.db import models
from django.db.models import Manager as GeoManager


class Contact(models.Model):

    # Primary key

    cc_id = models.AutoField("Contact ID", primary_key=True)



    # Other attributes

    cc_code = models.CharField("Contact Code", max_length=15)

    cc_code2 = models.CharField("Contact Code alias", max_length=15, blank=True)

    cc_fname = models.CharField("First name", max_length=30, blank=True)

    cc_lname = models.CharField("Last name", max_length=30, blank=True)

    cc_obs = models.CharField("Observatory", max_length=150, blank=True)

    cc_add1 = models.CharField("Address 1", max_length=60, blank=True)

    cc_add2 = models.CharField("Address 2", max_length=60, blank=True)

    cc_city = models.CharField("City", max_length=50, blank=True)

    cc_state = models.CharField("State", max_length=30, blank=True)

    cc_country = models.CharField("Country", max_length=50, blank=True)

    cc_post = models.CharField("Postal code", max_length=30, blank=True)

    cc_url = models.CharField("Web address", max_length=255, blank=True)

    cc_email = models.CharField("Email", max_length=320, blank=True)

    cc_phone = models.CharField("Phone", max_length=50, blank=True)

    cc_phone2 = models.CharField("Phone 2", max_length=50, blank=True)

    cc_fax = models.CharField("Fax", max_length=60, blank=True)

    cc_com = models.CharField("Comments", max_length=255, blank=True)

    cc_loaddate = models.DateTimeField("Load date, the date the data was"

                                       " entered (in UTC)")



    # Override default table name

    class Meta:

        db_table = 'cc'





class Bibliographic(models.Model):

    # Primary key

    cb_id = models.AutoField("ID, bibliography identifier", primary_key=True)



    # Other attributes

    cb_auth = models.CharField("Authors/Editors", max_length=255)

    cb_year = models.DateTimeField("Publication year")

    cb_title = models.CharField("Title", max_length=255)

    cb_journ = models.CharField("Journal", max_length=255)

    cb_vol = models.CharField("Volume", max_length=20)

    cb_pub = models.CharField("Publisher", max_length=50)

    cb_page = models.CharField("Pages", max_length=30)

    cb_doi = models.CharField("Digital Object Identifier", max_length=20)

    cb_isbn = models.CharField("International Standard Book Number",

                               max_length=13)

    cb_url = models.URLField("Info on the web", max_length=255)

    cb_labadr = models.CharField("Email address of observatory",

                                 max_length=320)

    cb_keywords = models.CharField("Keywords", max_length=255)

    cb_com = models.CharField("Comments", max_length=255)

    cb_loaddate = models.DateTimeField("Load date, the date the data was "

                                       "entered (in UTC)")



    # Foreign key(s)

    cc_load = models.ForeignKey(Contact, null=True,

                                   verbose_name = 'Loading contact',

                                   related_name='cb_cc_load_id',

                                   on_delete=models.CASCADE)



    # Override default table name

    class Meta:

        db_table = 'cb'





class Volcano(models.Model):

    # Primary key

    vd_id = models.AutoField("ID, Volcano Identifier (Index)",

                             primary_key=True)



    # Other attributes

    vd_cavw = models.CharField("The current CAVW number", max_length=15, blank=True, null=True)

    vd_name = models.CharField("Volcano Name (first)", max_length=255, blank=True, null=True)

    vd_name2 = models.CharField("Volcano Name (second)", max_length=255, blank=True, null=True)

    vd_tzone = models.FloatField("Time zone (relative to UTC)", blank=True, null=True)

    vd_mcont = models.CharField("M=Multiple contacts for this volcano",

                                max_length=1, blank=True, null=True)

    vd_com = models.CharField("Comments", max_length=255, blank=True, null=True)

    vd_loaddate = models.DateTimeField("Load date, the date the data was "

                                       "entered (in UTC)", blank=True, null=True)

    vd_pubdate = models.DateTimeField("Publish date, the date the data become "

                                      "public", blank=True, null=True)


    # Geometry field

    geometry = models.PointField(srid=32740, null=True, blank=True)

    objects = GeoManager()


    # Foreign key(s)

    cc_id1 = models.ForeignKey(Contact, null=True, related_name='vd_cc_id1',

                               verbose_name = 'First contact',

                               on_delete=models.CASCADE, blank=True)

    cc_id2 = models.ForeignKey(Contact, null=True, related_name='vd_cc_id2',

                               verbose_name = 'Second contact',

                               on_delete=models.CASCADE, blank=True)

    cc_id3 = models.ForeignKey(Contact, null=True, related_name='vd_cc_id3',

                               verbose_name = 'Third contact',

                               on_delete=models.CASCADE, blank=True)

    cc_id4 = models.ForeignKey(Contact, null=True, related_name='vd_cc_id4',

                               verbose_name = 'Fourth contact',

                               on_delete=models.CASCADE, blank=True)

    cc_id5 = models.ForeignKey(Contact, null=True, related_name='vd_cc_id5',

                               verbose_name = 'Fith contact',

                               on_delete=models.CASCADE, blank=True)

    cc_load = models.ForeignKey(Contact, null=True,

                                   verbose_name = 'Loading contact',

                                   related_name='vd_cc_load_id',

                                   on_delete=models.CASCADE, blank=True)


    # Override default table name

    class Meta:

        db_table = 'vd'





class Observation(models.Model):

    # Primary key

    co_id = models.AutoField("Observation ID", primary_key=True)



    # Other attributes

    co_code = models.CharField("Observation code", max_length=30, default="")

    co_observe = models.TextField("Description")

    co_stime = models.DateTimeField("Start time")

    co_stime_unc = models.DateTimeField("Start time uncertainty")

    co_etime = models.DateTimeField("End time")

    co_etime_unc = models.DateTimeField("End time uncertainty")

    co_com = models.CharField("Comments", max_length=255)

    co_loaddate = models.DateTimeField("Load date, the date the data was "

                                       "entered (in UTC)")

    co_pubdate = models.DateTimeField("Publish date, the date the data become "

                                      "public")

    cb_ids = models.ManyToManyField(Bibliographic, verbose_name = 'Bibliographic reference')



    # Foreign key(s)

    vd = models.ForeignKey(Volcano, null=True, related_name='co_vd_id',

                              verbose_name = 'Related volcano',

                              on_delete=models.CASCADE)

    cc_id = models.ForeignKey(Contact, null=True, related_name='co_cc_id',

                              verbose_name = 'First contact',

                              on_delete=models.CASCADE)

    cc_id2 = models.ForeignKey(Contact, null=True, related_name='co_cc_id2',

                               verbose_name = 'Second contact',

                               on_delete=models.CASCADE)

    cc_id3 = models.ForeignKey(Contact, null=True, related_name='co_cc_id3',

                               verbose_name = 'Third contact',

                               on_delete=models.CASCADE)

    cc_id4 = models.ForeignKey(Contact, null=True, related_name='co_cc_id4',

                               verbose_name = 'Fourth contact',

                               on_delete=models.CASCADE)

    cc_id5 = models.ForeignKey(Contact, null=True, related_name='co_cc_id5',

                               verbose_name = 'Fith contact',

                               on_delete=models.CASCADE)

    cc_load = models.ForeignKey(Contact, null=True,

                                   verbose_name = 'Loading contact',

                                   related_name='co_cc_load_id',

                                   on_delete=models.CASCADE)



    # Override default table name

    class Meta:

        db_table = 'co'





class VolcanoInformation(models.Model):

    # Enumerate table(s)

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

    # Primary key

    vd_inf_id = models.AutoField("ID, volcano information identifier (index)",

                                 primary_key=True)



    # Other attributes

    vd_inf_cavw = models.CharField("CAVW number, the current CAVW number",

                                   max_length=15)

    vd_inf_status = models.CharField(max_length=5,

                                     choices=STATUS_ENUM,

                                     default="UNKNO")

    vd_inf_desc = models.CharField("Short narrative", max_length=255)

    vd_inf_slat = models.FloatField("Summit latitude")

    vd_inf_slon = models.FloatField("Summit longitude")

    vd_inf_selev = models.FloatField("Summit elevation")

    vd_inf_type = models.CharField(max_length=5,

                                   choices=TYPE_ENUM,

                                   default="UNKNO")

    vd_inf_loc = models.CharField("Geographic location", max_length=30)

    vd_inf_rtype = models.CharField(max_length=5,

                                    choices=RTYPE_ENUM,

                                    default="UNKNO")

    vd_inf_evol = models.FloatField("Volume of edifice")

    vd_inf_numcal = models.IntegerField("Number of calderas")

    vd_inf_lcad_dia = models.FloatField("Diameter of largest caldera")

    vd_inf_ycald_lat = models.FloatField("Latitude of youngest caldera")

    vd_inf_ycald_lon = models.FloatField("Longitude of youngest caldera")

    vd_inf_stime = models.DateTimeField("Start time")

    vd_inf_stime_unc = models.DateTimeField("Start time uncertainty")

    vd_inf_etime = models.DateTimeField("End time")

    vd_inf_etime_unc = models.DateTimeField("End time uncertainty")

    vd_inf_com = models.CharField("Comments", max_length=255)

    vd_inf_loaddate = models.DateTimeField("Load date, the date the data was "

                                           "entered (in UTC)")

    vd_inf_pubdate = models.DateTimeField("Publish date, the date the data "

                                          "become public")

    # Foreign key(s)

    vd = models.ForeignKey(Volcano, null=True, related_name='vd_inf_vd_id',

                              verbose_name = 'Related volcano',

                              on_delete=models.CASCADE)

    cc = models.ForeignKey(Contact, null=True, related_name='vd_inf_cc_id',

                              verbose_name = 'First contact',

                              on_delete=models.CASCADE)

    cc_load = models.ForeignKey(Contact, null=True,

                                   verbose_name = 'Loading contact',

                                   related_name='vd_inf_cc_load_id',

                                   on_delete=models.CASCADE)



    # Override default table name

    class Meta:

        db_table = 'vd_inf'





class Eruption(models.Model):

    # Primary key

    ed_id = models.AutoField("ID, eruption identifier (index)",

                             primary_key=True)



    # Other attributes

    ed_code = models.CharField("EruptionCode", max_length=30, null=True)

    ed_name = models.CharField("EruptionName", max_length=60, null=True)

    ed_nar = models.CharField("Narrative", max_length=255, null=True)

    ed_stime = models.DateTimeField("Start time", null=True)

    ed_stime_bc = models.IntegerField("Year of start time before Christ", null=True)

    ed_stime_unc = models.DateTimeField("Start time uncertainty", null=True)

    ed_etime = models.DateTimeField("End time", null=True)

    ed_etime_bc = models.IntegerField("Year of end time before Christ", null=True)

    ed_etime_unc = models.DateTimeField("End time uncertainty", null=True)

    ed_climax = models.DateTimeField("Onset of climax", null=True)

    ed_climax_bc = models.IntegerField("Year of climax time before Christ", null=True)

    ed_climax_unc = models.DateTimeField("Onset of climax uncertainty", null=True)

    ed_com = models.CharField("Comments", max_length=255, null=True)

    ed_loaddate = models.DateTimeField("Load date, the date the data was "

                                       "entered (in UTC)", null=True)

    ed_pubdate = models.DateTimeField("Publish date, the date the data become "

                                      "public", null=True)

    cb_ids = models.ManyToManyField(Bibliographic, verbose_name='Bibliographic reference')



    # Foreign key(s)

    vd = models.ForeignKey(Volcano, null=True, related_name='ed_vd_id',

                              verbose_name = 'Related volcano',

                              on_delete=models.CASCADE)

    cc_id = models.ForeignKey(Contact, null=True, related_name='ed_cc_id',

                              verbose_name = 'First contact',

                              on_delete=models.CASCADE)

    cc_id2 = models.ForeignKey(Contact, null=True, related_name='ed_cc_id2',

                               verbose_name = 'Second contact',

                               on_delete=models.CASCADE)

    cc_id3 = models.ForeignKey(Contact, null=True, related_name='ed_cc_id3',

                               verbose_name = 'Third contact',

                               on_delete=models.CASCADE)

    cc_load = models.ForeignKey(Contact, null=True,

                                   verbose_name = 'Loading contact',

                                   related_name='ed_cc_load_id',

                                   on_delete=models.CASCADE)



    # Override default table name

    class Meta:

        db_table = 'ed'


class SeismicEvent(models.Model):

    # Primary key

    sd_ev_id = models.AutoField("ID, Seismic event identifier (index)",

                             primary_key=True)


    # Other attributes

    sd_ev_code = models.CharField("Seismic event code", max_length=30, null=True)

    sd_ev_stime = models.DateTimeField("Start time", null=True)

    sd_ev_stime_bc = models.IntegerField("Year of start time before Christ", null=True)

    sd_ev_stime_unc = models.DateTimeField("Start time uncertainty", null=True)

    sd_ev_etime = models.DateTimeField("End time", null=True)

    sd_ev_etime_bc = models.IntegerField("Year of end time before Christ", null=True)

    sd_ev_etime_unc = models.DateTimeField("End time uncertainty", null=True)

    sd_ev_com = models.CharField("Comments", max_length=255, null=True)

    sd_ev_loaddate = models.DateTimeField("Load date, the date the data was "

                                       "entered (in UTC)", null=True)

    sd_ev_pubdate = models.DateTimeField("Publish date, the date the data become "

                                      "public", null=True)

    cb_ids = models.ManyToManyField(Bibliographic, verbose_name = 'Bibliographic reference')



    # Foreign key(s)

    ed = models.ForeignKey(Eruption, null=True, related_name='sd_ev_ed_id',

                              on_delete=models.CASCADE)

    cc_id = models.ForeignKey(Contact, null=True, related_name='sd_ev_cc_id',

                              verbose_name = 'First contact',

                              on_delete=models.CASCADE)

    cc_id2 = models.ForeignKey(Contact, null=True, related_name='sd_ev_cc_id2',

                               verbose_name = 'Second contact',

                               on_delete=models.CASCADE)

    cc_id3 = models.ForeignKey(Contact, null=True, related_name='sd_ev_cc_id3',

                               verbose_name = 'Third contact',

                               on_delete=models.CASCADE)

    cc_load = models.ForeignKey(Contact, null=True,

                                   verbose_name = 'Loading contact',

                                   related_name='sd_ev_cc_load_id',

                                   on_delete=models.CASCADE)

    # Override default table name

    class Meta:

        db_table = 'sd_ev'



class EruptionObservation(models.Model):

    # Primary key

    eo_id = models.AutoField("ID, Eruption Observation identifier", primary_key=True)

    # Other attributes

    eo_code = models.CharField("Observation code", max_length=30, null=True)

    eo_observe = models.TextField("Description")

    eo_stime = models.DateTimeField("Start time")

    eo_stime_unc = models.DateTimeField("Start time uncertainty")

    eo_etime = models.DateTimeField("End time")

    eo_etime_unc = models.DateTimeField("End time uncertainty")

    eo_com = models.CharField("Comments", max_length=255)

    eo_loaddate = models.DateTimeField("Load date, the date the data was "

                                       "entered (in UTC)")

    eo_pubdate = models.DateTimeField("Publish date, the date the data become "

                                      "public")

    cb_ids = models.ManyToManyField(Bibliographic, verbose_name = 'Bibliographic reference')



    # Foreign key(s)

    ed = models.ForeignKey(Eruption, null=True, related_name='eo_ed_id',

                              on_delete=models.CASCADE)

    cc_id = models.ForeignKey(Contact, null=True, related_name='eo_cc_id',

                              verbose_name = 'First contact',

                              on_delete=models.CASCADE)

    cc_id2 = models.ForeignKey(Contact, null=True, related_name='eo_cc_id2',

                               verbose_name = 'Second contact',

                               on_delete=models.CASCADE)

    cc_id3 = models.ForeignKey(Contact, null=True, related_name='eo_cc_id3',

                               verbose_name = 'Third contact',

                               on_delete=models.CASCADE)

    cc_id4 = models.ForeignKey(Contact, null=True, related_name='eo_cc_id4',

                               verbose_name = 'Fourth contact',

                               on_delete=models.CASCADE)

    cc_id5 = models.ForeignKey(Contact, null=True, related_name='eo_cc_id5',

                               verbose_name = 'Fith contact',

                               on_delete=models.CASCADE)

    cc_load = models.ForeignKey(Contact, null=True,

                                   verbose_name = 'Loading contact',

                                   related_name='eo_cc_load_id',

                                   on_delete=models.CASCADE)



    # Override default table name

    class Meta:

        db_table = 'eo'



class Fissure(models.Model):

    # Primary key

    fissure_id = models.AutoField("ID, fissure identifier", primary_key=True)



    # Other attributes

    opentime = models.DateTimeField("Open time", null=True, blank=True)

    opentime_bc = models.IntegerField("Year of open time before Christ", null=True, blank=True)

    opentime_unc = models.DateTimeField("Open time uncertainty", null=True, blank=True)

    com = models.CharField("Comments", max_length=255, null=True, blank=True)

    com2 = models.CharField("Comments2", max_length=255, null=True, blank=True)

    com3 = models.CharField("Comments3", max_length=255, null=True, blank=True)

    com4 = models.CharField("Comments4", max_length=255, null=True, blank=True)

    com5 = models.CharField("Comments5", max_length=255, null=True, blank=True)

    com6 = models.CharField("Comments6", max_length=255, null=True, blank=True)

    loaddate = models.DateTimeField("Load date, the date the data was "

                                    "entered (in UTC)", null=True, blank=True)

    pubdate = models.DateTimeField("Publish date, the date the data become "

                                   "public", null=True, blank=True)

    cb_ids = models.ManyToManyField(Bibliographic, blank=True, verbose_name = 'Bibliographic reference')



    # Foreign key(s)

    ed = models.ForeignKey(Eruption, null=True,

                              verbose_name = 'Related eruption',

                              related_name='fissure_ed_id',

                              on_delete=models.CASCADE, blank=True)

    cc_load = models.ForeignKey(Contact, null=True,

                                   verbose_name = 'Loading contact',

                                   related_name='fissure_cc_load_id',

                                   on_delete=models.CASCADE, blank=True)

    cc_pub = models.ForeignKey(Contact, null=True,

                                  verbose_name = 'Contact that published the data',

                                  related_name='fissure_cc_pub_id',

                                  on_delete=models.CASCADE, blank=True)


    # Geometry field

    geometry = models.MultiLineStringField(srid=32740, null=True, blank=True)

    objects = GeoManager()

    # Override default table name

    class Meta:

        db_table = 'fissure'





class Cone(models.Model):

    # Enumerate table(s)

    TYPE_ENUM = (("STRAT", "Stratocone"),

                 ("SPATT", "Spatter cone"),

                 ("TUFFC", "Tuff cones"),

                 ("CINDE", "Cinder cone"),

                 ("ROOTL", "Rootless cones"))



    # Primary key

    cone_id = models.AutoField("ID, cone identifier", primary_key=True)



    # Other attributes

    name = models.CharField("Cone Name", max_length=60, null=True, blank=True)

    cone_type = models.CharField(max_length=5,

                                 choices=TYPE_ENUM, null=True, blank=True)

    height = models.FloatField("Height of the cone", null=True, blank=True)

    accretion_date = models.DateTimeField("Date of accretion", null=True, blank=True)

    accretion_date_bc = models.IntegerField("Year of accretion date before "

                                            "Christ", null=True, blank=True)

    accretion_date_unc = models.DateTimeField("Accretion date uncertainty", null=True, blank=True)

    disappearance_date = models.DateTimeField("Date of disappearance", null=True, blank=True)

    disappearance_date_bc = models.IntegerField("Year of disappearance date "

                                                "before Christ", null=True, blank=True)

    disappearance_date_unc = models.DateTimeField("Disappearance date "

                                                  "uncertainty", null=True, blank=True)

    crater_diameter = models.FloatField("Crater diameter", null=True, blank=True)

    com = models.CharField("Date comment", max_length=255, blank=True, null=True)

    com2 = models.CharField("Comments", max_length=255, blank=True, null=True)

    com3 = models.CharField("Author comments", max_length=255, blank=True, null=True)

    loaddate = models.DateTimeField("Load date, the date the data was entered "

                                    "(in UTC)", null=True, blank=True)

    pubdate = models.DateTimeField("Publish date, the date the data become "

                                   "public", null=True, blank=True)

    cb_ids = models.ManyToManyField(Bibliographic, blank=True, verbose_name = 'Bibliographic reference')


    # Geometry field

    geometry = models.MultiPolygonField(srid=32740, null=True, blank=True)

    objects = GeoManager()


    # Foreign key(s)

    fissure = models.ForeignKey(Fissure, null=True,

                                   verbose_name = 'Related fissure',

                                   related_name='cone_fissure_id',

                                   on_delete=models.CASCADE,

                                   blank=True)

    cc_load = models.ForeignKey(Contact, null=True,

                                   verbose_name = 'Loading contact',

                                   related_name='cone_cc_load_id',

                                   on_delete=models.CASCADE,

                                   blank=True)

    cc_pub = models.ForeignKey(Contact, null=True,

                                  verbose_name = 'Contact that published the data',

                                  related_name='cone_cc_pub_id',

                                  on_delete=models.CASCADE,
 
                                  blank=True)



    # Override default table name

    class Meta:

        db_table = 'cone'





class Tephras(models.Model):

    # Enumerate table(s)

    GRANULO_ENUM = (("", ""),

                    ("", ""))



    # Primary key

    teph_id = models.AutoField("ID, tephras identifier", primary_key=True)



    # Other attributes

    accretion_date = models.DateTimeField("Date of accretion")

    accretion_date_bc = models.IntegerField("Year of accretion date before "

                                            "Christ")

    accretion_date_unc = models.DateTimeField("Accretion date uncertainty")

    disappearance_date = models.DateTimeField("Date of disappearance")

    disappearance_date_bc = models.IntegerField("Year of disappearance date "

                                                "before Christ")

    disappearance_date_unc = models.DateTimeField("Disappearance date "

                                                  "uncertainty")

    teph_granulometry = models.CharField(max_length=5,

                                         choices=GRANULO_ENUM)

    com = models.CharField("Comments", max_length=255)

    loaddate = models.DateTimeField("Load date, the date the data was entered "

                                    "(in UTC)")

    pubdate = models.DateTimeField("Publish date, the date the data become "

                                   "public")

    cb_ids = models.ManyToManyField(Bibliographic, verbose_name = 'Bibliographic reference')



    # Geometry field

    geometry = models.PointField(srid=32740, null=True, blank=True)


    # Foreign key(s)

    fissure = models.ForeignKey(Fissure, null=True,

                                   verbose_name = 'Related fissure',

                                   related_name='teph_fissure_id',

                                   on_delete=models.CASCADE)

    cc_load = models.ForeignKey(Contact, null=True,

                                   verbose_name = 'Loading contact',

                                   related_name='teph_cc_load_id',

                                   on_delete=models.CASCADE)

    cc_pub = models.ForeignKey(Contact, null=True,

                                  verbose_name = 'Contact that published the data',

                                  related_name='teph_cc_pub_id',

                                  on_delete=models.CASCADE)



    # Override default table name

    class Meta:

        db_table = 'teph'





class Flow(models.Model):

    # Primary key

    flow_id = models.AutoField("ID, flow identifier", primary_key=True)



    # Other attributes

    stime = models.DateTimeField("Start time", null=True)

    stime_bc = models.IntegerField("Year of start time before Christ", null=True)

    stime_unc = models.DateTimeField("Start time uncertainty", null=True)

    etime = models.DateTimeField("End time", null=True)

    etime_bc = models.IntegerField("Year of end time before Christ", null=True)

    etime_unc = models.DateTimeField("End time uncertainty", null=True)

    final_vers = models.BooleanField("1 if it's the final version, else 0",

                                        default=False)

    flux = models.FloatField("Flux", null=True)

    com = models.CharField("Comments", max_length=255, null=True)

    loaddate = models.DateTimeField("Load date, the date the data was entered "

                                    "(in UTC)", null=True)

    pubdate = models.DateTimeField("Publish date, the date the data become "

                                   "public", null=True)

    cb_ids = models.ManyToManyField(Bibliographic, verbose_name = 'Bibliographic reference')


    # Geometry field
  
    geometry = models.MultiPolygonField(srid=32740, null=True, blank=True)

    objects = GeoManager()


    # Foreign key(s)

    fissure = models.ForeignKey(Fissure, null=True,

                                   verbose_name = 'Related fissure',

                                   related_name='flow_fissure_id',

                                   on_delete=models.CASCADE)

    cc_load = models.ForeignKey(Contact, null=True,

                                   verbose_name = 'Loading contact',

                                   related_name='flow_cc_load_id',

                                   on_delete=models.CASCADE)

    cc_pub = models.ForeignKey(Contact, null=True,

                                  verbose_name = 'Contact that published the data',

                                  related_name='flow_cc_pub_id',

                                  on_delete=models.CASCADE)



    # Override default table name

    class Meta:

        db_table = 'flow'




class Volume(models.Model):

    # Enumerate table(s)

    METHOD_ENUM = (("TOPO", "Topographic"),

                   ("TADRT", "TADR Turin"),

                   ("TADRC", "TADR Clermont"),

                   ("GAZ", "Gaz"))



    # Primary key

    volume_id = models.AutoField("ID, volume identifier", primary_key=True)



    # Other attributes

    value_measured = models.FloatField("value measured", null=True)

    value_calculated = models.FloatField("value calculated", null=True)

    volume_method = models.CharField(max_length=5,

                                     choices=METHOD_ENUM, null=True)

    com = models.CharField("Comments", max_length=255, null=True)

    loaddate = models.DateTimeField("Load date, the date the data was entered "

                                    "(in UTC)", null=True)

    pubdate = models.DateTimeField("Publish date, the date the data become "

                                   "public", null=True)

    cb_ids = models.ManyToManyField(Bibliographic, verbose_name = 'Bibliographic reference')



    # Foreign key(s)

    teph = models.ForeignKey(Tephras, null=True,

                                verbose_name = 'Related tephras',

                                related_name='volume_teph_id',

                                on_delete=models.CASCADE,
                               
                                blank=True)

    cone = models.ForeignKey(Cone, null=True,

                                verbose_name = 'Related cone',

                                related_name='volume_cone_id',

                                on_delete=models.CASCADE,
                               
                                blank=True)

    flow = models.ForeignKey(Flow, null=True,

                                verbose_name = 'Related flow',

                                related_name='volume_flow_id',

                                on_delete=models.CASCADE,
                               
                                blank=True)

    cc_load = models.ForeignKey(Contact, null=True,

                                   verbose_name = 'Loading contact',

                                   related_name='volume_cc_load_id',

                                   on_delete=models.CASCADE)

    cc_pub = models.ForeignKey(Contact, null=True,

                                  verbose_name = 'Contact that published the data',

                                  related_name='volume_cc_pub_id',

                                  on_delete=models.CASCADE)



    # Override default table name

    class Meta:

        db_table = 'volume'





class Sample(models.Model):

    # Primary key

    sample_id = models.AutoField("ID, identifier", primary_key=True)

    sample_code = models.CharField("Code", max_length=30, default='Null')

    sample_location = models.CharField("Location", max_length=255, default='Null')

    sample_elevation = models.FloatField("Elevation", default='Null')

    sample_date = models.DateTimeField("Sample date")

    sample_samplingtime = models.DateTimeField("Sampling time")

    sample_type = models.CharField("Type", max_length=5, default='Null')

    sample_collection_method = models.CharField("Collection method", max_length=5, default='Null')

    sample_collection_tool = models.CharField("Collection tool", max_length=5, default='Null')

    sample_size = models.FloatField("Size", default='Null')

    sample_weight = models.FloatField("Weight", default='Null')

    sample_texture = models.CharField("Texture", max_length=255, default='Null')

    sample_geological_age = models.DateTimeField("Geological age")

    sample_geological_unit = models.CharField("Geological unit", max_length=10, default='Null')

    sample_gsn_rock = models.IntegerField("IGSN number", default='Null')

    sample_label_rock = models.CharField("Label unit", max_length=30, default='Null')

    sample_photo = models.URLField("URL link", max_length=255, default='Null')


    # Other attributes

    cb_ids = models.ManyToManyField(Bibliographic, verbose_name = 'Bibliographic reference')


    # Foreign keys

    teph = models.ForeignKey(Tephras, null=True,

                                verbose_name = 'Related tephras',

                                related_name='sample_teph_id',

                                on_delete=models.CASCADE)

    cone = models.ForeignKey(Cone, null=True,

                                verbose_name = 'Related cone',

                                related_name='sample_cone_id',

                                on_delete=models.CASCADE)

    flow = models.ForeignKey(Flow, null=True,

                                verbose_name = 'Related flow',

                                related_name='sample_flow_id',

                                on_delete=models.CASCADE)

    cc_load = models.ForeignKey(Contact, null=True,

                                   verbose_name = 'Loading contact',

                                   related_name='sample_cc_load_id',

                                   on_delete=models.CASCADE)

    cc_pub = models.ForeignKey(Contact, null=True,

                                  verbose_name = 'Contact that published the data',

                                  related_name='sample_cc_pub_id',

                                  on_delete=models.CASCADE)


    #Override default table name

    class Meta:

        db_table = 'sample'



class Petrology(models.Model):

    # Primary key

    petro_id = models.AutoField("ID, petrology identifier", primary_key=True)



    # Other attributes

    cb_ids = models.ManyToManyField(Bibliographic, verbose_name = 'Bibliographic reference')



    # Foreign key(s)

    sample = models.ForeignKey(Sample, null=True,

                                verbose_name = 'Related sample',

                                related_name='petro_sample_id',

                                on_delete=models.CASCADE)


    cc_load = models.ForeignKey(Contact, null=True,

                                   verbose_name = 'Loading contact',

                                   related_name='petro_cc_load_id',

                                   on_delete=models.CASCADE)

    cc_pub = models.ForeignKey(Contact, null=True,

                                  verbose_name = 'Contact that published the data',

                                  related_name='petro_cc_pub_id',

                                  on_delete=models.CASCADE)



    # Override default table name

    class Meta:

        db_table = 'petro'





class Composition(models.Model):

    # Primary key

    compo_id = models.AutoField("ID, composition identifier", primary_key=True)



    # Other attributes

    cb_ids = models.ManyToManyField(Bibliographic, verbose_name = 'Bibliographic reference')



    # Foreign key(s)

    sample = models.ForeignKey(Sample, null=True,

                                verbose_name = 'Related sample',

                                related_name='compo_sample_id',

                                on_delete=models.CASCADE)


    cc_load = models.ForeignKey(Contact, null=True,

                                   verbose_name = 'Loading contact',

                                   related_name='compo_cc_load_id',

                                   on_delete=models.CASCADE)

    cc_pub = models.ForeignKey(Contact, null=True,

                                  verbose_name = 'Contact that published the data',

                                  related_name='compo_cc_pub_id',

                                  on_delete=models.CASCADE)



    # Override default table name

    class Meta:

        db_table = 'compo'


class SatelliteAirplane(models.Model):

    # Enumerate table(s)

    TYPE_ENUM = (("S", "Satellite"),

                 ("A", "Airplane"))

    ORI_ENUM = (("D", "digitized/Bibliography"),

                ("O", "Original from observatory"))



    # Primary key

    cs_id = models.AutoField("ID, satellite airplane identifier",

                             primary_key=True)



    # Other attributes

    cs_code = models.CharField("Code", max_length=40)

    cs_type = models.CharField(max_length=5,

                               choices=TYPE_ENUM)

    cs_name = models.CharField("Name", max_length=50)

    stime = models.DateTimeField("Start time")

    stime_unc = models.DateTimeField("Start time uncertainty")

    etime = models.DateTimeField("End time")

    etime_unc = models.DateTimeField("End time uncertainty")

    desc = models.CharField("Description", max_length=255)

    cs_ori = models.CharField(max_length=5,

                              choices=ORI_ENUM)

    com = models.CharField("Comments", max_length=255)

    loaddate = models.DateTimeField("Load date, the date the data was entered "

                                    "(in UTC)")

    pubdate = models.DateTimeField("Publish date, the date the data become "

                                   "public")

    cb_ids = models.ManyToManyField(Bibliographic, verbose_name = 'Bibliographic reference')



    # Foreign key(s)

    cc_load = models.ForeignKey(Contact, null=True,

                                   verbose_name = 'Loading contact',

                                   related_name='cs_cc_load_id',

                                   on_delete=models.CASCADE)

    cc_pub = models.ForeignKey(Contact, null=True,

                                  verbose_name = 'Contact that published the data',

                                  related_name='cs_cc_pub_id',

                                  on_delete=models.CASCADE)



    # Override default table name

    class Meta:

        db_table = 'cs'




class AcquisitionMethod(models.Model):

    # Enumerate table(s)

    VECTOR_ENUM = (("SATEL", "Satellite"),

                   ("AIRPL", "Airplane"),

                   ("WALK", "Walk"),

                   ("ULM", "Ulm"),

                   ("DRONE", "Drone"))



    # Primary key

    am_id = models.AutoField("ID, acquisition method identifier",

                             primary_key=True)



    # Other attributes

    stime = models.DateTimeField("Start time")

    stime_unc = models.DateTimeField("Start time uncertainty")

    etime = models.DateTimeField("End time")

    etime_unc = models.DateTimeField("End time uncertainty")

    am_vector = models.CharField(max_length=5,

                                 choices=VECTOR_ENUM)

    desc = models.CharField("Description", max_length=255)

    com = models.CharField("Comments", max_length=255)

    loaddate = models.DateTimeField("Load date, the date the data was entered "

                                    "(in UTC)")

    pubdate = models.DateTimeField("Publish date, the date the data become "

                                   "public")

    cb_ids = models.ManyToManyField(Bibliographic, verbose_name = 'Bibliographic reference')



    # Foreign key(s)

    cs = models.ForeignKey(SatelliteAirplane, null=True,

                              verbose_name = 'Related satellite/ airplane',

                              related_name='am_cs_id',

                              on_delete=models.CASCADE, blank=True)


    cc_load = models.ForeignKey(Contact, null=True,

                                   verbose_name = 'Loading contact',

                                   related_name='am_cc_load_id',

                                   on_delete=models.CASCADE)

    cc_pub = models.ForeignKey(Contact, null=True,

                                  verbose_name = 'Contact that published the data',

                                  related_name='am_cc_pub_id',

                                  on_delete=models.CASCADE)



    # Override default table name

    class Meta:

        db_table = 'am'




class MntOrtho(models.Model):

    # Enumerate table(s)

    TYPE_ENUM = (("MNT", "Mnt"),

                 ("ORTHO", "Orthophoto"))

    GCP_TYPE_ENUM = (("GNSSM", "GNSS measure"),

                     ("RIMAG", "Replicated image"))

    SOFTWARE_ENUM = (("PHOTO", "PhotoScan"),

                     ("MICMA", "MicMac"),

                     ("ERDAS", "ERDAS"),

                     ("ARCVI", "ArcView"),

                     ("POIVI", "Poivillier"),

                     ("ENVI", "Envi"),

                     ("GLOBM", "Global Mapper"),

                     ("CLOUD", "Cloud Compare"))



    # Primary key

    mo_id = models.AutoField("ID, mntOrtho identifier", primary_key=True)



    # Other attributes

    gcp_num = models.IntegerField("Gcp number", null=True, blank=True)

    reference_altitude = models.FloatField("Reference altitude", null=True, blank=True)

    precision = models.FloatField("Accuracy of the reference altitude", null=True, blank=True)

    mo_type = models.CharField(max_length=5,

                               choices=TYPE_ENUM, null=True, blank=True)

    mo_gcp_type = models.CharField(max_length=5,

                                   choices=GCP_TYPE_ENUM, null=True, blank=True)

    mo_software = models.CharField(max_length=5,

                                   choices=SOFTWARE_ENUM, null=True, blank=True)

    com = models.CharField("Comments", max_length=255, null=True, blank=True)

    loaddate = models.DateTimeField("Load date, the date the data was entered "

                                    "(in UTC)", null=True, blank=True)

    pubdate = models.DateTimeField("Publish date, the date the data become "

                                   "public", null=True, blank=True)

    cb_ids = models.ManyToManyField(Bibliographic, blank=True, verbose_name = 'Bibliographic reference')

    flow_ids = models.ManyToManyField(Flow, blank=True, verbose_name='Related flows')

    raster = models.RasterField(srid=32740, null=True, blank=True, verbose_name='Related raster')



    # Foreign key(s)

    am= models.ForeignKey(AcquisitionMethod, null=True,

                                   verbose_name = 'Acquisition method',

                                   related_name='mo_am_id',

                                   on_delete=models.CASCADE, blank=True)


    cc_load = models.ForeignKey(Contact, null=True,

                                   verbose_name = 'Loading contact',

                                   related_name='mo_cc_load_id',

                                   on_delete=models.CASCADE, blank=True)

    cc_pub = models.ForeignKey(Contact, null=True,

                                  verbose_name = 'Contact that published the data',

                                  related_name='mo_cc_pub_id',

                                  on_delete=models.CASCADE, blank=True)



    # Override default table name

    class Meta:

        db_table = 'mo'




class AcquisitionTool(models.Model):

    # Primary key

    at_id = models.AutoField("ID, acquisition tool identifier",

                             primary_key=True)



    # Other attributes

    cam = models.CharField("Camera", max_length=255)

    resolution_cam = models.FloatField("Camera resolution")

    optical = models.IntegerField("optical number")

    resolution_ground = models.FloatField("ground resolution")

    com = models.CharField("Comments", max_length=255)

    loaddate = models.DateTimeField("Load date, the date the data was entered "

                                    "(in UTC)")

    pubdate = models.DateTimeField("Publish date, the date the data become "

                                   "public")

    cb_ids = models.ManyToManyField(Bibliographic, verbose_name = 'Bibliographic reference')

    am_ids = models.ManyToManyField(AcquisitionMethod, verbose_name='Acquisition method')



    # Foreign key(s)

    cc_load = models.ForeignKey(Contact, null=True,

                                   verbose_name = 'Loading contact',

                                   related_name='at_cc_load_id',

                                   on_delete=models.CASCADE)

    cc_pub = models.ForeignKey(Contact, null=True,

                                  verbose_name = 'Contact that published the data',

                                  related_name='at_cc_pub_id',

                                  on_delete=models.CASCADE)



    # Override default table name

    class Meta:

        db_table = 'at'
