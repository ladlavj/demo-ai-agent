from datetime import datetime
from langchain_core.tools import tool

@tool
def get_time_now():
    """
        This would display current time
    """
    now = datetime.now()
    return now
