import json
import os

from .. import config
from .. import global_vars
from .. import json_encoders
from .. import utils
from ..problem import ProblemSession


def fatal(error):
    print(error)
    exit(0)


def load_session():
    try:
        if os.path.exists(config.get_session_file_path()):
            session_data_json = open(config.get_session_file_path(), 'r').read()
        elif os.path.exists(os.path.join('..', config.get_session_file_path())):
            config.internal_directory_path = os.path.join('..', config.internal_directory_path)
            session_data_json = open(config.get_session_file_path(), 'r').read()
        else:
            return False
        session_data = json.loads(session_data_json, object_hook=json_encoders.my_json_decoder)
        global_vars.problem = ProblemSession(config.polygon_url, session_data["problemId"])
        global_vars.problem.use_ready_session(session_data)
        return True
    except:
        return False


def save_session():
    session_data = global_vars.problem.dump_session()
    session_data_json = json.dumps(session_data, sort_keys=True, indent='  ', default=json_encoders.my_json_encoder)
    utils.safe_rewrite_file(config.get_session_file_path(), session_data_json)
