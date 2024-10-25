from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, XSD, RDFS, OWL
import pandas as pd
import os
import datetime
from urllib.parse import quote

from DataLoaderSaver import DataLoaderSaver
from DataAnalyzer import DataAnalyzer
from DataProcessor import DataProcessor
from URREFHelper import URREFHelper

""" Load datasets """
ncsc_data = DataLoaderSaver().load_dataset("NCSC", "processed")
apt_data = DataLoaderSaver().load_dataset("APT", "processed")
ncsc_justification_data = DataLoaderSaver().load_dataset("NCSC", "classification")

""" Explode NCSC datasets so each CVE-ID is its own instance """
ncsc_data = URREFHelper().explode_columns(ncsc_data, ['CVE-ID'])
ncsc_justification_data = URREFHelper().explode_columns(ncsc_justification_data, ['CVE-ID'])

""" Explode NCSC dataset so each product, os and version is its own instance """
ncsc_data = URREFHelper().explode_columns(ncsc_data, ['Platformen', 'Toepassingen', 'Versies'])

""" Select only necessary columns and merge NCSC and APT datasets"""
ncsc = ncsc_data[["CVE-ID", "Toepassingen", "Versies", "Platformen", "Kans"]]
apt = apt_data[["CVE-ID", "product", "version", "os"]]
merged = pd.merge(ncsc, apt, on='CVE-ID')

ncsc_justification_data.rename(columns={
    'Kans justified+important change': 'Justified',       
    'Kans no change': 'No_change', 
    'Kans unjustified change': 'Unjustified',
    'Kans unimportant change': 'Unimportant'
}, inplace=True)

ncsc_justification_data = ncsc_justification_data[['CVE-ID', 'Justified', 'No_change', 'Unjustified', 'Unimportant']] 

justified_dict = ncsc_justification_data.set_index('CVE-ID')['Justified'].to_dict()
no_change_dict = ncsc_justification_data.set_index('CVE-ID')['No_change'].to_dict()
unjustified_dict = ncsc_justification_data.set_index('CVE-ID')['Unjustified'].to_dict()
unimportant_dict = ncsc_justification_data.set_index('CVE-ID')['Unimportant'].to_dict()

merged['Justified'] = merged['CVE-ID'].map(justified_dict)
merged['No_change'] = merged['CVE-ID'].map(no_change_dict)
merged['Unjustified'] = merged['CVE-ID'].map(unjustified_dict)
merged['Unimportant'] = merged['CVE-ID'].map(unimportant_dict)

total_common_instances = len(merged)
unique_common_cve_ids = merged["CVE-ID"].nunique()

print(f"Total common instances: {total_common_instances}")
print(f"Unique common CVE-IDs: {unique_common_cve_ids}")

# merged = merged.head(1000) # for testing

g = Graph()
g.parse("URREF.owl", format="xml")
print("URREF graph loaded successfully!")

""" Create URREF Namespace and bind this + other namespaces to the graph """
TI = Namespace("http://example.org/threatintelligence/")

g.bind("ti", TI)
g.bind("rdfs", RDFS)

""" Create new threat intelligence classes, including hierarchy, and add them to the graph """
URREFHelper().create_classes(g, ["ThreatIntelligence", "Vulnerability", "Product", "Version", "OS", "Dataset", "Likelihood", "Justification"])
URREFHelper().assign_labels(g,["ThreatIntelligence"], ["Threat Intelligence"])
URREFHelper().add_subclasses_to_thing(g, [TI.ThreatIntelligence])
URREFHelper().add_subclasses_to_ti(g, [TI.Vulnerability, TI.Dataset, TI.Likelihood, TI.Justification])
URREFHelper().add_subclasses_to_vulnerability(g, [TI.Product, TI.Version, TI.OS])
URREFHelper().add_predicates(g, ["fromDataset", "hasProductName", "affectsProduct", "affectsVersion", "runsOn", "hasLikelihood", "hasDescriptionChange", "hasOSlabel", "hasVersionName"])

