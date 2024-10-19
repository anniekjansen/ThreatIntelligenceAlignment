from rdflib import URIRef, Literal, Namespace
from rdflib.namespace import RDF, XSD, RDFS, OWL
from urllib.parse import quote

class URREFHelper:

    TI = Namespace("http://example.org/threatintelligence/")

    def create_classes(self, g, class_names):
        for name in class_names:
            g.add((self.TI[name], RDF.type, RDFS.Class))

    def assign_labels(self, g, class_names, labels):
        for name, label in zip(class_names, labels):
            g.add((self.TI[name], RDF.type, self.TI[name]))
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

    def add_subclasses_to_dataset(self, g, class_names):
        for name in class_names:
            g.add((name, RDFS.subClassOf, self.TI.Dataset))

    def add_predicates(self, g, predicate_names):
        for name in predicate_names:
            setattr(self.TI, name, self.TI[name])
            g.add((self.TI[name], RDF.type, OWL.ObjectProperty))

    def explode_columns(self, data, column_names):
        for col in column_names:
            new_col_name = col + "_exploded"
            data = data.assign(**{new_col_name: data[col]}).explode(new_col_name)
            data = data.drop(columns=[col])
            data.rename(columns = {new_col_name: col}, inplace=True)
        data = data.reset_index(drop=True)
        return data

    def add_datasets_to_graph(self, g):
        NCSC_dataset_uri = URIRef("http://example.org/threatintelligence/dataset/NCSC")
        APT_dataset_uri = URIRef("http://example.org/threatintelligence/dataset/APT")
        if (NCSC_dataset_uri, RDF.type, self.TI.Dataset) not in g:
            g.add((NCSC_dataset_uri, RDF.type, self.TI.Dataset))
            g.add((NCSC_dataset_uri, RDFS.label, Literal("NCSC")))
        if (APT_dataset_uri, RDF.type, self.TI.Dataset) not in g:
            g.add((APT_dataset_uri, RDF.type, self.TI.Dataset))
            g.add((APT_dataset_uri, RDFS.label, Literal("APT")))
        return NCSC_dataset_uri, APT_dataset_uri
    
    def add_likelihood_to_graph(self, g, likelihood_label, vulnerability_uri):
        likelihood_uri = URIRef(f"http://example.org/threatintelligence/likelihood/{likelihood_label}")
        if (likelihood_uri, RDF.type, self.TI.Likelihood) not in g:
            g.add((likelihood_uri, RDF.type, self.TI.Likelihood))
            g.add((likelihood_uri, RDFS.label, Literal(likelihood_label, datatype=XSD.string)))
        g.add((vulnerability_uri, self.TI.hasLikelihood, likelihood_uri))

    def add_justification_to_graph(self, g, justification, vulnerability_uri):
        justification_uri = URIRef(f"http://example.org/threatintelligence/justification/{justification}")
        if (justification_uri, RDF.type, self.TI.Justification) not in g:
            g.add((justification_uri, RDF.type, self.TI.Justification))
            g.add((justification_uri, RDFS.label, Literal(justification, datatype=XSD.string)))
        g.add((vulnerability_uri, self.TI.hasDescriptionChange, justification_uri))

    def add_product_to_graph(self, g, product_name, dataset_uri, vulnerability_uri):
        product_uri = URIRef(f"http://example.org/threatintelligence/product/{quote(product_name.replace(' ', '_'))}")
        if (product_uri, RDF.type, self.TI.Product) not in g:
            g.add((product_uri, RDF.type, self.TI.Product))
            g.add((product_uri, self.TI.hasProductName, Literal(product_name, datatype=XSD.string)))
        g.add((product_uri, self.TI.fromDataset, dataset_uri))
        g.add((vulnerability_uri, self.TI.affectsProduct, product_uri))
        return product_uri
    
    def add_version_to_graph(self, g, version_name, dataset_uri, product_uri):
        version_uri = URIRef(f"http://example.org/threatintelligence/version/{quote(version_name.replace(' ', '_'))}")
        if (version_uri, RDF.type, self.TI.Version) not in g:
            g.add((version_uri, RDF.type, self.TI.Version))
            g.add((version_uri, self.TI.hasVersionName, Literal(version_name, datatype=XSD.string)))
        g.add((version_uri, self.TI.fromDataset, dataset_uri))
        g.add((product_uri, self.TI.affectsVersion, version_uri))
        return version_uri

    def add_os_to_graph(self, g, os_label, dataset_uri, version_uri):
        os_uri = URIRef(f"http://example.org/threatintelligence/os/{quote(os_label.replace(' ', '_'))}")
        if (os_uri, RDF.type, self.TI.OS) not in g:
            g.add((os_uri, RDF.type, self.TI.OS))
            g.add((os_uri, self.TI.hasOSlabel, Literal(os_label, datatype=XSD.string)))
        g.add((os_uri, self.TI.fromDataset, dataset_uri))
        g.add((version_uri, self.TI.runsOn, os_uri))
        return os_uri
        