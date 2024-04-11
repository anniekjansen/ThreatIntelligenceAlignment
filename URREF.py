from owlready2 import *

URREF = get_ontology("URREF.owl").load()

for cls in URREF.classes():
    print(cls)

# print(URREF.search(iri = "*Criterion"))
# print(URREF.search(iri = "*EvaluationCriterion"))
# EC = URREF.search_one(iri = "*EvaluationCriterion")


my_drug = URREF['Evaluation']("my_drug") # this works

# my_drug = URREF['EvaluationCriterion']("my_drug") # this does not work
# my_drug = URREF["http://eturwg.c4i.gmu.edu/ontologies/URREF.owl#EvaluationCriterion"]("my_drug") #this does not work

# "http://eturwg.c4i.gmu.edu/ontologies/URREF.owl#EvaluationCriterion"

#print(URREF['http://eturwg.c4i.gmu.edu/ontologies/URREF.owl#EvaluationCriterion'])

# class Drug(Thing):
#     namespace = URREF

# print(Drug.iri)


# print(URREF['Evaluation'])
# print(URREF['EvaluationCriterion']) #None?

print("URREF classes:")
classes = list(URREF.classes())
print(classes)
# print("URREF individuals:")
# print(list(URREF.individuals()))
# print("")

for c in classes:
    print(c)
    print(c.iri)
    class_name = str(c) 
    class_name = class_name.replace('URREF.', '')
    print(class_name)
    c.iri = "http://eturwg.c4i.gmu.edu/files/ontologies/URREF.owl#{class_name}".format(class_name=class_name)
    print(c.iri)

my_drug = URREF['EvaluationCriterion']("my_drug") # this now works

print(URREF['Evaluation'])
print(URREF['EvaluationCriterion'])

URREF.save(file = "URREF_1.owl", format = "rdfxml")
# URREF.save(file = "URREF_1.ttl", format = "ntriples")

