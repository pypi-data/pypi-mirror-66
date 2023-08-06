"""Client implementation using SQL database

Supported databases: sqlite, postgresql
"""

import copy
import functools
import inspect
import re
import typing
import uuid

import sqlalchemy as sqla

from .. import deid
from .. import errors
from .. import models as M
from .. import schemas as T
from .. import utils
from ..config import IngestConfig, StrategyConfig
from .abstract import Client

S = typing.TypeVar("S")  # pylint: disable=C0103
F = typing.TypeVar("F", bound=typing.Callable[..., typing.Any])  # pylint: disable=C0103


class DBClient(Client):  # pylint: disable=R0904
    """Ingest DB client implementing crud interface"""

    def __init__(self, url: str):
        super().__init__(url)
        self.engine, self.sessionmaker = utils.init_sqla(url)

        if self.engine.name == "sqlite":
            M.Base.metadata.create_all(self.engine)

    def __getattr__(self, name):
        method_name = None
        for prefix in ("get_all", "get", "update", "find_one", "count_all", "batch_writer"):
            if name.startswith(prefix):
                method_name = prefix
                break

        if method_name in ("get_all", "get", "update", "find_one", "count_all"):
            model_name = name.replace(method_name, "").strip("_")
            model_name = "".join([part.capitalize() for part in model_name.split("_")])
            func = getattr(self, method_name)
            @functools.wraps(func)
            def _wrapper(*args, **kwargs):
                return func(model_name, *args, **kwargs)
            return _wrapper
        if method_name == "batch_writer":
            type_, model_name = name.replace(method_name, "").strip("_").split("_", maxsplit=1)
            model_name = "".join([part.capitalize() for part in model_name.split("_")])
            func = getattr(self, method_name)
            @functools.wraps(func)
            def _wrapper(*args, **kwargs):
                return func(type_, model_name, *args, **kwargs)
            return _wrapper
        raise AttributeError(f"Unknown attribute: {name}")

    def check_connection(self):
        """Check whether or not the connection works"""
        try:
            # Test query
            self.engine.execute(sqla.text('SELECT 1'))
            return True
        except Exception:  # pylint: disable=broad-except
            return False

    def call_db(self, func: typing.Callable[..., S], *args, **kwargs) -> S:
        """Run the specified function in a transaction"""
        assert isinstance(func, FunctionTransactionInfo)
        session = self.sessionmaker()
        if session.bind.name == "sqlite":
            session.execute(f"BEGIN {func.transaction_type}")
        try:
            result = func(session, *args, **kwargs)
            session.commit()
        except:
            session.rollback()
            raise
        else:
            return result
        finally:
            session.close()

    # Non-ingest-bound methods

    def create_ingest(
        self,
        config: IngestConfig,
        strategy_config: StrategyConfig,
        fw_auth: typing.Optional[T.FWAuth] = None
    ) -> T.IngestOutAPI:
        if not fw_auth:
            fw_auth = utils.get_fw_auth(utils.get_api_key())
        ingest = M.Ingest(
            api_key=fw_auth.api_key,
            fw_host=fw_auth.host,
            fw_user=fw_auth.user,
            config=config.dict(exclude_none=True),
            strategy_config=strategy_config.dict(exclude_none=True),
            # TODO: user provided label from config
        )
        ingest_out = self.call_db(add, ingest)
        self.bind(ingest_out.id)  # type: ignore
        return T.IngestOutAPI(**ingest_out.dict())

    def list_ingests(self) -> typing.Iterable[T.IngestOutAPI]:
        query = sqla.orm.Query(M.Ingest)
        return self._iter_query(query, [M.Ingest.created], T.IngestOutAPI)

    def next_task(self, worker: str) -> typing.Optional[T.TaskOut]:
        """Get next pending task, assign to given worker and set status running"""
        return self.call_db(next_task, worker)

    # Ingest-bound methods

    @property
    def ingest(self) -> T.IngestOutAPI:
        """Get ingest operation the client bind to"""
        ingest = self.call_db(get, M.Ingest, self.ingest_id)
        return T.IngestOutAPI(**ingest.dict())

    def load_subject_csv(self, subject_csv: typing.BinaryIO) -> None:
        """Load subject CSV file"""
        self.call_db(load_subject_csv, self.ingest_id, subject_csv)

    def start(self) -> T.IngestOutAPI:
        """Start ingest scanning"""
        ingest = self.call_db(start, self.ingest_id)
        return T.IngestOutAPI(**ingest.dict())

    def review(self, changes=None) -> T.IngestOutAPI:
        """Review (accept) ingest, add any changes and start importing"""
        ingest = self.call_db(review, self.ingest_id, changes)
        return T.IngestOutAPI(**ingest.dict())

    def abort(self) -> T.IngestOutAPI:
        """Abort ingest operation"""
        ingest = self.call_db(abort, self.ingest_id)
        return T.IngestOutAPI(**ingest.dict())

    @property
    def progress(self) -> T.Progress:
        """Get ingest scan task and item/file/byte counts by status"""
        return self.call_db(get_progress, self.ingest_id)

    @property
    def summary(self) -> T.Summary:
        """Get ingest hierarchy node and file count by level and type"""
        return self.call_db(get_summary, self.ingest_id)

    @property
    def report(self) -> T.Report:
        """Get ingest status, elapsed time per status and list of failed tasks"""
        return self.call_db(get_report, self.ingest_id)

    @property
    def tree(self) -> typing.Iterable[T.ContainerOut]:
        """Yield hierarchy nodes (containers)"""
        query = (
            sqla.orm.Query([
                M.Container.id,
                M.Container.level,
                M.Container.path,
                M.Container.parent_id,
                M.Container.src_context,
                M.Container.dst_context,
                M.Container.ingest_id,
                sqla.sql.func.count(M.Item.id).label("files_cnt"),
                sqla.sql.func.sum(M.Item.bytes_sum).label("bytes_sum"),
            ])
            .outerjoin(M.Container.items)
            .filter(M.Container.ingest_id == self.ingest_id)
            .group_by(M.Container.id)
        )
        return self._iter_query(query, [M.Container.path], T.ContainerOut)

    @property
    def audit_logs(self) -> typing.Iterable[str]:
        """Yield audit log CSV lines"""
        query = (
            sqla.orm.Query([
                M.Item.id,
                M.Item.dir,
                M.Item.filename,
                M.Item.existing,
                M.Item.skipped,
                M.Container.dst_path,
                M.Task.status,
                M.Task.error,
            ])
            .outerjoin(M.Item.container, M.Item.task)
            .filter(M.Item.ingest_id == self.ingest_id)
        )

        fields = ["src_path", "dst_path", "status", "existing", "error"]
        first = True
        for item in self._iter_query(query, [M.Item.dir], T.AuditLogOut):
            if first:
                first = False
                header = ",".join(fields)
                yield f"{header}\n"

            # TODO normalize src path, make sure win32/local works
            values = dict(
                src_path=f"{self.ingest.config.src_fs}{item.dir}/{item.filename}",
                dst_path=f"{item.dst_path}/{item.filename}",
                status="skipped" if item.skipped else item.status.name,
                existing=item.existing,
                error=item.error,
            )
            row = ",".join(_csv_field_str(values[field]) for field in fields)
            yield f"{row}\n"

    @property
    def deid_logs(self) -> typing.Iterable[str]:
        """Yield de-id log CSV lines"""
        ingest = self.ingest
        assert ingest.config.de_identify

        # add fields from all deid file profiles
        fields = ["src_path", "type"]
        profile_name = ingest.config.deid_profile
        profiles = ingest.config.deid_profiles
        deid_profile = deid.load_deid_profile(profile_name, profiles)
        for file_profile in deid_profile.file_profiles:
            fields.extend(file_profile.get_log_fields())

        query = (
            sqla.orm.Query(M.DeidLog)
            .filter(M.DeidLog.ingest_id == self.ingest_id)
        )
        first = True
        for deid_log in self._iter_query(query, [M.DeidLog.created], T.DeidLogOut):
            if first:
                first = False
                header = ",".join(fields)
                yield f"{header}\n"

            before = {"src_path": deid_log.src_path, "type": "before", **deid_log.tags_before}
            before_row = ",".join(_csv_field_str(before.get(field)) for field in fields)
            yield f"{before_row}\n"

            after = {"src_path": deid_log.src_path, "type": "after", **deid_log.tags_after}
            after_row = ",".join(_csv_field_str(after.get(field)) for field in fields)
            yield f"{after_row}\n"

    @property
    def subjects(self) -> typing.Iterable[str]:
        """Yield subject CSV lines"""
        subject_config = self.ingest.config.subject_config
        if not subject_config:
            return
        query = (
            sqla.orm.Query(M.Subject)
            .filter(M.Subject.ingest_id == self.ingest_id)
        )
        first = True
        for subject in self._iter_query(query, [M.Subject.code], T.SubjectOut):
            if first:
                first = False
                fields = [subject_config.code_format] + subject_config.map_keys
                header = ",".join(fields)
                yield f"{header}\n"
            values = [subject.code] + subject.map_values
            row = ",".join(_csv_field_str(value) for value in values)
            yield f"{row}\n"

    # Ingest-bound extra methods

    @property
    def api_key(self) -> str:
        """Get the associated api key of the ingest"""
        ingest = self.call_db(get, M.Ingest, self.ingest_id)
        return ingest.api_key  # type: ignore

    def add(self, schema: T.Schema) -> T.Schema:
        """Add new task/container/item/deid-log to the ingest"""
        model_name = type(schema).__name__.replace("In", "")
        assert model_name in ("Task", "Container", "Item", "DeidLog")
        model_cls = getattr(M, model_name)
        model = model_cls(ingest_id=self.ingest_id, **schema.dict())
        return self.call_db(add, model)

    def get(self, model_name: str, model_id: uuid.UUID) -> T.Schema:
        """Get a task/container/item/deid-log by id"""
        assert model_name in ("Task", "Container", "Item", "DeidLog")
        model_cls = getattr(M, model_name)
        return self.call_db(get, model_cls, model_id)

    def get_all(self, model_name: str, *conditions: typing.Any) -> typing.Iterable[T.Schema]:
        """Get all ingests/tasks/containers/items/deid-logs by filters"""
        assert model_name in ("Task", "Container", "Item", "DeidLog")
        model_cls = getattr(M, model_name)
        order_by = _get_paginate_order_by_col(model_cls)
        query = sqla.orm.Query(model_cls).filter(model_cls.ingest_id == self.ingest_id)
        for condition in conditions:
            query = query.filter(condition)
        return self._iter_query(query, [order_by], model_cls.schema_cls())

    def get_items_sorted_by_dst_path(self) -> typing.Iterable[T.ItemWithContainerPath]:
        """Get items sorted by destination path including the filename.

        Primarily used in the detect duplicates task where sorting makes possible to
        find filepath conflicts without holding too much information in memory
        or overload the db backend with too much queries.
        """
        query = (
            sqla.orm.Query([
                M.Item.id,
                M.Item.dir,
                M.Item.filename,
                M.Item.existing,
                M.Container.path.label("container_path"),
            ])
            .join(M.Item.container)
            .filter(M.Item.ingest_id == self.ingest_id)
        )
        return self._iter_query(
            query,
            [M.Container.path.label("container_path"), M.Item.filename],
            T.ItemWithContainerPath,
        )

    def get_items_with_error_count(self) -> typing.Iterable[T.ItemWithErrorCount]:
        """Get all items with the number of realated errors"""
        query = (
            sqla.orm.Query([
                M.Item.id,
                M.Item.existing,
                sqla.sql.func.count(M.ItemError.id).label("error_cnt"),
            ])
            .outerjoin(M.Item.errors)
            .group_by(M.Item.id)
            .filter(M.Item.ingest_id == self.ingest_id)
        )

        return self._iter_query(query, [M.Item.id], T.ItemWithErrorCount)

    def count_all(self, model_name: str) -> int:
        """Get count of tasks/containers/items/deid-logs"""
        assert model_name in ("Task", "Container", "Item", "DeidLog")
        model_cls = getattr(M, model_name)
        return self.call_db(count_all, self.ingest.id, model_cls)

    def update(self, model_name: str, model_id: uuid.UUID, **updates: typing.Any) -> T.Schema:
        """Update a task/container/item"""
        assert model_name in ("Task", "Container", "Item")
        model_cls = getattr(M, model_name)
        return self.call_db(update, model_cls, model_id, **updates)

    def find_one(self, model_name: str, *conditions: typing.Any) -> typing.Any:
        """
        Get a task/container/item/deid-log by the specified key.

        Conditions need to specified in a way that uniquely identify an item.
        """
        assert model_name in ("Task", "Container", "Item", "DeidLog")
        assert conditions
        model_cls = getattr(M, model_name)
        conditions = (model_cls.ingest_id == self.ingest_id,) + conditions
        return self.call_db(find_one, model_cls, *conditions)

    def bulk(self, type_: str, model_name: str, mappings: typing.List[dict]) -> None:
        """Bulk add/update tasks/containers/items"""
        assert type_ in ("insert", "update")
        assert model_name in ("Task", "Container", "Item", "ItemError")
        model_cls = getattr(M, model_name)
        if type_ == "insert":
            def _set_ingest_id(obj):
                obj = copy.copy(obj)
                obj["ingest_id"] = self.ingest_id
                return obj
            mappings = [_set_ingest_id(m) for m in mappings]
        self.call_db(bulk, type_, model_cls, mappings)

    def start_resolving(self) -> T.IngestOut:
        """Set ingest status to resolving and add resolve task if all scans finished"""
        ingest = self.call_db(get, M.Ingest, self.ingest_id)
        if T.IngestStatus.is_terminal(ingest.status):  # type: ignore
            return ingest  # type: ignore
        if self.call_db(has_unfinished_tasks, self.ingest_id):
            return ingest  # type: ignore
        return self.call_db(start_singleton, self.ingest_id, T.TaskType.resolve)

    def start_detecting_duplicates(self) -> T.IngestOut:
        """Start detecting duplicates"""
        return self.call_db(start_singleton, self.ingest_id, T.TaskType.detect_duplicates)

    def resolve_subject(self, map_values: typing.List[str]) -> str:
        """Get existing or create new subject code based on the map values"""
        return self.call_db(resolve_subject, self.ingest_id, map_values)

    def start_finalizing(self) -> T.IngestOutAPI:
        """Set ingest status to finalizing and add finalize task if all uploads finished"""
        ingest = self.ingest
        if T.IngestStatus.is_terminal(ingest.status):
            return ingest
        if self.call_db(has_unfinished_tasks, self.ingest_id):
            return ingest
        return self.call_db(start_singleton, self.ingest_id, T.TaskType.finalize)

    def set_ingest_status(self, status: T.IngestStatus) -> T.IngestOut:
        """Set ingest status"""
        return self.call_db(set_ingest_status, self.ingest_id, status)

    def fail(self) -> T.IngestOut:
        """Set ingest status to failed and cancel pending tasks"""
        return self.call_db(fail_ingest, self.ingest_id)

    def batch_writer(self, *args, **kwargs) -> "BatchWriter":
        """Get batch writer which is bound to this client"""
        return BatchWriter(self, *args, **kwargs)

    def _iter_query(
        self,
        query: sqla.orm.Query,
        order_by_cols: typing.List[sqla.Column],
        schema: typing.Type[T.Schema],
        size: int = 10000
    ) -> typing.Iterable[typing.Any]:
        """Get all rows of the given query using seek method"""
        id_col = _get_id_column_from_query(query)
        columns = []
        for col in order_by_cols:
            if isinstance(col, sqla.sql.elements.Label):
                columns.append(col.element)
            else:
                columns.append(col)
        query = seek_query = query.order_by(*order_by_cols, id_col)
        while True:
            count = 0
            item = None
            for item in self.call_db(get_all, seek_query.limit(size), schema):
                count += 1
                yield item

            if count < size:
                break

            if item:
                values = []
                for col in order_by_cols:
                    values.append(getattr(item, col.name))
                seek_query = query.filter(sqla.sql.tuple_(*order_by_cols, id_col) > (*values, item.id))  # type: ignore
            else:
                break


