import pytest
from testservice.backend import *



@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, parameters, expected',
    [
        pytest.param('backend_parameters_none', '', None, marks=pytest.mark.xfail),
        pytest.param('', '', None, marks=pytest.mark.xfail),
        pytest.param('', '{}', None, marks=pytest.mark.xfail),
        pytest.param('backend_parameters_empty', '{}', {}),
        pytest.param('backend_parameters_filled',
                     '{"name": "backend_parameters_filled", "url": "https://test.url"}',
                     {'name':'backend_parameters_filled', 'url':'https://test.url'})
    ])
def test_generic_backend_create(name, parameters, expected):
    backend = GenericBackend(name, parameters)
    assert backend
    assert backend.parameters == expected


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, parameters, enabled, expected',
    [
        pytest.param('backend_parameters_empty', '{}', True, True),
        pytest.param('backend_parameters_empty', '{}', False, False),
    ])
def test_generic_backend_enabled(name, parameters, enabled, expected):
    backend = GenericBackend(name, parameters, enabled)
    assert backend.is_enabled() == expected
    backend.enable()
    assert backend.is_enabled() == True
    backend.disable()
    assert backend.is_enabled() == False


@pytest.mark.django_db
def test_generic_backend_same_name():
    backend = GenericBackend('test', '{}', False)
    new_backend = GenericBackend('test')
    assert backend.instance.name == 'test'
    assert backend.is_enabled() == False

    assert new_backend.instance.name == 'test'
    assert new_backend.is_enabled() == False
    assert new_backend.instance.id == backend.instance.id