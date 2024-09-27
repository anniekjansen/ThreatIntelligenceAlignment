from rdflib import Graph, URIRef, Literal, Namespace, BNode
from rdflib.namespace import RDF, XSD, RDFS, OWL
import pandas as pd
import string
import uuid
import numpy as np
import os
import glob
import datetime
import urllib.parse
import psutil
from urllib.parse import quote
import dask.dataframe as dd

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

# Find the maximum batch number
max_batch = 0
if not os.path.exists('batches'):
    os.makedirs('batches')

for file in os.listdir("batches"):
    if file.startswith("output_urref_batch_") and file.endswith(".owl"):
        batch_num = int(file.split("_")[-1].split(".")[0])
        if batch_num > max_batch:
            max_batch = batch_num

# Load and parse the maximum batch
batch_file = f"batches/output_urref_batch_{max_batch}.owl"
g = Graph()
if os.path.exists(batch_file):
    g.parse(batch_file, format="xml")
    print(f"Graph loaded from latest batch: {batch_file}")
else:
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

""" Populate ontology with all instances of the merged dataset in batches """
batch_size = 1000
num_batches = (len(merged) + batch_size - 1) // batch_size
start_batch = max_batch

for i in range(start_batch, num_batches + 1):
    start = (i - 1) * batch_size
    end = i * batch_size
    batch = merged.iloc[start:end]

    for index, row in batch.iterrows():
        CVE_ID = row['CVE-ID']

        LIKELIHOOD = row['Kans']
        # IMPACT = row['Schade']

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

        """ Likelihood, Impact, Justification """
        likelihood_uri = URREFHelper().add_likelihood_to_graph(g, LIKELIHOOD, vulnerability_uri)
        # impact_uri = URREFHelper().add_impact_to_graph(g, IMPACT, vulnerability_uri)
        
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

    # Serialize and save the graph after each batch
    # batch_file = f"batches/output_urref_batch_{i+1}.owl"
    # g.serialize(destination=batch_file, format="xml")
    # print(f"Batch {i+1} of {num_batches} committed and serialized.")
    print(f"Batch {i+1} of {num_batches} committed.")

# Rename the final file
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
final_file = f'output_urref_{timestamp}.owl'
g.serialize(destination=final_file, format="xml")
# os.rename(batch_file, final_file)
print(f"Final file saved as {final_file}")