class BatchWriter:
    """Batch insert/update writer of a given model"""

    def __init__(
        self,
        db: DBClient,
        type_: str,
        model_name: str,
        depends_on: "BatchWriter" = None,
        batch_size: int = 1000
    ):
        self.db = db  # pylint: disable=C0103
        self.type = type_
        self.model_name = model_name
        self.depends_on = depends_on
        self.batch_size = batch_size
        self.changes: typing.List[typing.Any] = []

    def push(self, change: typing.Any) -> None:
        """Push new change"""
        self.changes.append(change)
        if len(self.changes) >= self.batch_size:
            self.flush()

    def flush(self) -> None:
        """Flush all changes"""
        if self.depends_on:
            self.depends_on.flush()
        self.db.bulk(self.type, self.model_name, self.changes)
        self.changes = []


class FunctionTransactionInfo(typing.Generic[S]):  # pylint: disable=R0903
    """Holds transaction type for a given function."""
    def __init__(self, func: typing.Callable[..., S], type_="DEFERRED"):
        self.func = func
        self.transaction_type = type_
        functools.update_wrapper(self, func)

    def __call__(self, *args, **kwargs) -> S:
        return self.func(*args, **kwargs)

@typing.overload
def transaction(func: None = None, *, type_: str = "DEFERRED") -> typing.Callable[[F], F]:
    """Decorator to set transaction type for a function"""
    ...

