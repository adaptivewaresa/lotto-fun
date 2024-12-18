class Config:
    """Base configuration."""
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
