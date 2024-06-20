from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, XSD, RDFS, OWL
import pandas as pd

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
URREF = Namespace("http://example.org/urref#")
g.bind("urref", URREF)
g.bind("rdfs", RDFS)
g.bind("owl", OWL)

""" Create new threat intelligence classes, including hierarcy, and add them to the graph """
URREFHelper().create_classes(g, ["ThreatIntelligence", "Threat", "Vulnerability", "VulnerableProduct", "Time", "Product", "Platform", "Version"])
URREFHelper().assign_labels(g,["ThreatIntelligence", "VulnerableProduct"], ["Threat Intelligence", "Vulnerable Product"])
URREFHelper().add_subclasses_to_thing(g, [URREF.ThreatIntelligence])
URREFHelper().add_subclasses_to_ti(g, [URREF.Threat, URREF.Vulnerability, URREF.VulnerableProduct, URREF.Time])
URREFHelper().add_subclasses_to_vp(g, [URREF.Product, URREF.Platform, URREF.Version])

""" Explode the common identifier (CVE-ID) for the NCSC data """
ncsc_data = ncsc_data.assign(CVE_ID=ncsc_data['CVE-ID']).explode('CVE_ID')
ncsc_data = ncsc_data.drop(columns=['CVE-ID'])
ncsc_data.rename(columns = {'CVE_ID':'CVE-ID'}, inplace = True)
ncsc_data = ncsc_data.reset_index(drop=True)

""" Explode the Platformen attribute for the NCSC data """
ncsc_data = ncsc_data.assign(platformen=ncsc_data['Platformen']).explode('platformen')
ncsc_data = ncsc_data.drop(columns=['Platformen'])
ncsc_data.rename(columns = {'platformen':'Platformen'}, inplace = True)
ncsc_data = ncsc_data.reset_index(drop=True)

ncsc_data = ncsc_data.assign(toepassingen=ncsc_data['Toepassingen']).explode('toepassingen')
ncsc_data = ncsc_data.drop(columns=['Toepassingen'])
ncsc_data.rename(columns = {'toepassingen':'Toepassingen'}, inplace = True)
ncsc_data = ncsc_data.reset_index(drop=True)

ncsc_data = ncsc_data.assign(versies=ncsc_data['Versies']).explode('versies')
ncsc_data = ncsc_data.drop(columns=['Versies'])
ncsc_data.rename(columns = {'versies':'Versies'}, inplace = True)
ncsc_data = ncsc_data.reset_index(drop=True)

apt_data.rename(columns = {'vulnerability':'CVE-ID'}, inplace = True)

ncsc_data = ncsc_data.head(100)
apt_data = apt_data.head(100)

""" Add instances of the NCSC and APT datasets to the graph """
for idx, row in ncsc_data.iterrows():
    URREFHelper().create_instance(g, row, 'NCSC')
for idx, row in apt_data.iterrows():
    URREFHelper().create_instance(g, row, 'APT')

""" Serialize and save the graph """
g.serialize(destination="output_urref.owl", format="xml")
print("Graph serliazed and saved successfully!")
