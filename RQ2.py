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

from DataLoaderSaver import DataLoaderSaver
from DataAnalyzer import DataAnalyzer
from URREFHelper import URREFHelper

""" Load datasets """
ncsc_data = DataLoaderSaver().load_dataset("NCSC", "engineered")
apt_data = DataLoaderSaver().load_dataset("APT", "processed")
# ncsc_classification_data = DataLoaderSaver().load_dataset("NCSC", "classification")

""" Explode NCSC datasets so each CVE-ID is its own instance """
ncsc_data = URREFHelper().explode_columns(ncsc_data, ['CVE-ID'])
# ncsc_classification_data = URREFHelper().explode_columns(ncsc_classification_data, ['CVE-ID'])

""" Explode NCSC dataset so each product, os and version is its own instance """
# ncsc_data = URREFHelper().explode_columns(ncsc_data, ['Platformen', 'Toepassingen', 'Versies'])

""" Select only necessary columns and merge NCSC and APT datasets"""
# ncsc = ncsc_data[["CVE-ID", "Toepassingen", "Versies", "Platformen"]]
# apt = apt_data[["CVE-ID", "product", "version", "os"]]
ncsc = ncsc_data[["CVE-ID", "Toepassingen", "Platformen"]]
apt = apt_data[["CVE-ID", "product", "os"]]
merged = pd.merge(ncsc, apt, on='CVE-ID')

# merged = merged.head(10000)

# print(len(merged))
# merged.dropna(subset=["Toepassingen", "Versies", "Platformen"], how="all", inplace=True)
merged.dropna(subset=["Toepassingen", "Platformen"], how="all", inplace=True)
# print(len(merged))

total_common_instances = len(merged)
unique_common_cve_ids = merged["CVE-ID"].nunique()

print(f"Total common instances: {total_common_instances}")
print(f"Unique common CVE-IDs: {unique_common_cve_ids}")

""" check for normalization versions ??? """
# version_ncsc = merged['Versies'].dropna().unique()
# version_apt = merged['version'].dropna().unique()
# # print(version_ncsc)
# # print(version_apt)
# unique_versions = np.unique(np.concatenate((version_ncsc, version_apt)))

""" Check for common values """
# print((merged['Versies'] == merged['version']).sum())
# print((merged['Toepassingen'] == merged['product']).sum())
# print((merged['os'] == merged['Platformen']).sum())
    

# print(hello)

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
TI = Namespace("http://example.org/urref/")
# URREF= Namespace("http://eturwg.c4i.gmu.edu/files/ontologies/URREF.owl#")
g.bind("ti", TI)
g.bind("rdfs", RDFS)
g.bind("owl", OWL)

""" Create new threat intelligence classes, including hierarchy, and add them to the graph """
URREFHelper().create_classes(g, ["ThreatIntelligence", "Vulnerability", "Product", "Version", "OS"])
URREFHelper().assign_labels(g,["ThreatIntelligence"], ["Threat Intelligence"])
URREFHelper().add_subclasses_to_thing(g, [TI.ThreatIntelligence])
URREFHelper().add_subclasses_to_ti(g, [TI.Vulnerability])
URREFHelper().add_subclasses_to_vulnerability(g, [TI.Product, TI.Version, TI.OS])

# merged = merged.head(1000) # for testing

""" Populate ontology with all instances of the merged dataset in batches """
batch_size = 1000
num_batches = (len(merged) + batch_size - 1) // batch_size
start_batch = max_batch

# merged = merged.head(1000) # for testing

for i in range(start_batch, num_batches + 1):
    start = (i - 1) * batch_size
    end = i * batch_size
    batch = merged.iloc[start:end]

    for index, row in batch.iterrows():
        CVE_ID = row['CVE-ID']
        TOEPASSING = row['Toepassingen']
        PRODUCT = row["product"]
        # VERSIE = row["Versies"]
        # VERSION = row["version"]
        PLATFORM = row["Platformen"]
        OS = row["os"]

        vulnerability_uri = URIRef(f"http://example.org/urref/vulnerability/{CVE_ID}")
        g.add((vulnerability_uri, RDF.type, TI.Vulnerability))
        g.add((vulnerability_uri, TI.hasCVEID, Literal(row['CVE-ID'], datatype=XSD.string)))

        """ Product """
        toepassing_uri = URIRef(f"http://example.org/urref/product/{uuid.uuid4()}")
        g.add((toepassing_uri, RDF.type, TI.Product))
        g.add((toepassing_uri, TI.hasProductName, Literal(TOEPASSING, datatype=XSD.string)))
        g.add((toepassing_uri, TI.fromDataset, Literal("NCSC", datatype=XSD.string)))
        g.add((vulnerability_uri, URIRef("http://example.org/urref/affectsProduct"), toepassing_uri))

        product_uri = URIRef(f"http://example.org/urref/product/{uuid.uuid4()}")
        g.add((product_uri, RDF.type, TI.Product))
        g.add((product_uri, TI.hasProductName, Literal(PRODUCT, datatype=XSD.string)))
        g.add((product_uri, TI.fromDataset, Literal("APT", datatype=XSD.string)))
        g.add((vulnerability_uri, URIRef("http://example.org/urref/affectsProduct"), product_uri))

        """ Version """
        # versie_uri = URIRef(f"http://example.org/urref/version/{uuid.uuid4()}")
        # g.add((versie_uri, RDF.type, TI.Version))
        # g.add((versie_uri, TI.hasVersionName, Literal(VERSIE, datatype=XSD.string)))
        # g.add((versie_uri, TI.fromDataset, Literal("NCSC", datatype=XSD.string)))
        # g.add((product_uri, URIRef("http://example.org/urref/affectsVersion"), versie_uri))

        # version_uri = URIRef(f"http://example.org/urref/version/{uuid.uuid4()}")
        # g.add((version_uri, RDF.type, TI.Version))
        # g.add((version_uri, TI.hasVersionName, Literal(VERSION, datatype=XSD.string)))
        # g.add((version_uri, TI.fromDataset, Literal("APT", datatype=XSD.string)))
        # g.add((product_uri, URIRef("http://example.org/urref/affectsVersion"), version_uri))

        """ OS """
        os_uri = URIRef(f"http://example.org/urref/os/{uuid.uuid4()}")
        g.add((os_uri, RDF.type, TI.OS))
        g.add((os_uri, TI.hasOSlabel, Literal(PLATFORM, datatype=XSD.string)))
        g.add((os_uri, TI.fromDataset, Literal("NCSC", datatype=XSD.string)))
        # g.add((version_uri, URIRef("http://example.org/urref/runsOn"), os_uri))

        os_uri = URIRef(f"http://example.org/urref/os/{uuid.uuid4()}")
        g.add((os_uri, RDF.type, TI.OS))
        g.add((os_uri, TI.hasOSlabel, Literal(OS, datatype=XSD.string)))
        g.add((os_uri, TI.fromDataset, Literal("APT", datatype=XSD.string)))
        # g.add((version_uri, URIRef("http://example.org/urref/runsOn"), os_uri)) 

        # print(row, "added from total rows:", len(merged))

    # Commit the batch to the graph
    g.commit()

    # Serialize and save the graph after each batch
    batch_file = f"batches/output_urref_batch_{i+1}.owl"
    g.serialize(destination=batch_file, format="xml")
    print(f"Batch {i+1} of {num_batches} committed and serialized.")

# Rename the final file
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
final_file = f'output_urref_{timestamp}.owl'
os.rename(batch_file, final_file)
print(f"Final file saved as {final_file}")