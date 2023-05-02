import os
import logging
import jsonpickle
import boto3
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all
from harmony.schemas.requests.text import RawFile
from harmony.parser import convert_files_to_instruments
from pydantic import parse_obj_as
from typing import List
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)
patch_all()

client = boto3.client('lambda')
client.get_account_settings()

def lambda_handler(event, context):
    logger.info('## ENVIRONMENT VARIABLES\r' + jsonpickle.encode(dict(**os.environ)))
    logger.info('## EVENT\r' + jsonpickle.encode(event))
    logger.info('## CONTEXT\r' + jsonpickle.encode(context))
    files = parse_obj_as(List[RawFile],json.loads(event["body"]))
    for file in files:
        if file.file_id is None:
            file.file_id = uuid.uuid4().hex
    
    return convert_files_to_instruments(files)
