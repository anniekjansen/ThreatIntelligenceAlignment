from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, XSD
import pandas as pd

from DataLoaderSaver import DataLoaderSaver

""" Load datasets """
ncsc_data = DataLoaderSaver().load_dataset("NCSC", "engineered", "$")
apt_data = DataLoaderSaver().load_dataset("APT", "processed")
ncsc_classification_data = DataLoaderSaver().load_dataset("NCSC", "classification", "$")

""" Load the URREF ontology """
g = Graph()
g.parse("URREF.owl", format="xml")
print("Graph loaded successfully!")

URREF = Namespace("http://example.org/urref#")
g.bind("urref", URREF)

# Define a function to create URREF instances
def create_instance(row, dataset_type):

    # Add threat 
    threat_uri = URIRef(f"http://example.org/urref/threat/{row['Advisory ID']}")
    g.add((threat_uri, RDF.type, URREF.Threat))
    if dataset_type == 'NCSC':
        g.add((threat_uri, URREF.hasID, Literal(row['NCSC ID'], datatype=XSD.string)))
        g.add((threat_uri, URREF.hasUpdateNumber, Literal(int(row['Update']), datatype=XSD.integer)))
        g.add((threat_uri, URREF.hasDescription, Literal(row['Beschrijving'], datatype=XSD.string)))
        g.add((threat_uri, URREF.hasChanceClassification, Literal(row['Kans'], datatype=XSD.string)))
    else:
        g.add((threat_uri, URREF.hasID, Literal(row['campaign'], datatype=XSD.integer)))
    
    # Add vulnerability
    vulnerability_uri = URIRef(f"http://example.org/urref/vulnerability/{row['Advisory ID']}")
    g.add((vulnerability_uri, RDF.type, URREF.Vulnerability))
    if dataset_type == 'NCSC':
        g.add((vulnerability_uri, URREF.hasCVEID, Literal(row['CVE-ID'], datatype=XSD.string)))
    elif dataset_type == 'APT':
        g.add((vulnerability_uri, URREF.hasCVEID, Literal(int(row['vulnerability']), datatype=XSD.integer)))
        g.add((vulnerability_uri, URREF.hasAttackVector, Literal(row['attack_vector'], datatype=XSD.string)))
    g.add((threat_uri, URREF.hasVulnerability, vulnerability_uri))
    
    # Add vulnerable products
    product_uri = URIRef(f"http://example.org/urref/vulnerableproduct/{row['Advisory ID']}")
    g.add((product_uri, RDF.type, URIRef("http://example.org/urref#VulnerableProduct")))
    if dataset_type == 'NCSC':
        g.add((product_uri, URREF.hasProduct, Literal(row['Toepassingen'], datatype=XSD.string)))
        g.add((product_uri, URREF.hasPlatform, Literal(row['Platformen'], datatype=XSD.string)))
        g.add((product_uri, URREF.hasVersion, Literal(row['Versies'], datatype=XSD.string)))
    elif dataset_type == 'APT':
        g.add((product_uri, URREF.hasProduct, Literal(row['product'], datatype=XSD.string)))
        g.add((product_uri, URREF.hasPlatform, Literal(row['os'], datatype=XSD.string)))
        g.add((product_uri, URREF.hasVersion, Literal(row['version'], datatype=XSD.string)))
    g.add((threat_uri, URREF.hasVulnerableProduct, product_uri))
    
    # Add time
    time_uri = URIRef(f"http://example.org/urref/time/{row['Advisory ID']}")
    g.add((time_uri, RDF.type, URIRef("http://example.org/urref#Time")))
    if dataset_type == 'NCSC':
        g.add((time_uri, URREF.hasTime, Literal(row['Uitgiftedatum'], datatype=XSD.dateTime)))
    elif dataset_type == 'APT':
        g.add((time_uri, URREF.hasExploitedTime, Literal(row['exploited_time'], datatype=XSD.dateTime)))
        g.add((time_uri, URREF.hasPublishedTime, Literal(row['published_time'], datatype=XSD.dateTime)))
        g.add((time_uri, URREF.hasReservedTime, Literal(row['reserved_time'], datatype=XSD.dateTime)))
    g.add((threat_uri, URREF.hasTime, time_uri))


""" Explode the common identifier (CVE-ID) for the NCSC data """
ncsc_data = ncsc_data.assign(CVE_ID=ncsc_data['CVE-ID']).explode('CVE_ID')
ncsc_data.rename(columns = {'CVE_ID':'CVE-ID'}, inplace = True)
print(ncsc_data.head())

# Process NCSC dataset
for idx, row in ncsc_data.iterrows():
    create_instance(row, 'NCSC')

# Process APT dataset
for idx, row in apt_data.iterrows():
    create_instance(row, 'APT')

# Save the graph
g.serialize(destination="output_urref.owl", format="xml")
