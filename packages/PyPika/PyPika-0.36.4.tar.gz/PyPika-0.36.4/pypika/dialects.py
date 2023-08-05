from copy import copy

from pypika.enums import Dialects
from pypika.queries import (
    CreateQueryBuilder,
    Query,
    QueryBuilder,
    Table,
)
from pypika.terms import (
    ArithmeticExpression,
    Field,
    Term,
    Function,
    Star,
    ValueWrapper,
    EmptyCriterion
)
from pypika.utils import (
    QueryException,
    builder,
)


class SnowFlakeQueryBuilder(QueryBuilder):
    QUOTE_CHAR = None
    ALIAS_QUOTE_CHAR = '"'

    def __init__(self, **kwargs):
        super(SnowFlakeQueryBuilder, self).__init__(
            dialect=Dialects.SNOWFLAKE, **kwargs
        )


class SnowflakeQuery(Query):
    """
    Defines a query class for use with Snowflake.
    """

    @classmethod
    def _builder(cls, **kwargs):
        return SnowFlakeQueryBuilder(**kwargs)


class MySQLQueryBuilder(QueryBuilder):
    QUOTE_CHAR = "`"

    def __init__(self, **kwargs):
        super(MySQLQueryBuilder, self).__init__(
            dialect=Dialects.MYSQL, wrap_union_queries=False, **kwargs
        )
        self._duplicate_updates = []
        self._modifiers = []

    def __copy__(self):
        newone = super(MySQLQueryBuilder, self).__copy__()
        newone._duplicate_updates = copy(self._duplicate_updates)
        return newone

    @builder
    def on_duplicate_key_update(self, field, value):
        field = Field(field) if not isinstance(field, Field) else field
        self._duplicate_updates.append((field, ValueWrapper(value)))

    def get_sql(self, **kwargs):
        self._set_kwargs_defaults(kwargs)
        querystring = super(MySQLQueryBuilder, self).get_sql(**kwargs)
        if querystring and self._duplicate_updates:
            querystring += self._on_duplicate_key_update_sql(**kwargs)
        return querystring

    def _on_duplicate_key_update_sql(self, **kwargs):
        return " ON DUPLICATE KEY UPDATE {updates}".format(
            updates=",".join(
                "{field}={value}".format(
                    field=field.get_sql(**kwargs), value=value.get_sql(**kwargs)
                )
                for field, value in self._duplicate_updates
            )
        )

    @builder
    def modifier(self, value):
        """
        Adds a modifier such as SQL_CALC_FOUND_ROWS to the query.
        https://dev.mysql.com/doc/refman/5.7/en/select.html

        :param value: The modifier value e.g. SQL_CALC_FOUND_ROWS
        """
        self._modifiers.append(value)

    def _select_sql(self, **kwargs):
        """
        Overridden function to generate the SELECT part of the SQL statement,
        with the addition of the a modifier if present.
        """
        return "SELECT {distinct}{modifier}{select}".format(
            distinct="DISTINCT " if self._distinct else "",
            modifier="{} ".format(" ".join(self._modifiers)) if self._modifiers else "",
            select=",".join(
                term.get_sql(with_alias=True, subquery=True, **kwargs)
                for term in self._selects
            ),
        )


class MySQLLoadQueryBuilder:
    def __init__(self):
        self._load_file = None
        self._into_table = None

    @builder
    def load(self, fp):
        self._load_file = fp

    @builder
    def into(self, table):
        self._into_table = table if isinstance(table, Table) else Table(table)

    def get_sql(self, *args, **kwargs):
        querystring = ""
        if self._load_file and self._into_table:
            querystring += self._load_file_sql(**kwargs)
            querystring += self._into_table_sql(**kwargs)
            querystring += self._options_sql(**kwargs)

        return querystring

    def _load_file_sql(self, **kwargs):
        return "LOAD DATA LOCAL INFILE '{}'".format(self._load_file)

    def _into_table_sql(self, **kwargs):
        return " INTO TABLE `{}`".format(self._into_table.get_sql(**kwargs))

    def _options_sql(self, **kwargs):
        return " FIELDS TERMINATED BY ','"

    def __str__(self):
        return self.get_sql()


class MySQLQuery(Query):
    """
    Defines a query class for use with MySQL.
    """

    @classmethod
    def _builder(cls, **kwargs):
        return MySQLQueryBuilder(**kwargs)

    @classmethod
    def load(cls, fp):
        return MySQLLoadQueryBuilder().load(fp)


