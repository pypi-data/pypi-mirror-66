import time
import statsd
import functools
from contextlib import ContextDecorator
from .metrics import create_external_service_duration_metrics, create_function_duration_metrics, create_external_io_counter_metric
from .metrics import add_label_to_metric_without_mapping, logger
from .metrics import APP_NAME
from .helpers import get_hostname
from .constants import TAG_REDIS, TAG_MYSQL, TAG_API, TAG_ELASTICSEARCH, TAG_OTHER, TAG_MEMCACHE


class collect_external_io_metrics(ContextDecorator):

    def __init__(self, metric_prefix_app_name, service_name, service_address=None, service_tag=TAG_OTHER, custom_labels_dict=None):
        """
            Decorator /context-manager  to collect metrics from the wrapped function calling an external service. This is a lower level function if a custom tag is to be provided please use other decorators functions such as measure_api_io etc

            It returns the following metrics:
                1. service_name_external_io_duration_ms:
                   Labels: name, address, tag

                2. Counter based exception metric to count types of Exception raised during the external service call. Only created if status is 'error'.
                   error name will be the name of error class raised
            Attributes:
            metric_prefix_app_name: deprecated and does not serve any purpose, just there for compatibilty.
            service_address: defaults to hostname of the host running this code. Should be the address to which service is pointing/calling
            service_tag: can be one of the tags defined in constants file.
            custom_labels_dict dict: custom labels for metrics please don't use unnecessarily
        """
        if not service_address:
            self.service_address = get_hostname()
        self.io_name = service_name
        self.io_address = service_address
        self.io_tag = service_tag
        self.custom_labels_dict = custom_labels_dict

    def __enter__(self):
        """
            Attributes:
            ----------
            io_type str: Can be any one of the TAGS defined in constants .
                         e.g TAG_REDIS, TAG_OTHER etc.

        """
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        """
        stop_time = time.time()
        time_taken_ms = (stop_time - self.start_time)*1000
        if exc_type:
            status = 'error'
            exception_type = exc_type.__class__.__name__
        else:
            status = 'success',
            exception_type = None

        metric_name = create_external_service_duration_metrics(status, time_taken_ms, self.io_name,
                                                               self.io_address,
                                                               self.io_tag,
                                                               exception_type,
                                                               self.custom_labels_dict
                                                               )


def collect_function_duration_metrics(function_name):
    """
        Pushes metrics that measure function runtime as histogram and exception type counter
        It returns the following metrics:
            1. function_duration_ms:
               Labels:
               function_name

            2. external_io_total: Counter based exception metric to count types of Exception raised during the function call. Only created if status is 'error'.

        Attributes:
        ----------
        function_name str: function for which the metrics are collected.
    """
    def inner_func(func):
        @functools.wraps(func)
        def wrapper_decorator(*args, **kwargs):
            start_time = time.time()
            try:
                value = func(*args, **kwargs)
                end_time = time.time()
                duration_ms = (end_time - start_time)*1000

            except Exception as e:
                status = 'error'
                end_time = time.time()
                duration_ms = (end_time - start_time)*1000
                exception_type = e.__class__.__name__
                create_function_duration_metrics(
                    duration_ms, function_name, status, exception_type)
                raise

            else:
                status = 'success'
                create_function_duration_metrics(
                    duration_ms, function_name, status)

            return value
        return wrapper_decorator
    return inner_func


def measure_redis_io(name, address=None, custom_labels_dict=None):
    """
        decorator to measure runtime of function which makes redis io calls please make sure no other time consuming io calls inside decorated function.
        Attributes:
        -----------
        name: user friendly name for the function being decorated.
    """
    return collect_external_io_metrics(APP_NAME, name, TAG_REDIS, address, custom_labels_dict)


def measure_api_io(name, address=None, custom_labels_dict=None):
    """
        decorator /context-manager  to measure runtime of function which makes reexternal api calls please make sure no other time consuming io calls inside decorated function.
        Attributes:
        -----------
        name: user friendly name for the function being decorated.
    """
    return collect_external_io_metrics(APP_NAME, name, TAG_API, address, custom_labels_dict)


def measure_memcache_io(name, address=None, custom_labels_dict=None):
    """
        decorator  /context-manager to measure runtime of function which makes memcache io calls please make sure no other time consuming io calls inside decorated function.
        Attributes:
        -----------
        name: user friendly name for the function being decorated.
    """
    return collect_external_io_metrics(APP_NAME, name, TAG_MEMCACHE, address, custom_labels_dict)


def measure_mysql_io(name, address=None, custom_labels_dict=None):
    """
        decorator /context-manager to measure runtime of function which makes mysql io calls please make sure no other time consuming io calls inside decorated function.
        Attributes:
        -----------
        name: user friendly name for the function being decorated.
    """
    return collect_external_io_metrics(APP_NAME, TAG_MYSQL, address, custom_labels_dict)


def measure_elasticsearch_io(name, address=None, custom_labels_dict=None):
    """
        decorator/context-manager to measure runtime of function which makes elasticsearch io calls please make sure no other time consuming io calls inside decorated function.
        Attributes:
        -----------
        name: user friendly name for the function being decorated.
    """
    return collect_external_io_metrics(APP_NAME, name, TAG_ELASTICSEARCH, address,
                                       custom_labels_dict)


def measure_other_io(name, address=None, custom_labels_dict=None):
    return collect_external_io_metrics(APP_NAME, name, TAG_OTHER, address, custom_labels_dict)
