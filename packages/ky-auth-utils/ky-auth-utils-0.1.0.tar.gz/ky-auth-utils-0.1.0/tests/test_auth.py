import json
from auth import Auth


def test_auth():
    data = {
        'X-AUTH-USER-ID': '123456',
        'X-AUTH-USERNAME': 'test',
        'X-AUTH-USER-OBJ': '{"user_id": "123456", "username": "test"}',
        'X-AUTH-ROLES': 'common',
    }
    auth = Auth.from_dict(data)
    assert auth.user_id == data['X-AUTH-USER-ID']
    assert auth.username == data['X-AUTH-USERNAME']
    assert auth.user == json.loads(data['X-AUTH-USER-OBJ'])
    assert auth.roles == data['X-AUTH-ROLES'].split(',')
    assert auth.has_role('common') is True
    assert auth.has_role('vip') is False
    out = auth.to_dict()
    assert data == out
