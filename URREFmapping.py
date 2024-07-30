from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, XSD, RDFS, OWL
import pandas as pd
import string

from DataLoaderSaver import DataLoaderSaver
from DataAnalyzer import DataAnalyzer
from URREFHelper import URREFHelper

""" Load datasets """
ncsc_data = DataLoaderSaver().load_dataset("NCSC", "engineered")
apt_data = DataLoaderSaver().load_dataset("APT", "processed")
ncsc_classification_data = DataLoaderSaver().load_dataset("NCSC", "classification")

""" Load the URREF ontology """
g = Graph()
g.parse("URREF.owl", format="xml")
print("Graph loaded successfully!")

""" Create URREF Namespace and bind this + other namespaces to the graph """
TI = Namespace("http://example.org/urref/")
# URREF= Namespace("http://eturwg.c4i.gmu.edu/files/ontologies/URREF.owl#")
g.bind("ti", TI)
g.bind("rdfs", RDFS)
g.bind("owl", OWL)

""" Create new threat intelligence classes, including hierarcy, and add them to the graph """
URREFHelper().create_classes(g, ["ThreatIntelligence", "Threat", "Vulnerability", "VulnerableProduct", "Time", "Product", "Platform", "Version"])
URREFHelper().assign_labels(g,["ThreatIntelligence", "VulnerableProduct"], ["Threat Intelligence", "Vulnerable Product"])
URREFHelper().add_subclasses_to_thing(g, [TI.ThreatIntelligence])
URREFHelper().add_subclasses_to_ti(g, [TI.Threat, TI.Vulnerability, TI.VulnerableProduct, TI.Time])
URREFHelper().add_subclasses_to_vp(g, [TI.Product, TI.Platform, TI.Version])

""" Explode the columns of the NCSC data that include lists """
ncsc_data = URREFHelper().explode_columns(ncsc_data, ['CVE-ID', 'Platformen', 'Toepassingen', 'Versies'])
ncsc_classification_data = URREFHelper().explode_columns(ncsc_classification_data, ['CVE-ID'])

# apt_data.rename(columns = {'vulnerability':'CVE-ID'}, inplace = True)

# ncsc_data = ncsc_data.head(100)
# apt_data = apt_data.head(100)

# print(ncsc_data.head())
# print(apt_data.head())

print(f"Number of unique CVE-IDs NCSC: {len(ncsc_data['CVE-ID'].unique())}")
print(f"Number of unique CVE-IDs APT: {len(apt_data['CVE-ID'].unique())}")

""" Check the common instances """
common_instances = pd.merge(ncsc_data, apt_data, on='CVE-ID')
print(f"Number of common instances: {len(common_instances)}")
print(f"Number of unique CVE-IDs: {len(common_instances['CVE-ID'].unique())}")
common_instances = common_instances["CVE-ID"].unique()

unique_to_apt_data = apt_data[~apt_data['CVE-ID'].isin(ncsc_data['CVE-ID'])]
print(f"Number of unique CVE-IDs in APT that are not in NCSC: {len(unique_to_apt_data['CVE-ID'].unique())}")

unique_to_ncsc_data = ncsc_data[~ncsc_data['CVE-ID'].isin(apt_data['CVE-ID'])]
print(f"Number of unique CVE-IDs in NCSC that are not in APT: {len(unique_to_ncsc_data['CVE-ID'].unique())}") #should be none because NCSC is subset of APT

# print(common_instances)

# common = pd.merge(common_instances, ncsc_classification_data, on='CVE-ID')
# print(f"Number of common instances: {len(common)}")
# print(f"Number of unique CVE-IDs: {len(common['CVE-ID'].unique())}")

print(hello)

""" Add instances of the NCSC and APT datasets to the graph """
for index, row in ncsc_data.iterrows():
    URREFHelper().create_instance(g, row, 'NCSC')
for index, row in apt_data.iterrows():
    URREFHelper().create_instance(g, row, 'APT')

""" Serialize and save the graph """
g.serialize(destination="output_urref.owl", format="xml")
print("Graph serliazed and saved successfully!")
