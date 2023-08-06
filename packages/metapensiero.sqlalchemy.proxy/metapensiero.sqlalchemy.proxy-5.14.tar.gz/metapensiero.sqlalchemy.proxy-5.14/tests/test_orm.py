# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.proxy -- Tests for ProxiedEntity
# :Created:   dom 19 ott 2008 00:04:34 CEST
# :Author:    Lele Gaifax <lele@nautilus.homeip.net>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2008, 2013, 2014, 2015, 2016, 2017, 2018, 2020 Lele Gaifax
#

from __future__ import absolute_import

from datetime import date

from metapensiero.sqlalchemy.proxy.orm import ProxiedEntity
from fixture import Complex, Person, PairedPets, Pet, Session, setup, teardown


def test_basic():
    proxy = ProxiedEntity(Person, 'id,firstname,title'.split(','))

    sas = Session()

    res = proxy(sas, result='root', count='count',
                filter_col='lastname', filter_value='foo')
    assert res['message'] == 'Ok'
    assert res['count'] == 0

    res = proxy(sas, result='root', count='count',
                filter_by_lastname='foo', filter_by_firstname='bar')
    assert res['message'] == 'Ok'
    assert res['count'] == 0

    res = proxy(sas, Person.firstname == 'Lele', result='root', count='count')
    assert res['message'] == 'Ok'
    assert res['count'] == len(res['root'])
    assert res['root'][0].title == "Perito Industriale"

    res = proxy(sas, Person.firstname == 'Lele', Person.lastname == 'Gaifax',
                result='root', count='count')
    assert res['message'] == 'Ok'
    assert res['count'] == 0

    res = proxy(sas, result='root', count="count",
                filter_col='firstname', filter_value='Lele')
    assert res['message'] == 'Ok'
    assert res['count'] == len(res['root'])
    assert res['root'][0].title == "Perito Industriale"


def test_boolean():
    proxy = ProxiedEntity(Person, 'id,firstname'.split(','))

    sas = Session()

    res = proxy(sas, result='root', count='count', filter_by_smart='true')
    assert res['message'] == 'Ok'
    assert res['count'] == 1

    res = proxy(sas, result='root', count="count", filter_by_smart='false')
    assert res['message'] == 'Ok'
    assert res['count'] == len(res['root'])
    assert res['root'][0].firstname == u'Lele'

    res = proxy(sas, result=False, only_cols='["firstname","lastname"]')
    assert res['message'] == 'Ok'


def test_basic_decl():
    proxy = ProxiedEntity(Pet)

    sas = Session()

    res = proxy(sas, result='root', count='count',
                filter_col='name', filter_value='Yacu')
    assert res['message'] == 'Ok'
    assert res['count'] == 1


def test_metadata():
    proxy = ProxiedEntity(Person, 'id,smart,title'.split(','),
                          dict(smart=dict(label='Some value',
                                          hint='A value from a set',
                                          default=False,
                                          dictionary=((0, 'low'),
                                                      (1, 'medium'),
                                                      (2, 'high')))))

    sas = Session()

    res = proxy(sas, success='success', result=None, metadata='metadata')
    assert res['success'] is True
    assert res['metadata'].get('root_slot') is None
    fields = res['metadata']['fields']
    assert len(fields) == 3
    assert fields[1]['default'] is False
    assert fields[1]['dictionary'] == [[0, 'low'],
                                       [1, 'medium'],
                                       [2, 'high']]
    assert fields[2]['type'] == 'string'

    proxy = ProxiedEntity(
        Person,
        'id,firstname,lastname,birthdate,somevalue'.split(','),
        dict(firstname=dict(label='First name',
                            hint='First name of the person'),
             lastname=lambda fname: dict(label='Foo'),
             somevalue=dict(label='Some value',
                            hint='A value from a set',
                            dictionary={0: 'low',
                                        1: 'medium',
                                        2: 'high'})))
    proxy.translate = lambda msg: msg.upper()

    res = proxy(sas, success='success', result='root', count='count',
                metadata='metadata', filter_by_firstname='Lele', asdict=True)
    assert res['success'] is True
    assert res['message'] == 'Ok'
    assert res['count'] == 1
    fields = res['metadata']['fields']
    assert len(fields) == 5
    assert fields[1]['label'] == 'FIRST NAME'
    assert fields[2]['label'] == 'FOO'
    assert fields[3]['min'] == date(1980, 1, 1)
    assert fields[3]['max'] == date.today()
    assert fields[4]['dictionary'] == {0: 'LOW', 1: 'MEDIUM', 2: 'HIGH'}
    assert res['metadata']['count_slot'] == 'count'
    assert res['metadata']['root_slot'] == 'root'
    assert res['metadata']['success_slot'] == 'success'
    assert isinstance(res['root'][0], dict)

    proxy = ProxiedEntity(Pet, 'id,name,birthdate,weight,notes'.split(','),
                          dict(name=dict(label='Pet name',
                                         hint='The name of this pet')))

    res = proxy(sas, result=False, metadata='metadata')
    assert res['message'] == 'Ok'
    fields = res['metadata']['fields']
    assert len(fields) == 5
    assert fields[0]['label'] == 'id'
    assert fields[0]['hint'] == 'the pet id'
    assert fields[1]['label'] == 'Pet name'
    assert fields[1]['hint'] == 'The name of this pet'
    assert fields[2]['min'] == date(1980, 1, 1)
    assert fields[2]['max'] == date.today()
    assert fields[3]['decimals'] == 2
    assert res['metadata']['primary_key'] == 'id'

    proxy = ProxiedEntity(Complex)
    res = proxy(sas, result=False, metadata='metadata')
    assert res['metadata']['primary_key'] == ('id1', 'id2')

    proxy = ProxiedEntity(Pet)
    res = proxy(sas, result=False, metadata='metadata')
    fields = res['metadata']['fields']
    assert fields[4]['name'] == 'weight'
    assert fields[4]['decimals'] == 2
    assert fields[5]['name'] == 'notes'
    assert fields[5]['type'] == 'text'

    proxy = ProxiedEntity(PairedPets)
    res = proxy(sas, result=False, metadata='metadata')
    assert res['metadata']['primary_key'] == 'id'
    fields = res['metadata']['fields']
    assert fields[0]['name'] == 'id'
    assert 'default' not in fields[0]
    assert fields[1]['name'] == 'pet1_id'
    assert fields[1]['foreign_keys'] == ('pets.id',)