@typing.overload
def transaction(func: F) -> F:
    """Decorator to set transaction type for a function"""
    ...

def transaction(
    func: typing.Optional[F] = None, *, type_: str = "DEFERRED"
) -> typing.Union[F, typing.Callable[[F], F]]:
    """Decorator to set transaction type for a function"""
    if func:
        return FunctionTransactionInfo(func)
    return functools.partial(FunctionTransactionInfo, type_=type_)  # type: ignore

# Transactional crud methods

@transaction
def add(db: sqla.orm.Session, model: M.Base) -> T.Schema:
    """Add an object"""
    db.add(model)
    db.flush()
    return model.schema()


@transaction
def get(db: sqla.orm.Session, model_cls: typing.Type[M.Base], id_: uuid.UUID) -> T.Schema:
    """Get object by ID"""
    return db.query(model_cls).filter(model_cls.id == id_).one().schema()


@transaction
def get_all(
    db: sqla.orm.Session,
    query: sqla.orm.Query,
    schema: T.Schema,
) -> typing.List[T.Schema]:
    """Get all object that match the given query"""
    return [schema.from_orm(model) for model in query.with_session(db).all()]


@transaction
def count_all(db: sqla.orm.Session, ingest_id: uuid.UUID, model_cls: typing.Type[M.Base]) -> int:
    """Get count of row for the specified model"""
    return (
        db.query(sqla.sql.func.count(model_cls.id).label("count"))
        .filter(model_cls.ingest_id == ingest_id)
        .scalar()
    )


