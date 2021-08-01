import pytest
from .backend import *


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, settings, expected',
    [
        pytest.param('backend_settings_none', '', None, marks=pytest.mark.xfail),
        pytest.param('', '', None, marks=pytest.mark.xfail),
        pytest.param('', '{}', None, marks=pytest.mark.xfail),
        pytest.param('backend_settings_empty', '{}', GenericBackendInterface.Settings()),
        pytest.param('backend_settings_filled',
                     '{"name": "backend_settings_filled", "url": "https://test.url"}',
                     GenericBackendInterface.Settings(name='backend_settings_filled',
                                                      url='https://test.url'))
    ])
def test_generic_backend_create(name, settings, expected):
    backend = GenericBackendInterface(name, settings)
    assert backend
    assert backend.settings == expected


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, settings, enabled, expected',
    [
        pytest.param('backend_settings_empty', '{}', True, True),
        pytest.param('backend_settings_empty', '{}', False, False),
    ])
def test_generic_backend_enabled(name, settings, enabled, expected):
    backend = GenericBackendInterface(name, settings, enabled)
    assert backend.is_enabled() == expected
    backend.enable()
    assert backend.is_enabled() == True
    backend.disable()
    assert backend.is_enabled() == False


@pytest.mark.django_db
def test_generic_backend_same_name():
    backend = GenericBackendInterface('test', '{}', False)
    new_backend = GenericBackendInterface('test')
    assert backend.instance.name == 'test'
    assert backend.is_enabled() == False

    assert new_backend.instance.name == 'test'
    assert new_backend.is_enabled() == False
    assert new_backend.instance.id == backend.instance.id


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, settings, expected',
    [
        pytest.param('log_backend_settings_valid',
                     '{"filename":"test.log"}',
                     LogBackendInterface.Settings(filename='test.log')
                     ),
        pytest.param('log_backend_settings_valid_with_format',
                     '{"filename":"test.log", "format": "%(levelname)s - %(message)s"}',
                     LogBackendInterface.Settings(
                         filename='test.log',
                         format='%(levelname)s - %(message)s'
                        )
                     ),
        pytest.param('log_backend_settings_invalid',
                     '{"file":"test.log"}',
                     LogBackendInterface.Settings(filename='test.log'),
                     marks=pytest.mark.xfail
                     ),
    ])
def test_log_backend_settings(name, settings, expected):
    backend = LogBackendInterface(name, settings)
    assert backend.settings == expected


@pytest.mark.django_db
def test_log_backend_send(tmp_path):
    message = 'test log message'
    expected = 'INFO - ' + message + '\n'
    log_file = tmp_path / 'test.log'
    l = LogBackendInterface('test_log',
                            '{"filename":"'+str(log_file)+'", "format":"%(levelname)s - %(message)s"}')
    l.send(message)
    assert log_file.read_text() == expected


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, settings, expected',
    [
        pytest.param('email_backend_settings_valid',
                     '{"address":"user@test.mail"}',
                     EmailBackendInterface.Settings(address='user@test.mail')
                     ),
        pytest.param('email_backend_settings_invalid',
                     '{"address":"invalid_str"}',
                     EmailBackendInterface.Settings(address='user@test.mail'),
                     marks=pytest.mark.xfail
                     ),
    ])
def test_email_backend_settings(name, settings, expected):
    backend = EmailBackendInterface(name, settings)
    assert backend.settings == expected