class VerticaQueryBuilder(QueryBuilder):
    def __init__(self, **kwargs):
        super(VerticaQueryBuilder, self).__init__(dialect=Dialects.VERTICA, **kwargs)
        self._hint = None

    @builder
    def hint(self, label):
        self._hint = label

    def get_sql(self, *args, **kwargs):
        sql = super(VerticaQueryBuilder, self).get_sql(*args, **kwargs)

        if self._hint is not None:
            sql = "".join(
                [sql[:7], "/*+label({hint})*/".format(hint=self._hint), sql[6:]]
            )

        return sql


class VerticaCreateQueryBuilder(CreateQueryBuilder):
    def __init__(self):
        super(VerticaCreateQueryBuilder, self).__init__(dialect=Dialects.VERTICA)
        self._local = False
        self._preserve_rows = False

    @builder
    def local(self):
        if not self._temporary:
            raise AttributeError("'Query' object has no attribute temporary")

        self._local = True

    @builder
    def preserve_rows(self):
        if not self._temporary:
            raise AttributeError("'Query' object has no attribute temporary")

        self._preserve_rows = True

    def _create_table_sql(self, **kwargs):
        return "CREATE {local}{temporary}TABLE {table}".format(
            local="LOCAL " if self._local else "",
            temporary="TEMPORARY " if self._temporary else "",
            table=self._create_table.get_sql(**kwargs),
        )

    def _columns_sql(self, **kwargs):
        return " ({columns}){preserve_rows}".format(
            columns=",".join(column.get_sql(**kwargs) for column in self._columns),
            preserve_rows=self._preserve_rows_sql(),
        )

    def _as_select_sql(self, **kwargs):
        return "{preserve_rows} AS ({query})".format(
            preserve_rows=self._preserve_rows_sql(),
            query=self._as_select.get_sql(**kwargs),
        )

    def _preserve_rows_sql(self):
        return " ON COMMIT PRESERVE ROWS" if self._preserve_rows else ""


class VerticaCopyQueryBuilder:
    def __init__(self):
        self._copy_table = None
        self._from_file = None

    @builder
    def from_file(self, fp):
        self._from_file = fp

    @builder
    def copy_(self, table):
        self._copy_table = table if isinstance(table, Table) else Table(table)

    def get_sql(self, *args, **kwargs):
        querystring = ""
        if self._copy_table and self._from_file:
            querystring += self._copy_table_sql(**kwargs)
            querystring += self._from_file_sql(**kwargs)
            querystring += self._options_sql(**kwargs)

        return querystring

    def _copy_table_sql(self, **kwargs):
        return 'COPY "{}"'.format(self._copy_table.get_sql(**kwargs))

    def _from_file_sql(self, **kwargs):
        return " FROM LOCAL '{}'".format(self._from_file)

    def _options_sql(self, **kwargs):
        return " PARSER fcsvparser(header=false)"

    def __str__(self):
        return self.get_sql()


class VerticaQuery(Query):
    """
    Defines a query class for use with Vertica.
    """

    @classmethod
    def _builder(cls, **kwargs):
        return VerticaQueryBuilder(**kwargs)

    @classmethod
    def from_file(cls, fp):
        return VerticaCopyQueryBuilder().from_file(fp)

    @classmethod
    def create_table(cls, table):
        return VerticaCreateQueryBuilder().create_table(table)


class OracleQueryBuilder(QueryBuilder):
    def __init__(self, **kwargs):
        super(OracleQueryBuilder, self).__init__(dialect=Dialects.ORACLE, **kwargs)

    def get_sql(self, *args, **kwargs):
        return super(OracleQueryBuilder, self).get_sql(
            *args, groupby_alias=False, **kwargs
        )


class OracleQuery(Query):
    """
    Defines a query class for use with Oracle.
    """

    @classmethod
    def _builder(cls, **kwargs):
        return OracleQueryBuilder(**kwargs)


