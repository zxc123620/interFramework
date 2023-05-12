import pytest
import requests

from utils.api_keywords.ApiKeyWords import ApiKeyword


@pytest.fixture(scope="session")
def login():
    data = {
        "accounts": 'zxc',
        'pwd': '123456',
        'type': 'username'
    }
    res = ApiKeyword.post("http://shop-xo.hctestedu.com?s=api/user/login&application=app", data=data)
    if res.status_code == requests.codes.ok:
        return ApiKeyword.get_text(res.text, "$.data.token")
    else:
        res.raise_for_status()