@transaction
def update(
    db: sqla.orm.Session,
    model_cls: M.Base,
    id_: uuid.UUID,
    **updates: typing.Any
) -> T.Schema:
    """Update an object with the given update set"""
    query = db.query(model_cls).filter(model_cls.id == id_)
    query.update(updates)
    db.flush()
    return query.one().schema()


@transaction
def find_one(
    db: sqla.orm.Session,
    model_cls: M.Base,
    *conditions: typing.Any,
) -> T.Schema:
    """Find one matching row for the given model."""
    query = db.query(model_cls)
    for condition in conditions:
        query = query.filter(condition)
    return query.one().schema()


@transaction
def bulk(
    db: sqla.orm.Session, type_: str, model_cls: M.Base, mappings: typing.List[typing.Any]
) -> None:
    """Perform a bulk insert/update of the given list of mapping dictionaries"""
    assert type_ in ("insert", "update")
    bulk_method = getattr(db, f"bulk_{type_}_mappings")
    bulk_method(model_cls, mappings)
    db.flush()


@transaction(type_="IMMEDIATE")
def start(db: sqla.orm.Session, ingest_id: uuid.UUID) -> T.IngestOut:
    """Start the ingest, set ingest status to scanning and kick off
    the initial template scan task.

    Lock on the ingest row until the transaction ends to prevent starting
    multiple initial scan tasks.
    """
    ingest = _get_ingest(db, ingest_id, for_update=True)
    assert ingest.status == T.IngestStatus.created
    ingest.status = T.IngestStatus.scanning
    db.add(M.Task(
        ingest_id=ingest_id,
        type=T.TaskType.scan,
        context={"scanner": {"type": "template", "dir": "/"}},
    ))
    db.flush()
    return ingest.schema()


