# config.py
import os


class Config(object):
    """
    Common configurations
    """

    # Put any configurations here that are common across all environments
    DOMAIN = os.environ.get('KEEMAIL_DOMAIN')


class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
