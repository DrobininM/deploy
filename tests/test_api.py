import requests
from Config import config
from datetime import datetime, timedelta


def test_auth():
    day_ago = datetime.now() - timedelta(hours=24)
  
    r = requests.post(  
                        f'{config.API_URL}/auth/session',
                        headers={"Authorization": "Bearer 31620f51972845091649802035b423d1"}
                      )
    
    assert r.status_code == 200
    assert datetime.fromisoformat(r.json()["created_at"]) > day_ago


def test_programs_auth_failed():

    r = requests.post(  
                        f'{config.API_URL}/programs',
                        headers={"Authorization": "Bearer 123123123"}
                      )
    
    assert r.status_code == 405


def test_programs():

    auth_response = requests.post(
                                  f'{config.API_URL}/auth/session',
                                  headers={"Authorization": "Bearer 31620f51972845091649802035b423d1"}
                                 )

    programs_response = requests.get(  
                                      f'{config.API_URL}/programs',
                                      headers={"Authorization": f'Bearer {auth_response.json()["session_id"]}'}
                                     )
    
    assert programs_response.status_code == 200


def test_programs_filter_none():

    auth_response = requests.post(  
                                  f'{config.API_URL}/auth/session',
                                  headers={"Authorization": "Bearer 31620f51972845091649802035b423d1"}
                                 )

    programs_response = requests.post(  
                                      f'{config.API_URL}/programs/filter_by',
                                      headers={"Authorization": f'Bearer {auth_response.json()["session_id"]}'}
                                      )
    
    assert programs_response.status_code == 200


def test_programs_filter_empty():

    auth_response = requests.post(  
                                  f'{config.API_URL}/auth/session',
                                  headers={"Authorization": "Bearer 31620f51972845091649802035b423d1"}
                                 )

    programs_response = requests.post(  
                                      f'{config.API_URL}/programs/filter_by',
                                      data={},
                                      headers={"Authorization": f'Bearer {auth_response.json()["session_id"]}'}
                                      )
    
    assert programs_response.status_code == 200


def test_programs_filter():

    auth_response = requests.post(  
                                  f'{config.API_URL}/auth/session',
                                  headers={"Authorization": "Bearer 31620f51972845091649802035b423d1"}
                                 )

    programs_response = requests.post(  
                                      f'{config.API_URL}/programs/filter_by',
                                      json={"field_code": ["15.03.07"]},
                                      headers={"Authorization": f'Bearer {auth_response.json()["session_id"]}'}
                                      )
    
    assert programs_response.status_code == 200


def test_programs_limit_90():

    auth_response = requests.post(  
                                  f'{config.API_URL}/auth/session',
                                  headers={"Authorization": "Bearer 31620f51972845091649802035b423d1"}
                                 )
    
    programs_response = requests.get(  
                                      f'{config.API_URL}/programs?limit=90',
                                      headers={"Authorization": f'Bearer {auth_response.json()["session_id"]}'}
                                    )
    
    assert programs_response.status_code == 200
    assert len(programs_response.json()["programs"]) > 80


def test_programs_limit_10():

    auth_response = requests.post(  
                                  f'{config.API_URL}/auth/session',
                                  headers={"Authorization": "Bearer 31620f51972845091649802035b423d1"}
                                 )
    
    programs_response = requests.get(  
                                      f'{config.API_URL}/programs?limit=10',
                                      headers={"Authorization": f'Bearer {auth_response.json()["session_id"]}'}
                                    )
    
    assert programs_response.status_code == 200
    assert len(programs_response.json()["programs"]) < 20


def test_programs_validation_fail():

    auth_response = requests.post(  
                                  f'{config.API_URL}/auth/session',
                                  headers={"Authorization": "Bearer 31620f51972845091649802035b423d1"}
                                 )
    
    programs_response = requests.get(  
                                      f'{config.API_URL}/programs?limit=asd',
                                      headers={"Authorization": f'Bearer {auth_response.json()["session_id"]}'}
                                    )
    
    assert programs_response.status_code == 422


def test_fields():

    auth_response = requests.post(  
                                  f'{config.API_URL}/auth/session',
                                  headers={"Authorization": "Bearer 31620f51972845091649802035b423d1"}
                                 )

    fields_response = requests.get(  
                                      f'{config.API_URL}/fields/',
                                      headers={"Authorization": f'Bearer {auth_response.json()["session_id"]}'}
                                  )
    
    assert fields_response.status_code == 200
