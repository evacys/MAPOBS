# coding: utf8

import os
from django.contrib.gis.utils import LayerMapping
from .models import Flow, Fissure, Cone

""" This script does the mapping between shapefiles and the MAPOBS database """

#mapping = {'flow_id':'flow_id', 'geometry':'geometry'}
mapping = {'geometry':'geometry'}

# The flow shapefile location
shp_flow = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'data', '/home/sysop/CouleesOVPF/couleesOVPFvalides.shp')
)

# The fissure shapefile location
shp_fissure = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'data', '/home/sysop/FissuresOVPF/Fusion_fissures.shp')
)

# The cone shapefile location
shp_cone = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'data', '/home/sysop/ConesOVPF/conesOVPF.shp')
)

def run_flow(verbose=True):
    """ Does the mapping between the PostGIS flow entity and the shapefile """
    lm = LayerMapping(
        Flow, shp_flow, mapping,
        transform=True,
    )
    lm.save(strict=True, verbose=verbose)

def run_fissure(verbose=True):
    """ Does the mapping between the PostGIS fissure entity and the shapefile """
    lm = LayerMapping(
        Fissure, shp_fissure, mapping,
        transform=True,
    )
    lm.save(strict=True, verbose=verbose)

def run_cone(verbose=True):
    """ Does the mapping between the PostGIS cone entity and the shapefile """
    lm = LayerMapping(
        Cone, shp_cone, mapping,
        transform=True,
    )
    lm.save(strict=True, verbose=verbose)


