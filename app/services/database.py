import os
from dotenv import load_dotenv

from opensearchpy import OpenSearch

load_dotenv()

def init_opensearch():
    OS_API_URL = os.getenv("OS_API_URL")
    OS_API_ID = os.getenv("OS_API_USER")
    OS_API_KEY = os.getenv("OS_API_PWD")

    os_client = OpenSearch(
        hosts=OS_API_URL,
        http_auth=(OS_API_ID, OS_API_KEY),
        http_compress=True,
        verify_certs=False,
        ssl_show_warn=False
    )
    return os_client

os_client = init_opensearch()