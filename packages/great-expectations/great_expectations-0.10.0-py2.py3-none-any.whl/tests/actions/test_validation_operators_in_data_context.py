import pytest
import json

from great_expectations.data_context import (
    BaseDataContext,
)
from great_expectations.core import (
    expectationSuiteSchema,
)

from great_expectations.data_context.util import (
    file_relative_path,
)


@pytest.fixture()
def parameterized_expectation_suite():
    fixture_path = file_relative_path(
        __file__,
        "../test_fixtures/expectation_suites/parameterized_expression_expectation_suite_fixture.json",
    )
    with open(fixture_path, "r",) as suite:
        return expectationSuiteSchema.load(json.load(suite))


@pytest.fixture
def validation_operators_data_context(basic_data_context_config_for_validation_operator, filesystem_csv_4):
    data_context = BaseDataContext(
        basic_data_context_config_for_validation_operator
    )

    data_context.add_datasource("my_datasource",
                                class_name="PandasDatasource",
                                batch_kwargs_generators={
                                    "subdir_reader": {
                                        "class_name": "SubdirReaderBatchKwargsGenerator",
                                        "base_directory": str(filesystem_csv_4)
                                    }
                                })
    data_context.create_expectation_suite("f1.foo")

    df = data_context.get_batch(batch_kwargs=data_context.build_batch_kwargs("my_datasource",
                                                                             "subdir_reader", "f1"),
                                expectation_suite_name="f1.foo")
    df.expect_column_values_to_be_between(column="x", min_value=1, max_value=9)
    failure_expectations = df.get_expectation_suite(discard_failed_expectations=False)

    df.expect_column_values_to_not_be_null(column="y")
    warning_expectations = df.get_expectation_suite(discard_failed_expectations=False)

    data_context.save_expectation_suite(failure_expectations, expectation_suite_name="f1.failure")
    data_context.save_expectation_suite(warning_expectations, expectation_suite_name="f1.warning")

    return data_context


def test_validation_operator_evaluation_parameters(validation_operators_data_context, parameterized_expectation_suite):
    validation_operators_data_context.save_expectation_suite(parameterized_expectation_suite, "param_suite")
    res = validation_operators_data_context.run_validation_operator(
        "store_val_res_and_extract_eval_params",
        assets_to_validate=[
            (
                validation_operators_data_context.build_batch_kwargs("my_datasource", "subdir_reader", "f1"),
                "param_suite"
            )
        ],
        evaluation_parameters={
            "urn:great_expectations:validations:source_patient_data.default:expect_table_row_count_to_equal.result"
            ".observed_value": 3
        }
    )
    assert res["success"] is True

    validation_operators_data_context.save_expectation_suite(parameterized_expectation_suite, "param_suite.failure")
    res = validation_operators_data_context.run_validation_operator(
        "errors_and_warnings_validation_operator",
        assets_to_validate=[
            (
                validation_operators_data_context.build_batch_kwargs("my_datasource", "subdir_reader", "f1"),
                "param_suite.failure"
            )
        ],
        evaluation_parameters={
            "urn:great_expectations:validations:source_patient_data.default:expect_table_row_count_to_equal.result"
            ".observed_value": 10
        },
        base_expectation_suite_name="param_suite"
    )
    assert res["success"] is False


def test_action_list_operator(validation_operators_data_context):
    data_context = validation_operators_data_context
    validator_batch_kwargs = data_context.build_batch_kwargs("my_datasource", "subdir_reader", "f1")

    batch = data_context.get_batch(expectation_suite_name="f1.failure",
                                   batch_kwargs=validator_batch_kwargs
                                   )

    assert data_context.stores["validation_result_store"].list_keys() == []
    # We want to demonstrate running the validation operator with both a pre-built batch (DataAsset) and with
    # a tuple of parameters for get_batch
    operator_result = data_context.run_validation_operator(
        assets_to_validate=[batch, (validator_batch_kwargs, "f1.warning")],
        run_id="test-100",
        evaluation_parameters={},
        validation_operator_name="store_val_res_and_extract_eval_params",
    )
    # results = data_context.run_validation_operator(my_ge_df)

    validation_result_store_keys = data_context.stores["validation_result_store"].list_keys()
    print(validation_result_store_keys)
    assert len(validation_result_store_keys) == 2
    assert operator_result["success"]
    assert len(operator_result['details'].keys()) == 2

    first_validation_result = data_context.stores["validation_result_store"].get(validation_result_store_keys[0])
    assert data_context.stores["validation_result_store"].get(validation_result_store_keys[0]).success is True


def test_warning_and_failure_validation_operator(validation_operators_data_context):
    data_context = validation_operators_data_context
    validator_batch_kwargs = data_context.build_batch_kwargs("my_datasource", "subdir_reader", "f1")

    batch = data_context.get_batch(expectation_suite_name="f1.warning",
                                   batch_kwargs=validator_batch_kwargs)

    # NOTE: 20200130 - JPC - currently the warning and failure validation operator ignores the batch-provided suite and
    # fetches its own

    assert data_context.validations_store.list_keys() == []

    # We want to demonstrate running the validation operator with both a pre-built batch (DataAsset) and with
    # a tuple of parameters for get_batch
    results = data_context.run_validation_operator(
        assets_to_validate=[batch],
        run_id="test-100",
        validation_operator_name="errors_and_warnings_validation_operator",
        base_expectation_suite_name="f1"
    )

    validations_keys = data_context.validations_store.list_keys()
    assert len(validations_keys) == 2  # we should have run two suites even though there was only one batch
    suite_names = [key.expectation_suite_identifier.expectation_suite_name for key in validations_keys]
    assert "f1.warning" in suite_names
    assert "f1.failure" in suite_names
