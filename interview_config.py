from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MIN_COMPENSATION: int = 95000
    MAX_COMPENSATION: int = 600000
    P25_COMPENSATION: int = 192000
    MEDIAN_COMPENSATION: int = 254000
    P75_COMPENSATION: int = 348000
    P90_COMPENSATION: int = 455000

    MIN_INTERVIEW_LENGTH: float = 0.25
    MAX_INTERVIEW_LENGTH: float = 2.0
    MAX_CANDIDATES_TO_CONSIDER: int = 1000
    DEFAULT_SELF_ASSESSMENT_TIME: float = 1.0
    DEFAULT_INTERVIEW_LENGTH: float = 1.0

    class Config:
        env_file = ".env"


settings = Settings()
