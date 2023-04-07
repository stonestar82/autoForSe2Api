# -*- coding: utf-8 -*-
import os
import json


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA = json.loads(open('{}/config.json'.format(ROOT_DIR)).read())


class JsonConfig:
    @staticmethod
    def get_data(varname, value=None):
        return DATA.get(varname) or os.environ.get(varname) or value

    @staticmethod
    def set_data(key, value):
        DATA[key] = value
        with open('{}/config.json'.format(ROOT_DIR), 'w') as f:
            json.dump(DATA, f, indent=4)


# app config
class AppConfig:
    ROOT_DIR = ROOT_DIR
    STATIC_DIR = '{0}/static'.format(ROOT_DIR)
    TEMPLATES_DIR = '{0}/templates'.format(ROOT_DIR)
    ERROR_CODE = {
        40000: 'Bad Request',
        41000: 'Gone',
        40300: 'Forbidden',
        40400: 'Not Found',
        50000: 'Internal Server Error',
    }

    APP_MODE_PRODUCTION = 'production'
    APP_MODE_DEVELOPMENT = 'development'
    APP_MODE_TESTING = 'testing'

    APP_MODE = JsonConfig.get_data('APP_MODE', APP_MODE_PRODUCTION)
    APP_HOST = JsonConfig.get_data('APP_HOST', '0.0.0.0')
    APP_PORT = int(JsonConfig.get_data('APP_PORT', 80))

    DB_USER_NAME = JsonConfig.get_data('DB_USER_NAME', 'root')
    DB_USER_PASSWD = JsonConfig.get_data('DB_USER_PASSWD', 'password')
    DB_HOST = JsonConfig.get_data('DB_HOST', 'localhost')
    DB_NAME = JsonConfig.get_data('DB_NAME', 'flask')
    REDIS_HOST = JsonConfig.get_data('REDIS_HOST', 'localhost')
    REDIS_PASSWD = JsonConfig.get_data('REDIS_PASSWD')
    
    @staticmethod
    def from_app_mode():
        mode = {
            AppConfig.APP_MODE_PRODUCTION: 'config.ProductionConfig',
            AppConfig.APP_MODE_DEVELOPMENT: 'config.DevelopmentConfig',
            AppConfig.APP_MODE_TESTING: 'config.TestingConfig',
        }
        return mode.get(AppConfig.APP_MODE, mode[AppConfig.APP_MODE_DEVELOPMENT])

    @staticmethod
    def database_url(dialect='mysql'):
      
        return '{}://{}:{}@{}/{}?charset=utf8'.format(dialect, AppConfig.DB_USER_NAME, AppConfig.DB_USER_PASSWD,
                                                      AppConfig.DB_HOST, AppConfig.DB_NAME)


# flask config
class FlaskConfig:
    SECRET_KEY = '9022b99ae34ae74ec06bbeac8653b6c98a6ff9ee66ac4f96'
    SQLALCHEMY_DATABASE_URI = AppConfig.database_url()
    # https://stackoverflow.com/questions/33738467/how-do-i-know-if-i-can-disable-sqlalchemy-track-modifications
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False


class ProductionConfig(FlaskConfig):
    pass


class DevelopmentConfig(FlaskConfig):
    SQLALCHEMY_ECHO = True
    DEBUG = True
    TESTING = True


class TestingConfig(FlaskConfig):
    TESTING = True
