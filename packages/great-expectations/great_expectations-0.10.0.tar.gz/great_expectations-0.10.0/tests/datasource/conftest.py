import pytest

from great_expectations.datasource import PandasDatasource, SqlAlchemyDatasource, SparkDFDatasource


@pytest.fixture(scope="module")
def basic_pandas_datasource():
    return PandasDatasource("basic_pandas_datasource")


@pytest.fixture
def basic_sqlalchemy_datasource(sqlitedb_engine):
    return SqlAlchemyDatasource("basic_sqlalchemy_datasource", engine=sqlitedb_engine)


@pytest.fixture
def postgresql_sqlalchemy_datasource(postgresql_engine):
    return SqlAlchemyDatasource("postgresql_sqlalchemy_datasource", engine=postgresql_engine)


@pytest.fixture(scope="module")
def basic_sparkdf_datasource():
    return SparkDFDatasource("basic_sparkdf_datasource")
