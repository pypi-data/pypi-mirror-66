import json
import os

from .util import app_dir


class DeploymentType:
    SOLO = "SOLO"  # 也就是本地模式
    DEV = "DEV"  # 开发环境
    QA = "QA"  # 测试环境
    UAT = "UAT"  # 预生产环境
    PROD = "PROD"  # 生产环境
    dict = {
        SOLO: "SOLO",
        DEV: "DEV",
        QA: "QA",
        UAT: "UAT",
        PROD: "PROD"
    }


default_config = {
    'port': 8000,
    'app_name': '',
    'default_host': '',
    'env': DeploymentType.SOLO,
    'app_settings': {
        'debug': True,
        'xsrf_cookies': True,
    },
    'log': {
        'log_file_path': app_dir + '/app.log',
        'logging_level': 'DEBUG',
        'log_to_level_files': False,
        'log_to_stderr': True,
        'log_file_max_size': 100 * 1000 * 1000,
        'log_file_num_backups': 30,
        'log_rotate_when': 'D',
        'log_rotate_interval': 1,
        'log_rotate_mode': 'time'
    },
    'middleware_classes': []
}


def load_config_dir(config_file_dir='', profile=''):
    _config = default_config
    if not config_file_dir:
        config_file_dir = app_dir + '/conf'  # 默认的配置目录

    config_files = ['application.json']
    if profile:
        config_files.append('application-' + profile.lower() + '.json')

    try:
        files = os.listdir(config_file_dir)
    except FileNotFoundError:
        files = []

    for file in config_files:
        if file in files:
            c = load_config_file(config_file_dir + '/' + file)
            _config = {**_config, **c}

    return _config


def load_config_file(config_file):
    with open(config_file) as f:
        _config = json.load(f)
    return _config
