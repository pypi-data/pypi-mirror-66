from catcher.steps.external_step import ExternalStep
from catcher.steps.step import update_variables

from catcher_modules.database import SqlAlchemyDb


class MSSql(ExternalStep, SqlAlchemyDb):
    """
    :Input:

    :conf:  mssql configuration. Can be a single line string or object. Dialect is not mandatory. **Required**.

    - dbname: name of the database to connect to
    - user: database user
    - host: database host
    - password: user's password
    - port: database port
    :query: query to run. **Required**

    :Examples:

    Select all from test, use object configuration
    ::
        mssql:
          request:
              conf:
                  dbname: test
                  user: user
                  password: password
                  host: localhost
                  port: 1433
              query: 'select count(*) as count from test'
          register: {documents: '{{ OUTPUT }}'}

    **Note** that we alias count. For some reason sqlalchemy for mssql will return `count(*)` as a column name
    instead of `count`.


    Insert into test, using string configuration
    ::
        mssql:
          request:
              conf: 'user:password@localhost:5432/test'
              query: 'insert into test(id, num) values(3, 3);'

    Insert into test, using string configuration with dialect
    ::
        mssql:
          request:
              conf: 'mssql+pymssql://user:password@localhost:5432/test'
              query: 'insert into test(id, num) values(3, 3);'

      """

    @property
    def driver(self) -> str:
        return "mssql+pymssql"

    @update_variables
    def action(self, includes: dict, variables: dict) -> any:
        body = self.simple_input(variables)
        return variables, self.execute(body)