@transaction(type_="IMMEDIATE")
def review(
    db: sqla.orm.Session, ingest_id: uuid.UUID, changes: typing.Optional[T.ReviewIn] = None
) -> T.IngestOut:
    """Save review and start preparing, set ingest status to preparing and kick off
    the prepare task.

    Lock on the ingest row until the transaction ends to prevent starting multiple
    prepare tasks.
    """
    ingest = _get_ingest(db, ingest_id, for_update=True)
    assert ingest.status == T.IngestStatus.in_review
    ingest.status = T.IngestStatus.preparing
    if changes is not None:
        for change in changes:
            db.add(M.Review(ingest_id=ingest_id, **change.dict()))
    db.add(M.Task(ingest_id=ingest_id, type=T.TaskType.prepare))
    db.flush()
    return ingest.schema()


@transaction(type_="IMMEDIATE")
def abort(db: sqla.orm.Session, ingest_id: uuid.UUID) -> T.IngestOut:
    """Abort the ingest, set ingest status to aborted and cancel all pending
    tasks.

    Lock on the ingest row until the transaction ends to prevent setting ingest/tasks
    statuses multiple times.
    """
    ingest = _get_ingest(db, ingest_id, for_update=True)
    if ingest.status == T.IngestStatus.aborted:
        return ingest.schema()
    ingest.status = T.IngestStatus.aborted
    _cancel_pending_tasks(db, ingest_id)
    db.flush()
    return ingest.schema()


