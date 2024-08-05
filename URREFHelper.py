from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, XSD, RDFS, OWL
import pandas as pd

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
