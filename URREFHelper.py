from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, XSD, RDFS, OWL
import pandas as pd

class URREFHelper:

    URREF = Namespace("http://example.org/urref#")

    def create_classes(self, g, class_names):
        for name in class_names:
            g.add((self.URREF[name], RDF.type, OWL.Class))
    
    def assign_labels(self, g, class_names, labels):
        for name, label in zip(class_names, labels):
            g.add((self.URREF[name], RDFS.label, Literal(label)))
    
    def add_subclasses_to_thing(self, g, class_names):
        for name in class_names:
            g.add((name, RDFS.subClassOf, OWL.Thing))

    def add_subclasses_to_ti(self, g, class_names):
        for name in class_names:
            g.add((name, RDFS.subClassOf, self.URREF.ThreatIntelligence))
    
    def add_subclasses_to_vp(self, g, class_names):
        for name in class_names:
            g.add((name, RDFS.subClassOf, self.URREF.VulnerableProduct))

    def create_instance(self, g, row, security_dataset):
        CVE_ID = row['CVE-ID']
        
        # Add threat 
        threat_uri = URIRef(f"http://example.org/urref/threat/{CVE_ID}")
        g.add((threat_uri, RDF.type, self.URREF.Threat))
        if security_dataset == 'NCSC':
            columns = ['NCSC ID', 'Update', 'Beschrijving', 'Kans']
            predicates = [self.URREF.hasNCSCID, self.URREF.hasUpdateNumber, self.URREF.hasDescription, self.URREF.hasChanceClassification]
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
            if pd.notna(row['campaign']):
                g.add((threat_uri, self.URREF.hasCampaignID, Literal(row['campaign'], datatype=XSD.integer)))
            else:
                g.add((threat_uri, self.URREF.hasCampaignID, Literal(None, datatype=XSD.integer)))
        
        # Add vulnerability
        vulnerability_uri = URIRef(f"http://example.org/urref/vulnerability/{CVE_ID}")
        g.add((vulnerability_uri, RDF.type, self.URREF.Vulnerability))
        if security_dataset == 'NCSC':
            if pd.notna(row['CVE-ID']):
                g.add((vulnerability_uri, self.URREF.hasCVEID, Literal(row['CVE-ID'], datatype=XSD.string)))
            else:
                g.add((vulnerability_uri, self.URREF.hasCVEID, Literal(None, datatype=XSD.string)))
        elif security_dataset == 'APT':
            columns = ['CVE-ID', 'attack_vector']
            predicates = [self.URREF.hasCVEID, self.URREF.hasAttackVector]
            datatypes = [XSD.string, XSD.string]
            for column, predicate, datatype in zip(columns, predicates, datatypes):
                if pd.notna(row[column]):
                    g.add((vulnerability_uri, predicate, Literal(row[column], datatype=datatype)))
                else:
                    g.add((vulnerability_uri, predicate, Literal(None, datatype=datatype)))

        g.add((threat_uri, self.URREF.hasVulnerability, vulnerability_uri))
        
        # Add vulnerable products
        product_uri = URIRef(f"http://example.org/urref/vulnerableproduct/{CVE_ID}")
        g.add((product_uri, RDF.type, self.URREF.VulnerableProduct))
        if security_dataset == 'NCSC':
            columns = ['Toepassingen', 'Platformen', 'Versies']
            predicates = [self.URREF.hasProduct, self.URREF.hasPlatform, self.URREF.hasVersion]
            datatypes = [XSD.string, XSD.string, XSD.string]
            for column, predicate, datatype in zip(columns, predicates, datatypes):
                if pd.notna(row[column]):
                    g.add((product_uri, predicate, Literal(row[column], datatype=datatype)))
                else:
                    g.add((product_uri, predicate, Literal(None, datatype=datatype)))
        elif security_dataset == 'APT':
            columns = ['product', 'os', 'version']
            predicates = [self.URREF.hasProduct, self.URREF.hasPlatform, self.URREF.hasVersion]
            datatypes = [XSD.string, XSD.string, XSD.string]
            for column, predicate, datatype in zip(columns, predicates, datatypes):
                if pd.notna(row[column]):
                    g.add((product_uri, predicate, Literal(row[column], datatype=datatype)))
                else:
                    g.add((product_uri, predicate, Literal(None, datatype=datatype)))

        g.add((threat_uri, self.URREF.hasVulnerableProduct, product_uri))
        
        # Add time
        time_uri = URIRef(f"http://example.org/urref/time/{CVE_ID}")
        g.add((time_uri, RDF.type, self.URREF.Time))
        if security_dataset == 'NCSC':
            if pd.notna(row['Uitgiftedatum']):
                g.add((time_uri, self.URREF.hasTime, Literal(row['Uitgiftedatum'], datatype=XSD.dateTime)))
            else: 
                g.add((time_uri, self.URREF.hasTime, Literal(None, datatype=XSD.dateTime)))
        elif security_dataset == 'APT':
            columns = ['exploited_time', 'published_time', 'reserved_time']
            predicates = [self.URREF.hasExploitedTime, self.URREF.hasPublishedTime, self.URREF.hasReservedTime]
            datatypes = [XSD.dateTime, XSD.dateTime, XSD.dateTime]
            if pd.notna(row[column]):
                g.add((time_uri, predicate, Literal(row[column], datatype=datatype)))
            else:
                g.add((time_uri, predicate, Literal(None, datatype=datatype)))

        g.add((threat_uri, self.URREF.hasTime, time_uri))