@transaction(type_="IMMEDIATE")
def next_task(db: sqla.orm.Session, worker: str) -> typing.Optional[T.TaskOut]:
    """Get next task which's status is pending and set the status to running.

    Lock on the first task that match and skip any locked ones. This prevents the
    workers to grab the same task.
    """
    query = _for_update(
        db.query(M.Task).filter(M.Task.status == T.TaskStatus.pending),
        skip_locked=True,
    )
    task = query.first()
    if task is None:
        return None
    task.worker = worker
    task.status = T.TaskStatus.running
    db.flush()
    return task.schema()


@transaction
def get_progress(db: sqla.orm.Session, ingest_id: uuid.UUID) -> T.Progress:
    """Get ingest scan task and item/file/byte counts by status"""
    progress = T.Progress().dict()
    scan_tasks_by_status = (
        db.query(
            M.Task.status,
            sqla.sql.func.count(M.Task.id).label("count"),
        )
        .filter(
            M.Task.ingest_id == ingest_id,
            M.Task.type == T.TaskType.scan,
        )
        .group_by(M.Task.status)
    )
    for row in scan_tasks_by_status:
        progress["scans"][row.status] = row.count
        progress["scans"]["total"] += row.count
        if T.TaskStatus.is_terminal(row.status):
            progress["scans"]["finished"] += row.count

    tasks_by_type = (
        db.query(
            M.Task.type,
            sqla.sql.func.sum(M.Task.completed).label("completed"),
            sqla.sql.func.sum(M.Task.total).label("total"),
        )
        .filter(
            M.Task.ingest_id == ingest_id,
        )
        .group_by(M.Task.type)
    )
    for row in tasks_by_type:
        progress["stages"][T.TaskType.ingest_status(row.type)]["completed"] = row.completed
        progress["stages"][T.TaskType.ingest_status(row.type)]["total"] = row.total

    items_by_status = (
        db.query(
            M.Task.status,
            M.Item.skipped,
            sqla.sql.func.count(M.Item.id).label("items"),
            sqla.sql.func.sum(M.Item.files_cnt).label("files"),
            sqla.sql.func.sum(M.Item.bytes_sum).label("bytes"),
        )
        .outerjoin(M.Item.task)
        .filter(M.Item.ingest_id == ingest_id)
        .group_by(M.Task.status, M.Item.skipped)
    )
    for row in items_by_status.all():
        if row.skipped:
            # items skipped via review tracked separately
            status = "skipped"
        elif row.status is None:
            # items that don't have any (upload task) status yet
            status = "scanned"
        else:
            # items with an upload task tracked as the task status
            status = row.status

        for attr in ("items", "files", "bytes"):
            progress[attr][status] = getattr(row, attr)
            progress[attr]["total"] += getattr(row, attr)
            if T.TaskStatus.is_terminal(status):
                progress[attr]["finished"] += getattr(row, attr)
    return T.Progress(**progress)


@transaction
def get_summary(db: sqla.orm.Session, ingest_id: uuid.UUID) -> T.Summary:
    """Get ingest hierarchy node and file count by level and type"""
    summary = {}
    containers_by_level = (
        db.query(
            M.Container.level,
            sqla.sql.func.count(M.Container.id).label("count"))
        .filter(M.Container.ingest_id == ingest_id)
        .group_by(M.Container.level)
    )
    for row in containers_by_level.all():
        level_name = T.ContainerLevel.get_item(row.level).name
        summary[f"{level_name}s"] = row.count
    items_by_type = (
        db.query(
            M.Item.type,
            sqla.sql.func.count(M.Item.id).label("count"))
        .filter(M.Item.ingest_id == ingest_id)
        .group_by(M.Item.type)
    )
    for row in items_by_type.all():
        summary[f"{row.type}s"] = row.count
    errors_by_type = (
        db.query(
            M.ItemError.error_code,
            sqla.sql.func.count(M.ItemError.id).label("count")
        )
        .filter(M.ItemError.ingest_id == ingest_id)
        .group_by(M.ItemError.error_code)
    )
    for row in errors_by_type.all():
        error = errors.get_item_error_by_code(row.error_code)
        summary.setdefault("errors", []).append({
            "code": error.code,
            "message": error.message,
            "description": error.description,
            "count": row.count,
        })
    return T.Summary(**summary)


@transaction
def get_report(db: sqla.orm.Session, ingest_id: uuid.UUID) -> T.Report:
    """Get ingest status, elapsed time per status and list of failed tasks"""
    ingest = _get_ingest(db, ingest_id)
    elapsed = {}
    for old, new in zip(ingest.history, ingest.history[1:]):
        old_status, old_timestamp = old
        new_status, new_timestamp = new  # pylint: disable=W0612
        elapsed[old_status] = new_timestamp - old_timestamp
    failed_tasks = (
        db.query(
            M.Task.id.label("task"),  # pylint: disable=E1101
            M.Task.type,
            M.Task.error.label("message"),
        )
        .filter(
            M.Task.ingest_id == ingest_id,
            M.Task.status == T.TaskStatus.failed,
        )
        .order_by(M.Task.created)
    )
    return T.Report(
        status=ingest.status,
        elapsed=elapsed,
        errors=failed_tasks.all(),
    )


@transaction(type_="IMMEDIATE")
def start_singleton(db: sqla.orm.Session, ingest_id: uuid.UUID, type_: T.TaskType) -> T.IngestOut:
    """Start singleton task (resolve, finalize).

    Lock on the ingest row until the transaction ends to prevent strating singletons multiple times.
    """
    # all scan tasks finished - lock the ingest
    ingest = _get_ingest(db, ingest_id, for_update=True)
    # set status and add scan task (once - noop for 2nd worker)
    if ingest.status != T.TaskType.ingest_status(type_) and not T.IngestStatus.is_terminal(ingest.status):
        ingest.status = T.TaskType.ingest_status(type_)
        db.add(M.Task(ingest_id=ingest_id, type=type_))
        db.flush()
    return ingest.schema()


@transaction
def has_unfinished_tasks(db: sqla.orm.Session, ingest_id: uuid.UUID) -> bool:
    """Return true if there are penging/running tasks otherwise false"""
    pending_or_running = (
        db.query(M.Task.id)
        .filter(
            M.Task.ingest_id == ingest_id,
            M.Task.status.in_([T.TaskStatus.pending, T.TaskStatus.running])
        )
    )
    return bool(pending_or_running.count())


@transaction(type_="IMMEDIATE")
def resolve_subject(
    db: sqla.orm.Session, ingest_id: uuid.UUID, map_values: typing.List[str]
) -> str:
    """Get existing or create new subject code based on the map values"""
    ingest = _get_ingest(db, ingest_id, for_update=True)
    subject = (
        db.query(M.Subject)
        .filter(
            M.Subject.ingest_id == ingest_id,
            M.Subject.map_values == map_values,
        )
        .first()
    )
    if subject is None:
        subject_config = ingest.config["subject_config"]
        subject_config["code_serial"] += 1
        sqla.orm.attributes.flag_modified(ingest, "config")
        subject = M.Subject(
            ingest_id=ingest_id,
            code=subject_config["code_format"].format(
                SubjectCode=subject_config["code_serial"]
            ),
            map_values=map_values,
        )
        db.add(subject)
        db.flush()
    return subject.code


@transaction(type_="IMMEDIATE")
def set_ingest_status(
    db: sqla.orm.Session, ingest_id: uuid.UUID, status: T.IngestStatus
) -> T.IngestOut:
    """Set ingest status"""
    ingest = _get_ingest(db, ingest_id, for_update=True)
    if ingest.status != status:
        ingest.status = status
        db.flush()
    return ingest.schema()


@transaction(type_="IMMEDIATE")
def fail_ingest(db: sqla.orm.Session, ingest_id: uuid.UUID) -> T.IngestOut:
    """Set ingest status to failed and cancel pending tasks"""
    ingest = _get_ingest(db, ingest_id, for_update=True)
    ingest.status = T.IngestStatus.failed
    _cancel_pending_tasks(db, ingest_id)
    db.flush()
    return ingest.schema()


@transaction(type_="IMMEDIATE")
def load_subject_csv(
    db: sqla.orm.Session, ingest_id: uuid.UUID, subject_csv: typing.BinaryIO
) -> None:
    """Load subject codes from csv file.

    Lock on the ingest row to prevent mixing different subject configs.
    """
    ingest = _get_ingest(db, ingest_id, for_update=True)
    subject_config = ingest.config.setdefault("subject_config", {})
    header = subject_csv.readline().decode("utf8").strip()
    code_format, *map_keys = header.split(",")
    if subject_config:
        assert map_keys == subject_config["map_keys"]
    else:
        subject_config["code_format"] = code_format
        subject_config["map_keys"] = map_keys
    subject_config.setdefault("code_serial", 0)

    code_re = re.compile(r"^[^\d]*(\d+)[^\d]*$")
    for line in subject_csv:
        subject = line.decode("utf8").strip()
        code, *map_values = subject.split(",")
        match = code_re.match(code)
        if not match:
            raise ValueError(f"Invalid code in subject csv: {code}")
        code_int = int(match.group(1))
        if code_int > subject_config["code_serial"]:
            subject_config["code_serial"] = code_int
        # NOTE all subjects in memory
        db.add(M.Subject(
            ingest_id=ingest_id,
            code=code,
            map_values=map_values,
        ))
    sqla.orm.attributes.flag_modified(ingest, "config")
    db.flush()

# Helpers

def _get_ingest(db: sqla.orm.Session, ingest_id: uuid.UUID, for_update: bool = False) -> M.Ingest:
    """Get ingest by ID and locks on it if requested"""
    query = db.query(M.Ingest).filter(M.Ingest.id == ingest_id)
    if for_update:
        query = _for_update(query)
    return query.one()


def _for_update(query: sqla.orm.Query, skip_locked: bool = False) -> sqla.orm.Query:
    """Lock as granularly as possible for given query and backend"""
    # with_for_update() locks selected rows in postgres
    # (ignored w/ sqlite, but its not a problem, since we use immediate transactions there)
    # skip_locked silently skips over records that are currently locked
    # populate_existing to get objects with the latest modifications
    # see: https://github.com/sqlalchemy/sqlalchemy/issues/4774
    return query.with_for_update(skip_locked=skip_locked).populate_existing()


def _cancel_pending_tasks(db: sqla.orm.Session, ingest_id: uuid.UUID) -> None:
    """Cancel all pending tasks"""
    pending_tasks = db.query(M.Task).filter(
        M.Task.ingest_id == ingest_id,
        M.Task.status == T.TaskStatus.pending,
    )
    pending_tasks.update({M.Task.status: T.TaskStatus.canceled})


def _csv_field_str(field):
    """Stringify csv fields"""
    return "" if field is None else str(field)


def _get_paginate_order_by_col(model_cls: M.Base) -> sqla.Column:
    """Determine the primary order by column for a given model.

    If the model has a compound index for the paginator then return the index's second column,
    otherwise the ID column.
    """
    for index in model_cls.__table__.indexes:
        if isinstance(index, sqla.Index) and index.name.endswith("_paginate"):
            col = index.columns.items()[1][1]
            return getattr(model_cls, col.name)
    return model_cls.id


def _get_id_column_from_query(query: sqla.orm.Query) -> sqla.Column:
    """Get id column from the given query's column descriptions.

    Used to always order rows by a unique column in _iter_query.
    """
    for col_desc in query.column_descriptions:
        if inspect.isclass(col_desc["expr"]):
            return col_desc["expr"].id
        if col_desc["name"] == "id":
            return col_desc["expr"]
    raise ValueError("No id column detected in query")


__all__ = [
    "DBClient"
]