class PostgreQueryBuilder(QueryBuilder):
    def __init__(self, **kwargs):
        super(PostgreQueryBuilder, self).__init__(dialect=Dialects.POSTGRESQL, **kwargs)
        self._returns = []
        self._return_star = False

        self._on_conflict = False
        self._on_conflict_fields = []
        self._on_conflict_do_nothing = False
        self._on_conflict_do_updates = []
        self._on_conflict_wheres = None
        self._on_conflict_do_update_wheres = None

        self._distinct_on = []

    def __copy__(self):
        newone = super(PostgreQueryBuilder, self).__copy__()
        newone._returns = copy(self._returns)
        newone._on_conflict_do_updates = copy(self._on_conflict_do_updates)
        return newone

    @builder
    def distinct_on(self, *fields):
        for field in fields:
            if isinstance(field, str):
                self._distinct_on.append(Field(field))
            elif isinstance(field, Term):
                self._distinct_on.append(field)

    @builder
    def on_conflict(self, *target_fields):
        if not self._insert_table:
            raise QueryException("On conflict only applies to insert query")

        self._on_conflict = True

        for target_field in target_fields:
            if isinstance(target_field, str):
                self._on_conflict_fields.append(self._conflict_field_str(target_field))
            elif isinstance(target_field, Term):
                self._on_conflict_fields.append(target_field)

    @builder
    def do_nothing(self):
        if len(self._on_conflict_do_updates) > 0:
            raise QueryException("Can not have two conflict handlers")
        self._on_conflict_do_nothing = True

    @builder
    def do_update(self, update_field, update_value):
        if self._on_conflict_do_nothing:
            raise QueryException("Can not have two conflict handlers")

        if isinstance(update_field, str):
            field = self._conflict_field_str(update_field)
        elif isinstance(update_field, Field):
            field = update_field
        else:
            raise QueryException("Unsupported update_field")

        self._on_conflict_do_updates.append((field, ValueWrapper(update_value)))

    @builder
    def where(self, criterion):
        if not self._on_conflict:
            return super().where(criterion)

        if isinstance(criterion, EmptyCriterion):
            return

        if self._on_conflict_do_nothing:
            raise QueryException('DO NOTHING doest not support WHERE')

        if self._on_conflict_fields and self._on_conflict_do_updates:
            if self._on_conflict_do_update_wheres:
                self._on_conflict_do_update_wheres &= criterion
            else:
                self._on_conflict_do_update_wheres = criterion
        elif self._on_conflict_fields:
            if self._on_conflict_wheres:
                self._on_conflict_wheres &= criterion
            else:
                self._on_conflict_wheres = criterion
        else:
            raise QueryException('Can not have fieldless ON CONFLICT WHERE')

    def _distinct_sql(self, **kwargs):
        if self._distinct_on:
            return "DISTINCT ON({distinct_on}) ".format(
                distinct_on=",".join(
                    term.get_sql(with_alias=True, **kwargs) for term in self._distinct_on
                )
            )
        return super()._distinct_sql(**kwargs)

    def _conflict_field_str(self, term):
        if self._insert_table:
            return Field(term, table=self._insert_table)

    def _on_conflict_sql(self, **kwargs):
        if not self._on_conflict_do_nothing and len(self._on_conflict_do_updates) == 0:
            if not self._on_conflict_fields:
                return ""
            raise QueryException("No handler defined for on conflict")

        if self._on_conflict_do_updates and not self._on_conflict_fields:
            raise QueryException("Can not have fieldless on conflict do update")

        conflict_query = " ON CONFLICT"
        if self._on_conflict_fields:
            fields = [f.get_sql(with_alias=True, **kwargs)
                      for f in self._on_conflict_fields]
            conflict_query += " (" + ', '.join(fields) + ")"

        if self._on_conflict_wheres:
            conflict_query += " WHERE {where}".format(
                where=self._on_conflict_wheres.get_sql(subquery=True, **kwargs)
            )

        return conflict_query

    def _on_conflict_action_sql(self, **kwargs):
        if self._on_conflict_do_nothing:
            return " DO NOTHING"
        elif len(self._on_conflict_do_updates) > 0:
            action_sql = " DO UPDATE SET {updates}".format(
                updates=",".join(
                    "{field}={value}".format(
                        field=field.get_sql(**kwargs),
                        value=value.get_sql(with_namespace=True, **kwargs),
                    )
                    for field, value in self._on_conflict_do_updates
                )
            )

            if self._on_conflict_do_update_wheres:
                action_sql += " WHERE {where}".format(
                    where=self._on_conflict_do_update_wheres.get_sql(subquery=True, with_namespace=True, **kwargs)
                )
            return action_sql

        return ''

    @builder
    def returning(self, *terms):
        for term in terms:
            if isinstance(term, Field):
                self._return_field(term)
            elif isinstance(term, str):
                self._return_field_str(term)
            elif isinstance(term, ArithmeticExpression):
                self._return_other(term)
            elif isinstance(term, Function):
                raise QueryException("Aggregate functions are not allowed in returning")
            else:
                self._return_other(self.wrap_constant(term, self._wrapper_cls))

    def _validate_returning_term(self, term):
        for field in term.fields_():
            if not any([self._insert_table, self._update_table, self._delete_from]):
                raise QueryException("Returning can't be used in this query")
            if (
                field.table not in {self._insert_table, self._update_table}
                and term not in self._from
            ):
                raise QueryException("You can't return from other tables")

    def _set_returns_for_star(self):
        self._returns = [
            returning for returning in self._returns if not hasattr(returning, "table")
        ]
        self._return_star = True

    def _return_field(self, term):
        if self._return_star:
            # Do not add select terms after a star is selected
            return

        self._validate_returning_term(term)

        if isinstance(term, Star):
            self._set_returns_for_star()

        self._returns.append(term)

    def _return_field_str(self, term):
        if term == "*":
            self._set_returns_for_star()
            self._returns.append(Star())
            return

        if self._insert_table:
            self._return_field(Field(term, table=self._insert_table))
        elif self._update_table:
            self._return_field(Field(term, table=self._update_table))
        elif self._delete_from:
            self._return_field(Field(term, table=self._from[0]))
        else:
            raise QueryException("Returning can't be used in this query")

    def _return_other(self, function):
        self._validate_returning_term(function)
        self._returns.append(function)

    def _returning_sql(self, **kwargs):
        return " RETURNING {returning}".format(
            returning=",".join(
                term.get_sql(with_alias=True, **kwargs) for term in self._returns
            ),
        )

    def get_sql(self, with_alias=False, subquery=False, **kwargs):
        self._set_kwargs_defaults(kwargs)

        querystring = super(PostgreQueryBuilder, self).get_sql(
            with_alias, subquery, **kwargs
        )
        with_namespace = False
        if self._update_table and self.from_:
            with_namespace = True

        querystring += self._on_conflict_sql(**kwargs)
        querystring += self._on_conflict_action_sql(**kwargs)

        if self._returns:
            querystring += self._returning_sql(with_namespace=with_namespace, **kwargs)
        return querystring