g.add((TI.fromDataset, RDF.type, OWL.ObjectProperty))
g.add((TI.hasProductName, RDF.type, OWL.ObjectProperty))
g.add((TI.affectsProduct, RDF.type, OWL.ObjectProperty))
g.add((TI.affectsVersion, RDF.type, OWL.ObjectProperty))
g.add((TI.runsOn, RDF.type, OWL.ObjectProperty))
g.add((TI.hasLikelihood, RDF.type, OWL.ObjectProperty))
g.add((TI.hasDescriptionChange, RDF.type, OWL.ObjectProperty))
g.add((TI.hasOSlabel, RDF.type, OWL.ObjectProperty))
g.add((TI.hasVersionName, RDF.type, OWL.ObjectProperty))

""" Populate ontology with all instances of the merged dataset in batches """
batch_size = 1000
num_batches = (len(merged) + batch_size - 1) // batch_size

for i in range(0, num_batches + 1):
    start = (i - 1) * batch_size
    end = i * batch_size
    batch = merged.iloc[start:end]

    for index, row in batch.iterrows():
        CVE_ID = row['CVE-ID']
        LIKELIHOOD = row['Kans']
        JUSTIFIED= row['Justified']
        NOCHANGE = row['No_change']
        UNJUSTIFIED = row['Unjustified']
        UNIMPORTANT = row['Unimportant']
        TOEPASSING = row['Toepassingen']
        PRODUCT = row["product"]
        VERSIE = row["Versies"]
        VERSION = row["version"]
        PLATFORM = row["Platformen"]
        OS = row["os"]

        """ Vulnerability """
        vulnerability_uri = URIRef(f"http://example.org/threatintelligence/vulnerability/{CVE_ID}")
        if (vulnerability_uri, RDF.type, TI.Vulnerability) not in g:
            g.add((vulnerability_uri, RDF.type, TI.Vulnerability))
        g.add((vulnerability_uri, TI.hasCVEID, Literal(row['CVE-ID'], datatype=XSD.string)))

        """ Dataset """
        NCSC_dataset_uri, APT_dataset_uri = URREFHelper().add_datasets_to_graph(g)

        """ Likelihood & Justification """
        likelihood_uri = URREFHelper().add_likelihood_to_graph(g, LIKELIHOOD, vulnerability_uri)        
        justifications = [JUSTIFIED, NOCHANGE, UNJUSTIFIED, UNIMPORTANT]
        justifications_label = ["Justified", "No_change", "Unjustified", "Unimportant"]
        for j in range(0,len(justifications)):
            if justifications[j] != 0:
                justification_uri = URREFHelper().add_justification_to_graph(g, justifications_label[j], vulnerability_uri)

        """ Product """
        if TOEPASSING == None:
            TOEPASSING = "Unknown"
        if PRODUCT == None:
            PRODUCT = "Unknown"

        product_uri_ncsc = URREFHelper().add_product_to_graph(g, TOEPASSING, NCSC_dataset_uri, vulnerability_uri)
        product_uri_apt = URREFHelper().add_product_to_graph(g, PRODUCT, APT_dataset_uri, vulnerability_uri)

        """ VERSION """
        if VERSIE == None:
            VERSIE = "Unknown"
        if VERSION == None:
            VERSION = "Unknown"

        version_uri_ncsc = URREFHelper().add_version_to_graph(g, VERSIE, NCSC_dataset_uri, product_uri_ncsc)
        version_uri_apt = URREFHelper().add_version_to_graph(g, VERSION, APT_dataset_uri, product_uri_apt)

        """ OS """
        if PLATFORM == None:
            PLATFORM = "Unknown"
        if OS == None:
            OS = "Unknown"

        os_uri_ncsc = URREFHelper().add_os_to_graph(g, PLATFORM, NCSC_dataset_uri, version_uri_ncsc)
        os_uri_apt = URREFHelper().add_os_to_graph(g, OS, APT_dataset_uri, version_uri_apt)

    g.commit()

    print(f"Batch {i+1} of {num_batches} committed.")

timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
final_file = f'output_urref_{timestamp}.owl'
g.serialize(destination=final_file, format="xml")
print(f"File saved as {final_file}")
