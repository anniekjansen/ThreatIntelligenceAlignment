from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, XSD, RDFS, OWL
from urllib.parse import quote
import pandas as pd
import uuid

class URREFHelper:

    TI = Namespace("http://example.org/urref/")
    #URREF= Namespace("http://eturwg.c4i.gmu.edu/files/ontologies/URREF.owl#")

    def create_classes(self, g, class_names):
        for name in class_names:
            g.add((self.TI[name], RDF.type, OWL.Class))
    
    def assign_labels(self, g, class_names, labels):
        for name, label in zip(class_names, labels):
            g.add((self.TI[name], RDFS.label, Literal(label)))
    
    def add_subclasses_to_thing(self, g, class_names):
        for name in class_names:
            g.add((name, RDFS.subClassOf, OWL.Thing))

    def add_subclasses_to_ti(self, g, class_names):
        for name in class_names:
            g.add((name, RDFS.subClassOf, self.TI.ThreatIntelligence))
    
    def add_subclasses_to_vulnerability(self, g, class_names):
        for name in class_names:
            g.add((name, RDFS.subClassOf, self.TI.Vulnerability))

    def explode_columns(self, data, column_names):
        for col in column_names:
            new_col_name = col + "_exploded"
            data = data.assign(**{new_col_name: data[col]}).explode(new_col_name)
            data = data.drop(columns=[col])
            data.rename(columns = {new_col_name: col}, inplace=True)
        data = data.reset_index(drop=True)
        return data
    
        # Function to get or create a product class
    def add_product_to_graph(self, g, product_name, dataset, vulnerability_uri):
        product_uri = URIRef(f"http://example.org/urref/product/{quote(product_name.replace(' ', '_'))}")
        if (product_uri, RDF.type, self.TI.Product) not in g:
            g.add((product_uri, RDF.type, self.TI.Product))
            g.add((product_uri, self.TI.hasProductName, Literal(product_name, datatype=XSD.string)))
        g.add((product_uri, self.TI.fromDataset, Literal(dataset, datatype=XSD.string)))
        g.add((vulnerability_uri, URIRef("http://example.org/urref/affectsProduct"), product_uri))
        return product_uri
    
    def add_version_to_graph(self, g, version_name, dataset, product_uri):
        version_uri = URIRef(f"http://example.org/urref/version/{quote(version_name.replace(' ', '_'))}")
        if (version_uri, RDF.type, self.TI.Version) not in g:
            g.add((version_uri, RDF.type, self.TI.Version))
            g.add((version_uri, self.TI.hasVersionName, Literal(version_name, datatype=XSD.string)))
        g.add((version_uri, self.TI.fromDataset, Literal(dataset, datatype=XSD.string)))
        g.add((product_uri, URIRef("http://example.org/urref/affectsVersion"), version_uri))
        return version_uri

    def add_os_to_graph(self, g, os_label, dataset, version_uri):
        os_uri = URIRef(f"http://example.org/urref/os/{quote(os_label.replace(' ', '_'))}")
        if (os_uri, RDF.type, self.TI.OS) not in g:
            g.add((os_uri, RDF.type, self.TI.OS))
            g.add((os_uri, self.TI.hasOSlabel, Literal(os_label, datatype=XSD.string)))
        g.add((os_uri, self.TI.fromDataset, Literal(dataset, datatype=XSD.string)))
        g.add((version_uri, URIRef("http://example.org/urref/runsOn"), os_uri))
        return os_uri
    
    def add_total_application_affected_ncsc_to_graph(self, g, total_application_affected, vulnerability_uri):
        total_application_affected_uri = URIRef(f"http://example.org/urref/totalApplicationAffected/{quote(total_application_affected.replace(' ', '_'))}")
        if (total_application_affected_uri, RDF.type, self.TI.TotalApplicationAffected) not in g:
            g.add((total_application_affected_uri, RDF.type, self.TI.TotalApplicationAffected))
            g.add((total_application_affected_uri, self.TI.hasTotalApplicationAffected, Literal(total_application_affected, datatype=XSD.string)))
        g.add((vulnerability_uri, URIRef("http://example.org/urref/hasTotalApplicationAffected"), total_application_affected_uri))
        return total_application_affected_uri
    
    def add_total_application_affected_apt_to_graph(self, g, total_application_affected, vulnerability_uri):
        total_application_affected_uri = URIRef(f"http://example.org/urref/totalApplicationAffected/{quote(total_application_affected.replace(' ', '_'))}")
        if (total_application_affected_uri, RDF.type, self.TI.TotalApplicationAffected) not in g:
            g.add((total_application_affected_uri, RDF.type, self.TI.TotalApplicationAffected))
            g.add((total_application_affected_uri, self.TI.hasTotalApplicationAffected, Literal(total_application_affected, datatype=XSD.string)))
        g.add((vulnerability_uri, URIRef("http://example.org/urref/hasTotalApplicationAffected"), total_application_affected_uri))
        return total_application_affected_uri
    