import pytest

import datetime

from great_expectations.core.metric import ValidationMetricIdentifier
from great_expectations.data_context.util import instantiate_class_from_config


from great_expectations.core import ExpectationSuiteValidationResult, ExpectationValidationResult, \
    ExpectationConfiguration


@pytest.fixture(params=[
    {
        "class_name": "EvaluationParameterStore",
        "store_backend": {
            "class_name": "DatabaseStoreBackend",
            "credentials": {
                "drivername": "postgresql",
                "username": "postgres",
                "password": "",
                "host": "localhost",
                "port": "5432",
                "database": "test_ci"
            }
        }
    },
    {
        "class_name": "EvaluationParameterStore",
        "module_name": "great_expectations.data_context.store"
    }
])
def param_store(request, test_backends):
    if "postgresql" not in test_backends:
        pytest.skip("skipping fixture because postgresql not selected")

    return instantiate_class_from_config(
        config=request.param,
        config_defaults={
            "module_name": "great_expectations.data_context.store",
        },
        runtime_environment={}
    )


def test_evaluation_parameter_store_methods(data_context):
    run_id = "20191125T000000.000000Z"
    source_patient_data_results = ExpectationSuiteValidationResult(
        meta={
            "expectation_suite_name": "source_patient_data.default",
            "run_id": run_id
        },
        results=[
            ExpectationValidationResult(
                expectation_config=ExpectationConfiguration(
                    expectation_type="expect_table_row_count_to_equal",
                    kwargs={
                        "value": 1024,
                    }
                ),
                success=True,
                exception_info={
                    "exception_message": None,
                    "exception_traceback": None,
                    "raised_exception": False},
                result={
                    "observed_value": 1024,
                    "element_count": 1024,
                    "missing_percent": 0.0,
                    "missing_count": 0
                }
            )
        ],
        success=True
    )

    data_context.store_evaluation_parameters(source_patient_data_results)

    bound_parameters = data_context.evaluation_parameter_store.get_bind_params(run_id)
    assert bound_parameters == {
        'urn:great_expectations:validations:source_patient_data.default:expect_table_row_count_to_equal.result'
        '.observed_value': 1024
    }
    source_diabetes_data_results = ExpectationSuiteValidationResult(
        meta={
            "expectation_suite_name": "source_diabetes_data.default",
            "run_id": run_id
        },
        results=[
            ExpectationValidationResult(
                expectation_config=ExpectationConfiguration(
                    expectation_type="expect_column_unique_value_count_to_be_between",
                    kwargs={
                        "column": "patient_nbr",
                        "min": 2048,
                        "max": 2048
                    }
                ),
                success=True,
                exception_info={
                    "exception_message": None,
                    "exception_traceback": None,
                    "raised_exception": False},
                result={
                    "observed_value": 2048,
                    "element_count": 5000,
                    "missing_percent": 0.0,
                    "missing_count": 0
                }
            )
        ],
        success=True
    )

    data_context.store_evaluation_parameters(source_diabetes_data_results)
    bound_parameters = data_context.evaluation_parameter_store.get_bind_params(run_id)
    assert bound_parameters == {
        'urn:great_expectations:validations:source_patient_data.default:expect_table_row_count_to_equal.result'
        '.observed_value': 1024,
        'urn:great_expectations:validations:source_diabetes_data.default'
        ':expect_column_unique_value_count_to_be_between.result.observed_value:column=patient_nbr': 2048
    }


def test_database_evaluation_parameter_store_basics(param_store):
    run_id = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%S.%fZ")
    metric_identifier = ValidationMetricIdentifier(
        run_id=run_id,
        expectation_suite_identifier="asset.warning",
        metric_name="expect_column_values_to_match_regex.result.unexpected_percent",
        metric_kwargs_id="column=mycol"
    )
    metric_value = 12.3456789

    param_store.set(metric_identifier, metric_value)
    value = param_store.get(metric_identifier)
    assert value == metric_value


def test_database_evaluation_parameter_store_get_bind_params(param_store):
    # Bind params must be expressed as a string-keyed dictionary.
    # Verify that the param_store supports that
    run_id = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%S.%fZ")
    metric_identifier = ValidationMetricIdentifier(
        run_id=run_id,
        expectation_suite_identifier="asset.warning",
        metric_name="expect_column_values_to_match_regex.result.unexpected_percent",
        metric_kwargs_id="column=mycol"
    )
    metric_value = 12.3456789
    param_store.set(metric_identifier, metric_value)

    metric_identifier = ValidationMetricIdentifier(
        run_id=run_id,
        expectation_suite_identifier="asset.warning",
        metric_name="expect_table_row_count_to_be_between.result.observed_value",
        metric_kwargs_id=None
    )
    metric_value = 512
    param_store.set(metric_identifier, metric_value)

    metric_identifier = ValidationMetricIdentifier(
        run_id=run_id,
        expectation_suite_identifier="asset2.warning",
        metric_name="expect_column_values_to_match_regex.result.unexpected_percent",
        metric_kwargs_id="column=mycol"
    )
    metric_value = 12.3456789
    param_store.set(metric_identifier, metric_value)

    params = param_store.get_bind_params(run_id)
    assert params == {
        'urn:great_expectations:validations:asset.warning:'
        'expect_column_values_to_match_regex.result.unexpected_percent:column=mycol': 12.3456789,
        'urn:great_expectations:validations:asset.warning:'
        'expect_table_row_count_to_be_between.result.observed_value': 512,
        'urn:great_expectations:validations:asset2.warning:'
        'expect_column_values_to_match_regex.result.unexpected_percent:column=mycol': 12.3456789,
    }
