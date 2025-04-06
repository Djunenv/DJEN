from pydantic_settings import BaseSettings

class ValidatorSettings(BaseSettings):
    iteration_interval: int = 800
    max_allowed_weights: int = 420
