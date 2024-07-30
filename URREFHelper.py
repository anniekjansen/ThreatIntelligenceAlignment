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
    
    def add_subclasses_to_vp(self, g, class_names):
        for name in class_names:
            g.add((name, RDFS.subClassOf, self.TI.VulnerableProduct))

    def explode_columns(self, data, column_names):
        for col in column_names:
            new_col_name = col + "_exploded"
            data = data.assign(**{new_col_name: data[col]}).explode(new_col_name)
            data = data.drop(columns=[col])
            data.rename(columns = {new_col_name: col}, inplace=True)
        data = data.reset_index(drop=True)
        return data

    def create_instance(self, g, row, security_dataset):
        CVE_ID = row['CVE-ID']
        
        # Add threat 
        threat_uri = URIRef(f"http://example.org/urref/Threat/{CVE_ID}")
        g.add((threat_uri, RDF.type, self.TI.Threat))
        if security_dataset == 'NCSC':
            g.add((threat_uri, self.TI.fromNCSC, Literal(True, datatype=XSD.boolean)))
            columns = ['NCSC ID', 'Update', 'Beschrijving', 'Kans']
            predicates = [self.TI.hasNCSCID, self.TI.hasUpdateNumber, self.TI.hasDescription, self.TI.hasChanceClassification]
            datatypes = [XSD.string, XSD.integer, XSD.string, XSD.string]
            for column, predicate, datatype in zip(columns, predicates, datatypes):
                if pd.notna(row[column]):
                    if datatype == XSD.integer:
                        g.add((threat_uri, predicate, Literal(int(row[column]), datatype=datatype)))
                    else:
                        g.add((threat_uri, predicate, Literal(row[column], datatype=datatype)))
                else:
                    g.add((threat_uri, predicate, Literal(None, datatype=datatype)))
        else:
            g.add((threat_uri, self.TI.fromAPT, Literal(True, datatype=XSD.boolean)))
            if pd.notna(row['campaign']):
                g.add((threat_uri, self.TI.hasCampaignID, Literal(row['campaign'], datatype=XSD.integer)))
            else:
                g.add((threat_uri, self.TI.hasCampaignID, Literal(None, datatype=XSD.integer)))
        
        # Add vulnerability
        vulnerability_uri = URIRef(f"http://example.org/urref/vulnerability/{CVE_ID}")
        g.add((vulnerability_uri, RDF.type, self.TI.Vulnerability))
        if security_dataset == 'NCSC':
            if pd.notna(row['CVE-ID']):
                g.add((vulnerability_uri, self.TI.hasCVEID, Literal(row['CVE-ID'], datatype=XSD.string)))
            else:
                g.add((vulnerability_uri, self.TI.hasCVEID, Literal(None, datatype=XSD.string)))
        elif security_dataset == 'APT':
            columns = ['CVE-ID', 'attack_vector']
            predicates = [self.TI.hasCVEID, self.TI.hasAttackVector]
            datatypes = [XSD.string, XSD.string]
            for column, predicate, datatype in zip(columns, predicates, datatypes):
                if pd.notna(row[column]):
                    g.add((vulnerability_uri, predicate, Literal(row[column], datatype=datatype)))
                else:
                    g.add((vulnerability_uri, predicate, Literal(None, datatype=datatype)))

        g.add((threat_uri, self.TI.hasVulnerability, vulnerability_uri))
        
        # Add vulnerable products
        product_uri = URIRef(f"http://example.org/urref/vulnerableproduct/{CVE_ID}")
        g.add((product_uri, RDF.type, self.TI.VulnerableProduct))
        if security_dataset == 'NCSC':
            columns = ['Toepassingen', 'Platformen', 'Versies']
            predicates = [self.TI.hasProduct, self.TI.hasPlatform, self.TI.hasVersion]
            datatypes = [XSD.string, XSD.string, XSD.string]
            for column, predicate, datatype in zip(columns, predicates, datatypes):
                if pd.notna(row[column]):
                    g.add((product_uri, predicate, Literal(row[column], datatype=datatype)))
                else:
                    g.add((product_uri, predicate, Literal(None, datatype=datatype)))
        elif security_dataset == 'APT':
            columns = ['product', 'os', 'version']
            predicates = [self.TI.hasProduct, self.TI.hasPlatform, self.TI.hasVersion]
            datatypes = [XSD.string, XSD.string, XSD.string]
            for column, predicate, datatype in zip(columns, predicates, datatypes):
                if pd.notna(row[column]):
                    g.add((product_uri, predicate, Literal(row[column], datatype=datatype)))
                else:
                    g.add((product_uri, predicate, Literal(None, datatype=datatype)))

        g.add((threat_uri, self.TI.hasVulnerableProduct, product_uri))
        
        # Add time
        time_uri = URIRef(f"http://example.org/urref/time/{CVE_ID}")
        g.add((time_uri, RDF.type, self.TI.Time))
        if security_dataset == 'NCSC':
            if pd.notna(row['Uitgiftedatum']):
                g.add((time_uri, self.TI.hasTime, Literal(row['Uitgiftedatum'], datatype=XSD.dateTime)))
            else: 
                g.add((time_uri, self.TI.hasTime, Literal(None, datatype=XSD.dateTime)))
        elif security_dataset == 'APT':
            columns = ['exploited_time', 'published_time', 'reserved_time']
            predicates = [self.TI.hasExploitedTime, self.TI.hasPublishedTime, self.TI.hasReservedTime]
            datatypes = [XSD.dateTime, XSD.dateTime, XSD.dateTime]
            if pd.notna(row[column]):
                g.add((time_uri, predicate, Literal(row[column], datatype=datatype)))
            else:
                g.add((time_uri, predicate, Literal(None, datatype=datatype)))

        g.add((threat_uri, self.TI.hasTime, time_uri))
