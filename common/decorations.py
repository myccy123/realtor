# -*- coding: utf-8 -*-
from utils.log import Logger
from utils.jsonutil import *
from django.shortcuts import HttpResponse

log = Logger(__name__)
logger = log.get_logger()


def http_log():
    def inner(func):
        def wrapper(*args, **kwargs):
            request = args[0]
            logger.info('%s %s', request.method, request.build_absolute_uri())
            logger.info('request cookies   ↓↓↓↓↓↓↓\n %s',
                        dumps(dict(request.COOKIES)))
            logger.info('request params   ↓↓↓↓↓↓↓\n %s',
                        dumps(getattr(request, request.method)))
            logger.info('request body     ↓↓↓↓↓↓↓\n %s',
                        request.body.decode())
            result = func(*args, **kwargs)
            logger.info('response content ↓↓↓↓↓↓↓\n %s',
                        result.content.decode())
            return result

        return wrapper

    return inner
