import rdfalchemy
from rdfalchemy.samples.doap import FOAF
from rdfalchemy.samples.foaf import Person
from rdfalchemy.orm import mapper
from rdflib import ConjunctiveGraph

import logging
log = logging.getLogger('rdfalchemy')
if not log.handlers:
    log.addHandler(logging.StreamHandler())
#log.setLevel(10)


Person.db = ConjunctiveGraph()
Person.knows = rdfalchemy.rdfMultiple(FOAF.knows, range_type=FOAF.Person)


def test_start():
    assert len(Person.db) == 0
    p = Person(last="Cooper", first="Philip")
    assert len(Person.db) == 3
    del p


def test_addBNodeKnowsL():
    Person.knows = rdfalchemy.rdfList(FOAF.knows, range_type=FOAF.Person)
    mapper()
    p1 = Person.get_by(first="Philip")
    p2 = Person(last="Cooper", first="Ben")
    p3 = Person(last="Cooper", first="Matt")
    assert len(Person.db) == 9
    p1.knows = [p2, p3]
    print(len(Person.db))
    assert len(Person.db) == 14
    del p1.knows
    print(len(Person.db))
    assert len(Person.db) == 3


def test_addBNodeKnowsM():
    Person.knows = rdfalchemy.rdfMultiple(FOAF.knows, range_type=FOAF.Person)
    p1 = Person.get_by(first="Philip")
    p2 = Person(last="Cooper", first="Ben")
    p3 = Person(last="Cooper", first="Matt")
    assert len(Person.db) == 9
    p1.knows = [p2, p3]
    print(len(Person.db))
    assert len(Person.db) == 11
    del p1.knows
    print(len(Person.db))
    assert len(Person.db) == 3
