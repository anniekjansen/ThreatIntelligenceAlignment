from rdflib import Graph, URIRef, Literal, Namespace, BNode
from rdflib.namespace import RDF, XSD, RDFS, OWL
import pandas as pd
import string
import uuid


from DataLoaderSaver import DataLoaderSaver
from DataAnalyzer import DataAnalyzer
from URREFHelper import URREFHelper

""" Load datasets """
ncsc_data = DataLoaderSaver().load_dataset("NCSC", "engineered")
apt_data = DataLoaderSaver().load_dataset("APT", "processed")
ncsc_classification_data = DataLoaderSaver().load_dataset("NCSC", "classification")

""" Explode NCSC datasets so each CVE-ID is its own instance """
ncsc_data = URREFHelper().explode_columns(ncsc_data, ['CVE-ID'])
ncsc_classification_data = URREFHelper().explode_columns(ncsc_classification_data, ['CVE-ID'])

""" Explode NCSC dataset so each product, os and version is its own instance """
ncsc_data = URREFHelper().explode_columns(ncsc_data, ['Platformen', 'Toepassingen', 'Versies'])

# ncsc_data = ncsc_data.head(100)
# apt_data = apt_data.head(100)

# print(ncsc_data.head())
# print(apt_data.head())

""" Select only necessary columns and merge NCSC and APT datasets"""
ncsc = ncsc_data[["CVE-ID", "Toepassingen", "Versies", "Platformen"]]
apt = apt_data[["CVE-ID", "product", "version", "os"]]
merged = pd.merge(ncsc, apt, on='CVE-ID')

# print(len(merged))
merged.dropna(subset=["Toepassingen", "Versies", "Platformen"], how="all", inplace=True)
# print(len(merged))

# print(merged['product'].unique())
merged['product'] = merged['product'].str.replace('_', ' ')
print(merged['product'].unique())


# print(merged.head(10))

# unique_toepassingen = merged['Toepassingen'].unique()
# print(unique_toepassingen)

# common_values = [value for value in unique_toepassingen if value in merged['product'].values]

# if common_values:
#     print("Common values between Toepassingen and product columns:")
#     print(common_values)
# else:
#     print("No common values found between Toepassingen and product columns.")


keywords = ['Apple', 'Excel', "Powerpoint", "Visio", "Word", "Commence", "Visual", "SharePoint"'Adobe Acrobat', 'Office', "Excel", "Flash", "Google", "JDK", "JRE", "Biztalk", "Oracle", "Firefox", "Adobe Reader", "Blackberry", "IBM", "Adobe", "Windows", "Skype", "Explorer", "Linux", "WinRAR", "Confluence", "Open XML", "SQL"]  # add more keywords as needed
# transform to DICTIONAIRY?!


# for keyword in keywords:
#     merged['product'] = merged['product'].str.replace(r'.*' + keyword + '.*', keyword, regex=True, case=False)

for keyword in keywords:
    merged['product'] = merged['product'].str.replace(r'(?i).*' + keyword + '.*', keyword, regex=True)

print(merged['product'].unique())




# # One-hot encode the columns
# toepassingen_dummies = pd.get_dummies(merged['Toepassingen'].str.strip()).add_prefix('NCSC_Toepassingen_')
# versies_dummies = pd.get_dummies(merged['Versies'].str.strip()).add_prefix('NCSC_Versies_')
# platformen_dummies = pd.get_dummies(merged['Platformen'].str.strip()).add_prefix('NCSC_Platformen_')
# product_dummies = pd.get_dummies(merged['product']).add_prefix('APT_product_')
# version_dummies = pd.get_dummies(merged['version']).add_prefix('APT_version_')
# os_dummies = pd.get_dummies(merged['os']).add_prefix('APT_os_')

# # Concatenate the one-hot encoded columns with the original dataset
# merged_onehot = pd.concat([merged, toepassingen_dummies, versies_dummies, platformen_dummies, product_dummies, version_dummies, os_dummies], axis=1)

# # Drop the original columns
# merged_onehot.drop(['Toepassingen', 'Versies', 'Platformen', 'product', 'version', 'os'], axis=1, inplace=True)

# print(merged_onehot.head(10))


print(hello)

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
URREFHelper().create_classes(g, ["ThreatIntelligence", "Vulnerability", "Product", "Version", "OS"])
URREFHelper().assign_labels(g,["ThreatIntelligence"], ["Threat Intelligence"])
URREFHelper().add_subclasses_to_thing(g, [TI.ThreatIntelligence])
URREFHelper().add_subclasses_to_ti(g, [TI.Vulnerability])
URREFHelper().add_subclasses_to_vulnerability(g, [TI.Product, TI.Version, TI.OS])

# merged = merged.head(1000) # for testing

""" Populate ontology with all instances of the merged dataset in batches """
batch_size = 1000
num_batches = (len(merged) + batch_size - 1) // batch_size

for i in range(num_batches):
    start = i * batch_size
    end = (i + 1) * batch_size
    batch = merged.iloc[start:end]

    for index, row in batch.iterrows():
        CVE_ID = row['CVE-ID']
        TOEPASSING = row['Toepassingen']
        PRODUCT = row["product"]
        VERSIE = row["Versies"]
        VERSION = row["version"]
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
        versie_uri = URIRef(f"http://example.org/urref/version/{uuid.uuid4()}")
        g.add((versie_uri, RDF.type, TI.Version))
        g.add((versie_uri, TI.hasVersionName, Literal(VERSIE, datatype=XSD.string)))
        g.add((versie_uri, TI.fromDataset, Literal("NCSC", datatype=XSD.string)))
        g.add((product_uri, URIRef("http://example.org/urref/affectsVersion"), versie_uri))

        version_uri = URIRef(f"http://example.org/urref/version/{uuid.uuid4()}")
        g.add((version_uri, RDF.type, TI.Version))
        g.add((version_uri, TI.hasVersionName, Literal(VERSION, datatype=XSD.string)))
        g.add((version_uri, TI.fromDataset, Literal("APT", datatype=XSD.string)))
        g.add((product_uri, URIRef("http://example.org/urref/affectsVersion"), version_uri))

        """ OS """
        os_uri = URIRef(f"http://example.org/urref/os/{uuid.uuid4()}")
        g.add((os_uri, RDF.type, TI.OS))
        g.add((os_uri, TI.hasOSlabel, Literal(PLATFORM, datatype=XSD.string)))
        g.add((os_uri, TI.fromDataset, Literal("NCSC", datatype=XSD.string)))
        g.add((version_uri, URIRef("http://example.org/urref/runsOn"), os_uri))

        os_uri = URIRef(f"http://example.org/urref/os/{uuid.uuid4()}")
        g.add((os_uri, RDF.type, TI.OS))
        g.add((os_uri, TI.hasOSlabel, Literal(OS, datatype=XSD.string)))
        g.add((os_uri, TI.fromDataset, Literal("APT", datatype=XSD.string)))
        g.add((version_uri, URIRef("http://example.org/urref/runsOn"), os_uri)) 

        # print(row, "added from total rows:", len(merged))

    # Commit the batch to the graph
    g.commit()

    print(f"Batch {i+1} of {num_batches} committed.")

# Serialize and save the graph
g.serialize(destination="output_urref.owl", format="xml")
print("Graph serialized and saved successfully!")
