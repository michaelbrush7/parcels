#!/usr/bin/env python
# coding: utf-8

# In[71]:


import requests
import pandas as pd
from shapely.geometry import Polygon
from pyproj import Geod


# In[72]:


#pyproj.get_ellps_map()


# In[ ]:


# Function to handle geometric transformations
def transform_geo(df):
    
    # Convert geometry rings into polygons
    df["geometry"] = df["geometry.rings"].apply(lambda x: Polygon(x[0]))
    
    # Calculate the area of each polygon
    geod = Geod(ellps='WGS84')
    df["area"] = df["geometry"].apply(lambda x: abs(geod.geometry_area_perimeter(x)[0]))
    
    return df


# In[ ]:


# Function to categorize ownership
def transform_own(df):
    df["owner_cat"] = 'other'
    df.loc[((df['OWNER_NAME'].str.contains('LLC') == True) | (df['OWNER_NAME'].str.contains('L L C'))), 'owner_cat'] = 'llc'
    df.loc[(df['OWN_ADD'] == df['PROP_ADD']), 'owner_cat'] = 'owner_occupy'
    return df


# In[73]:


# Function to get data from a URL and store to a csv file
def retrieve_county_data(aURL, aOutFile):
    # retrieve data to a dataframe
    s = requests.get(aURL).json()
    df = pd.json_normalize(s, record_path="features")
    df.columns = df.columns.str.lstrip('attributes.')
    
    # Data Carpentry
    
    # Standardize Case where needed
    df.loc[:, df.columns != 'geometry.rings'].apply(lambda x: x.astype(str).str.lower())
    
    
    transform_geo(df)
    
    # Categorize owner type
    # - owner_occupy: owner address matches property
    # - llc: owner name includes llc or similar. most likely individual landlords?
    # - commercial: appears to be a commercial entity
    # - other: Unable to determine owner type
    transform_own(df)
    
    # Write data to a file
    df.to_csv(aOutFile, index_label = 'index')
    #print(df)


# In[70]:


#url = "https://maps.stlouisco.com/arcgis/rest/services/OpenData/OpenData/FeatureServer/7/query?where=PROPCLASS%20%3D%20'R'&outFields=*&geometry=-90.458%2C38.722%2C-90.384%2C38.746&geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelContains&outSR=4326&f=json"
#url = "https://maps.stlouisco.com/arcgis/rest/services/OpenData/OpenData/FeatureServer/7/query?where=1%3D1&outFields=*&geometry=-90.412%2C38.728%2C-90.403%2C38.731&geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelContains&outSR=4326&f=json"
#retrieve_county_data(url, "./data/parcels/stl_county_test_set.csv")


# ```
# {'objectIdFieldName': 'OBJECTID',
#  'globalIdFieldName': '',
#  'geometryType': 'esriGeometryPolygon',
#  'spatialReference': {'wkid': 4326, 'latestWkid': 4326},
#  'fields': [
#   {'name': 'OBJECTID',
#    'alias': 'OBJECTID',
#    'type': 'esriFieldTypeOID'},
#   {'name': 'PARENT_LOC',
#    'alias': 'PARENT_LOC',
#    'type': 'esriFieldTypeString',
#    'length': 9},
#   {'name': 'LOCATOR',
#    'alias': 'LOCATOR',
#    'type': 'esriFieldTypeString',
#    'length': 9},
#   {'name': 'TAXYR', 'alias': 'TAXYR', 'type': 'esriFieldTypeSmallInteger'},
#   ...],
#  'features': [{'attributes': {'OBJECTID': 1,
#     'PARENT_LOC': '10E620112',
#     'LOCATOR': '10E620112',
#     'TAXYR': 2022,
#     'OWNER_NAME': 'ADOLPHUS MARK FAMILY TRUST ETAL',
#     'PROP_ADRNUM': '1161',
#     'PROP_ADD': '1161 DUNN RD',
#     'PROP_ZIP': '63138',
#     'OWN_ADD': '17930 N 93RD WAY',
#     'OWN_CITY': 'SCOTTSDALE',
#     'OWN_STATE': 'AZ',
#     'OWN_ZIP': '85255',
#     'SCHSUB': '139WW',
#     'MUNYCODE': '000',
#     'SUBDIVISION': None,
#     'TAXCODE': 'A',
#     'ASSTLANDVAL': 12540,
#     'ASSTIMPVAL': 0,
#     'TOTASSMT': 12540,
#     'APPLANDVAL': 39200,
#     'APPIMPVAL': 0,
#     'TOTAPVAL': 39200,
#     'PROPCLASS': 'C',
#     'LUC': '910',
#     'LANDUSE2': '910',
#     'LUCODE': 'Vacant/Agriculture',
#     'TENURE': 'NOT OWNER',
#     'LIVUNIT': 0,
#     'YEARBLT': 0,
#     'RESQFT': 0,
#     'COMSTRUC': 0,
#     'DEEDBKPG': '23433-259',
#     'RECDATEDAILY': None,
#     'ASRBKPG': '08 0756 B',
#     'DEEDTYPE': None,
#     'ACRES': 0.2,
#     'BLOCKNUM': None,
#     'LOTNUM': None,
#     'LOTDIM': '0183/0276 0100/0035',
#     'LOTFRONT': None,
#     'LOTDEPTH': None,
#     'LEGAL': 'SURVEY 112-47-7',
#     'CAREOF': None,
#     'NBHD': 'C01NORTH',
#     'LANDUSE3': None,
#     'BLDGNAME': ' ',
#     'TWP': 'SF',
#     'TWPNAME': 'ST. FERDINAND',
#     'MUNICIPALITY': 'UNINCORPORATED',
#     'COUNTY_COUNCIL': 4,
#     'FIRE_DISTRICT': 'SPANISH LAKE',
#     'SCHOOLCODE': 139,
#     'SCHOOL_DISTRICT': 'HAZELWOOD',
#     'SPECIAL_SCHOOL': 1,
#     'JR_COLLEGE': 1,
#     'LIBRARY_DISTRICT': 'ST LOUIS COUNTY',
#     'LIGHT_DISTRICT': None,
#     'MUNI_WARD': None,
#     'STATE_REP': 66,
#     'STATE_SENATE': 13,
#     'US_CONGRESS': 1,
#     'CENSUS_TRACT': '210100',
#     'CENSUS_BLOCKGROUP': '1',
#     'FIRM_PANEL': '29189C0089K',
#     'ZONING': 'M1',
#     'MUNI_ZONING': None,
#     'TRASH_DISTRICT': 2,
#     'TRASH_OPTOUT': None,
#     'COGIS': None,
#     'CODE_ENFORCEMENT_DISTRICT': 4,
#     'PMZ_NEIGHBORHOOD': 1010}},
#     ...
# ```

# In[ ]:





# In[ ]:




