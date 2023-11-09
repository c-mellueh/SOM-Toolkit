import os
import uuid
import datetime
DIR_PATH = os.path.dirname(__file__)
LOG_PATH = os.path.join(DIR_PATH, f"{datetime.date.today()}_{uuid.uuid4()}.log")