class PostgreSQLQuery(Query):
    """
    Defines a query class for use with PostgreSQL.
    """

    @classmethod
    def _builder(cls, **kwargs):
        return PostgreQueryBuilder(**kwargs)


class RedshiftQuery(Query):
    """
    Defines a query class for use with Amazon Redshift.
    """

    @classmethod
    def _builder(cls, **kwargs):
        return QueryBuilder(dialect=Dialects.REDSHIFT, **kwargs)


class MSSQLQueryBuilder(QueryBuilder):
    def __init__(self, **kwargs):
        super(MSSQLQueryBuilder, self).__init__(dialect=Dialects.MSSQL, **kwargs)
        self._top = None

    @builder
    def top(self, value):
        """
        Implements support for simple TOP clauses.

        Does not include support for PERCENT or WITH TIES.

        https://docs.microsoft.com/en-us/sql/t-sql/queries/top-transact-sql?view=sql-server-2017
        """
        try:
            self._top = int(value)
        except ValueError:
            raise QueryException("TOP value must be an integer")

    def get_sql(self, *args, **kwargs):
        return super(MSSQLQueryBuilder, self).get_sql(
            *args, groupby_alias=False, **kwargs
        )

    def _top_sql(self):
        if self._top:
            return "TOP ({}) ".format(self._top)
        else:
            return ""

    def _select_sql(self, **kwargs):
        return "SELECT {distinct}{top}{select}".format(
            top=self._top_sql(),
            distinct="DISTINCT " if self._distinct else "",
            select=",".join(
                term.get_sql(with_alias=True, subquery=True, **kwargs)
                for term in self._selects
            ),
        )


class MSSQLQuery(Query):
    """
    Defines a query class for use with Microsoft SQL Server.
    """

    @classmethod
    def _builder(cls, **kwargs):
        return MSSQLQueryBuilder(**kwargs)


class ClickHouseQuery(Query):
    """
    Defines a query class for use with Yandex ClickHouse.
    """

    @classmethod
    def _builder(cls, **kwargs):
        return QueryBuilder(
            dialect=Dialects.CLICKHOUSE, wrap_union_queries=False, **kwargs
        )


class SQLLiteValueWrapper(ValueWrapper):
    def get_value_sql(self, *args, **kwargs):
        if isinstance(self.value, bool):
            return "1" if self.value else "0"
        return super().get_value_sql(*args, **kwargs)


class SQLLiteQuery(Query):
    """
    Defines a query class for use with Microsoft SQL Server.
    """

    @classmethod
    def _builder(cls, **kwargs):
        return QueryBuilder(
            dialect=Dialects.SQLLITE, wrapper_cls=SQLLiteValueWrapper, **kwargs
        )
