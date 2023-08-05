__version__ = "0.0.4"
import logging

logger = logging.getLogger()
logger.disabled = True

try:
    import airflow

    from . import cli
    from . import http
    from . import models
    from . import utils

except ImportError as e:
    print(
        "Airflow must be installed for Windmill to run. To install windmill with the tested version of airflow run:\n   pip install airflow-windmill[airflow]"
    )

logger.disabled = False
