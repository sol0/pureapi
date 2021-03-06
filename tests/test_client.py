from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from pureapi import client
import pprint
from addict import Dict

def test_get():
  r_persons = client.get('persons', {'size':1, 'offset':0})
  assert r_persons.status_code == 200

  r = client.get('organisational-units', {'size':1, 'offset':0})
  assert r.status_code == 200

  d = r.json()
  assert d['count'] > 0
  assert len(d['items']) == 1

  org = d['items'][0]
  uuid = org['uuid']

  r_uuid = client.get('organisational-units/' + uuid, {'size':1, 'offset':0})
  assert r_uuid.status_code == 200

  d_uuid = r.json()
  assert d_uuid['count'] > 0
  assert len(d_uuid['items']) == 1

  org_uuid = d_uuid['items'][0]
  assert org_uuid['uuid'] == uuid

def test_get_all_transformed():
  r = client.get('organisational-units', {'size':1, 'offset':0})
  d = r.json()
  count = d['count']

  transformed_count = 0
  for org in client.get_all_transformed('organisational-units'):
    assert isinstance(org, Dict)
    assert 'uuid' in org
    transformed_count += 1
  assert transformed_count == count

  for person in client.get_all_transformed('persons'):
    assert isinstance(person, Dict)
    assert 'uuid' in person
    break

def test_filter():
  payload = {
    "size": 1,
    "offset": 0,
    "forOrganisationalUnits": {
      "uuids": [
        "2db56085-27ed-460a-8037-aeef0fd38efa"
      ]
    }
  }
  r = client.filter('research-outputs', payload)
  assert r.status_code == 200

  d = r.json()
  assert d['count'] > 0
  assert len(d['items']) == 1

def test_filter_all_transformed():
  type_uri = "/dk/atira/pure/organisation/organisationtypes/organisation/peoplesoft_deptid"
  payload = {
    "organisationalUnitTypeUri": [ 
      type_uri
    ]
  }
  r = client.filter('organisational-units', payload)
  d = r.json()
  count = d['count']

  transformed_count = 0
  for org in client.filter_all_transformed('organisational-units', payload):
    assert isinstance(org, Dict)
    assert 'uuid' in org
    assert org['type'][0]['uri'] == type_uri
    transformed_count += 1
  assert transformed_count == count

