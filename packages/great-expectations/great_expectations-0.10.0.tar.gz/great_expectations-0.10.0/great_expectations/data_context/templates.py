# -*- coding: utf-8 -*-
import os
import uuid

PROJECT_HELP_COMMENT = """
# Welcome to Great Expectations! Always know what to expect from your data.
# 
# Here you can define datasources, batch kwargs generators, integrations and
# more. This file is intended to be committed to your repo. For help with
# configuration please:
#   - Read our docs: https://docs.greatexpectations.io/en/latest/reference/data_context_reference.html#configuration
#   - Join our slack channel: http://greatexpectations.io/slack

config_version: 1

# Datasources tell Great Expectations where your data lives and how to get it.
# You can use the CLI command `great_expectations datasource new` to help you
# add a new datasource. Read more at https://docs.greatexpectations.io/en/latest/features/datasource.html
datasources: {}
"""

CONFIG_VARIABLES_INTRO = """# This config file supports variable substitution which enables: 1) keeping
# secrets out of source control & 2) environment-based configuration changes
# such as staging vs prod.
#
# When GE encounters substitution syntax (like `my_key: ${my_value}` or 
# `my_key: $my_value`) in the config file, it will attempt to replace the value
# of `my_key` with the value from an environment variable `my_value` or a
# corresponding key read from the file specified using
# `config_variables_file_path`. Environment variables take precedence.
#
# If the substitution value comes from the config variables file, it can be a
# simple (non-nested) value or a nested value such as a dictionary. If it comes
# from an environment variable, it must be a simple value. Read more at:
# https://docs.greatexpectations.io/en/latest/reference/data_context_reference.html#managing-environment-and-secrets

"""

CONFIG_VARIABLES_TEMPLATE = CONFIG_VARIABLES_INTRO + "instance_id: " + str(uuid.uuid4()) + os.linesep

PROJECT_OPTIONAL_CONFIG_COMMENT = CONFIG_VARIABLES_INTRO + """
config_variables_file_path: uncommitted/config_variables.yml

# The plugins_directory will be added to your python path for custom modules
# used to override and extend Great Expectations.
plugins_directory: plugins/

# Validation Operators are customizable workflows that bundle the validation of
# one or more expectation suites and subsequent actions. The example below
# stores validations and send a slack notification. To read more about
# customizing and extending these, read: https://docs.greatexpectations.io/en/latest/features/validation_operators_and_actions.html
validation_operators:
  action_list_operator:
    # To learn how to configure sending Slack notifications during evaluation
    # (and other customizations), read: https://docs.greatexpectations.io/en/latest/reference/validation_operators/action_list_validation_operator.html
    class_name: ActionListValidationOperator
    action_list:
      - name: store_validation_result
        action:
          class_name: StoreValidationResultAction
      - name: store_evaluation_params
        action:
          class_name: StoreEvaluationParametersAction
      - name: update_data_docs
        action:
          class_name: UpdateDataDocsAction
      # - name: send_slack_notification_on_validation_result
      #   action:
      #     class_name: SlackNotificationAction
      #     # put the actual webhook URL in the uncommitted/config_variables.yml file
      #     slack_webhook: ${validation_notification_slack_webhook}
      #     notify_on: all # possible values: "all", "failure", "success"
      #     renderer:
      #       module_name: great_expectations.render.renderer.slack_renderer
      #       class_name: SlackRenderer
    
stores:
# Stores are configurable places to store things like Expectations, Validations
# Data Docs, and more. These are for advanced users only - most users can simply
# leave this section alone.
# 
# Three stores are required: expectations, validations, and
# evaluation_parameters, and must exist with a valid store entry. Additional
# stores can be configured for uses such as data_docs, validation_operators, etc.
  expectations_store:
    class_name: ExpectationsStore
    store_backend:
      class_name: TupleFilesystemStoreBackend
      base_directory: expectations/

  validations_store:
    class_name: ValidationsStore
    store_backend:
      class_name: TupleFilesystemStoreBackend
      base_directory: uncommitted/validations/

  evaluation_parameter_store:
    # Evaluation Parameters enable dynamic expectations. Read more here:
    # https://docs.greatexpectations.io/en/latest/reference/evaluation_parameters.html
    class_name: EvaluationParameterStore

expectations_store_name: expectations_store
validations_store_name: validations_store
evaluation_parameter_store_name: evaluation_parameter_store

data_docs_sites:
  # Data Docs make it simple to visualize data quality in your project. These
  # include Expectations, Validations & Profiles. The are built for all
  # Datasources from JSON artifacts in the local repo including validations &
  # profiles from the uncommitted directory. Read more at https://docs.greatexpectations.io/en/latest/features/data_docs.html
  local_site:
    class_name: SiteBuilder
    # set to false to hide how-to buttons in Data Docs
    show_how_to_buttons: true
    store_backend:
        class_name: TupleFilesystemStoreBackend
        base_directory: uncommitted/data_docs/local_site/
    site_index_builder:
        class_name: DefaultSiteIndexBuilder
"""

ANONYMIZED_USAGE_STATISTICS_ENABLED = """
anonymous_usage_statistics:
  enabled: True
"""

ANONYMIZED_USAGE_STATISTICS_DISABLED = """
anonymous_usage_statistics:
  enabled: False
"""

PROJECT_TEMPLATE_USAGE_STATISTICS_ENABLED = PROJECT_HELP_COMMENT + PROJECT_OPTIONAL_CONFIG_COMMENT + ANONYMIZED_USAGE_STATISTICS_ENABLED
PROJECT_TEMPLATE_USAGE_STATISTICS_DISABLED = PROJECT_HELP_COMMENT + PROJECT_OPTIONAL_CONFIG_COMMENT + ANONYMIZED_USAGE_STATISTICS_DISABLED