def test_query():
    proxy = ProxiedEntity(Person)

    sas = Session()

    res = proxy(sas, query=u"Lele", fields="firstname,lastname,nickname")
    assert len(res) == 1

    res = proxy(sas, query=u"Lele", fields="firstname")
    assert len(res) == 1

    res = proxy(sas, query=u"perito")
    assert len(res) == 1

    res = proxy(sas, query=u"aifa", fields="firstname,lastname,nickname")
    assert len(res) > 1


def test_filters():
    proxy = ProxiedEntity(Person)

    sas = Session()

    res = proxy(sas, filters=[dict(property='firstname', value=u"=Lele")])
    assert len(res) == 1

    res = proxy(sas, filters=[dict(property='firstname')])
    assert len(res) > 1

    res = proxy(sas, filters=[dict(value=u'=Lele')])
    assert len(res) > 1

    res = proxy(sas, filters=[dict(property='firstname', value=u"Lele",
                                   operator='=')])
    assert len(res) == 1

    res = proxy(sas, filters=[dict(property='lastname', value=u"aifa")])
    assert len(res) > 1

    res = proxy(sas, filters=[dict(property='lastname', value=u"aifa",
                                   operator='~')])
    assert len(res) > 1


def test_dict():
    proxy = ProxiedEntity(Person, 'id,firstname,lastname,goodfn'.split(','))

    sas = Session()

    res = proxy(sas, limit=1, asdict=True)
    assert len(res) == 1
    p = res[0]
    for f in ('id', 'firstname', 'lastname', 'goodfn'):
        assert f in p
    assert 'birthdate' not in p


def test_plain_entities():
    proxy = ProxiedEntity(Person)

    sas = Session()

    res = proxy(sas, filter_by_firstname='Lele')
    assert len(res) == 1
    p = res[0]
    assert p.firstname == 'Lele'
    assert isinstance(p, Person)


def test_sort():
    proxy = ProxiedEntity(Person)

    sas = Session()

    res = proxy(sas, sort_col="firstname")
    assert res[0].firstname < res[1].firstname

    res = proxy(sas, sort_col="lastname,firstname")
    assert res[0].firstname < res[1].firstname

    res = proxy(sas, sort_col="firstname", sort_dir="DESC")
    assert res[0].firstname > res[1].firstname

    res = proxy(sas, sorters='[{"property":"firstname","direction":"DESC"}]')
    assert res[0].firstname > res[1].firstname

    res = proxy(sas, sorters=dict(property="firstname", direction="DESC"))
    assert res[0].firstname > res[1].firstname


def test_sort_multiple():
    proxy = ProxiedEntity(Person)

    sas = Session()

    res = proxy(sas, sorters=[dict(property="firstname", direction="ASC")])
    assert res[0].firstname < res[1].firstname

    res = proxy(sas, sorters=[dict(property="firstname", direction="DESC")])
    assert res[0].firstname > res[1].firstname

    res = proxy(sas, sorters=[dict(property="somevalue"),
                              dict(property="birthdate", direction="DESC")])
    assert res[0].birthdate > res[1].birthdate


def test_orm_queries():
    from sqlalchemy.orm import Query

    sas = Session()

    query = Query([Pet])
    proxy = ProxiedEntity(query)

    res = proxy(sas, sort_col="name")
    assert res[0].name < res[1].name

    query = Query([Pet])
    proxy = ProxiedEntity(query, fields=['name', 'birthdate'])
    res = proxy(sas, success='success', result=None, metadata='metadata')
    assert res['success'] is True
    assert res['metadata'].get('root_slot') is None
    assert len(res['metadata']['fields']) == 2
    assert res['metadata']['fields'][0]['label'] == "Pet name"


# Silence pylint
setup, teardown
