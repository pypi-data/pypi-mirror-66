# -*- coding: utf-8 -*-

import re
import logging
from datetime import datetime
from functools import reduce, partial
from mongoengine import EmbeddedDocumentField, Document, QuerySet, register_connection
from mongoengine.queryset.visitor import Q
from mongoengine.errors import *
from spaceone.core import config
from spaceone.core import utils
from spaceone.core.error import *
from spaceone.core.model import BaseModel

_MONGO_CONNECTIONS = []
_UNIQUE_ERROR_FORMAT = 'index: {}.*dup key.*'
_LOGGER = logging.getLogger(__name__)


def _raise_unique(unique_fields, message, data):
    for name in unique_fields:
        if re.search(_UNIQUE_ERROR_FORMAT.format(name), message):
            raise ERROR_NOT_UNIQUE(key=name, value=data[name])


def _default_resolver(key, value, operator, is_multiple, is_exact_field):
    if is_multiple:
        return reduce(lambda x, y: x | y,
                      map(lambda i: Q(**{f'{key}__{operator}': i}), value))
    else:
        return Q(**{f'{key}__{operator}': value})


def _eq_resolver(key, value, is_multiple, is_exact_field):
    if is_exact_field or value is None:
        return Q(**{key: value})
    else:
        return Q(**{f'{key}__iexact': value})


def _in_resolver(key, value, is_multiple, is_exact_field):
    if is_exact_field or len(value) == 0:
        return Q(**{f'{key}__in': value})
    else:
        return reduce(lambda x, y: x | y,
                      map(lambda i: Q(**{f'{key}__iexact': i}), value))


def _not_in_resolver(key, value, is_multiple, is_exact_field):
    return Q(**{f'{key}__nin': value})


def _regex_resolver(key, value, is_multiple, is_exact_field):
    if is_multiple:
        return reduce(lambda x, y: x | y,
                      map(lambda i: Q(**{'__raw__': {key: {'$regex': i, '$options': 'i'}}}), value))
    else:
        return Q(**{'__raw__': {key: {'$regex': value, '$options': 'i'}}})


_OPERATORS = {
    # model operator : (mongoengine operator, is_multiple)
    'lt': ('lt', False),
    'lte': ('lte', False),
    'gt': ('gt', False),
    'gte': ('gte', False),
    'eq': (_eq_resolver, False),
    'not': ('ne', False),
    'exists': ('exists', False),
    'match': ('match', False),
    'contain': ('icontains', False),
    'not_contain': ('not__icontains', False),
    'regex': (_regex_resolver, False),
    'in': (_in_resolver, True),
    'not_in': (_not_in_resolver, True),
    'contain_in': ('icontains', True),
    'not_contain_in': ('not_icontains', True),
    'regex_in': (_regex_resolver, True)
}


def _stat_group_resolver(key, operator, alias):
    return {alias: f'${key}'}


def _stat_count_resolver(key, operator, alias):
    alias = alias or 'count'
    return {alias: {'$sum': 1}}


def _stat_average_resolver(key, operator, alias):
    alias = alias or f'{key}_average'
    return {alias: {'$avg': f'${key}'}}


def _stat_add_to_set_resolver(key, operator, alias):
    alias = alias or key
    return {alias: {'$addToSet': f'${key}'}}


def _stat_merge_objects_resolver(key, operator, alias):
    alias = alias or key
    return {alias: {'$mergeObjects': f'${key}'}}


def _stat_default_resolver(key, operator, alias):
    alias = alias or f'{key}_{operator}'
    return {alias: {f'${operator}': f'${key}'}}


_STAT_OPERATORS = {
    'group': _stat_group_resolver,
    'count': _stat_count_resolver,
    'sum': _stat_default_resolver,
    'average': _stat_average_resolver,
    'max': _stat_default_resolver,
    'min': _stat_default_resolver,
    'add_to_set': _stat_add_to_set_resolver,
    'merge_objects': _stat_merge_objects_resolver
}


class MongoCustomQuerySet(QuerySet):

    def last(self):
        return self.order_by('-id').first()


class MongoModel(Document, BaseModel):
    meta = {
        'abstract': True,
        'queryset_class': MongoCustomQuerySet
    }

    @classmethod
    def connect(cls):
        db_alias = cls._meta.get('db_alias', 'default')
        if db_alias not in _MONGO_CONNECTIONS:
            global_conf = config.get_global()
            if db_alias not in global_conf.get('DATABASES', {}):
                raise ERROR_DB_CONFIGURATION(backend=db_alias)

            db_conf = global_conf['DATABASES'][db_alias].copy()
            register_connection(db_alias, **db_conf)

            _MONGO_CONNECTIONS.append(db_alias)

    @classmethod
    def create(cls, data):
        create_data = {}
        unique_fields = []

        for name, field in cls._fields.items():
            if field.unique:
                unique_fields.append(name)

            if name in data:
                create_data[name] = data[name]
            else:
                generate_id = getattr(field, 'generate_id', None)
                if generate_id:
                    create_data[name] = utils.generate_id(generate_id)

                if getattr(field, 'auto_now', False):
                    create_data[name] = datetime.utcnow()
                elif getattr(field, 'auto_now_add', False):
                    create_data[name] = datetime.utcnow()

        try:
            new_vo = cls(**create_data).save()
        except NotUniqueError as e:
            _raise_unique(unique_fields, str(e), create_data)
            raise ERROR_NOT_UNIQUE_KEYS(keys=', '.join(unique_fields))
        except Exception as e:
            raise ERROR_DB_QUERY(reason=e)

        return new_vo

    def update(self, data):
        unique_fields = []
        updatable_fields = self._meta.get('updatable_fields',
                                          list(filter(lambda x: x != self._meta.get('id_field', 'id'),
                                                      self._fields.keys())))

        for key in list(data.keys()):
            if key not in updatable_fields:
                del data[key]

        for name, field in self._fields.items():
            if field.unique:
                unique_fields.append(name)

            if getattr(field, 'auto_now', False):
                if name not in data.keys():
                    data[name] = datetime.utcnow()

        if data != {}:
            try:
                super().update(**data)
                self.reload()
            except NotUniqueError as e:
                _raise_unique(unique_fields, str(e), data)
                raise ERROR_DB_QUERY(reason=e)
            except Exception as e:
                raise ERROR_DB_QUERY(reason=e)

        return self

    def delete(self):
        super().delete()

    def terminate(self):
        super().delete()

    def set_data(self, key, data):
        key = key.replace('.', '__')
        set_data = {
            f'set__{key}': data
        }

        super().update(**set_data)
        self.reload()
        return self

    def unset_data(self, *keys):
        unset_data = {}

        for key in keys:
            key = key.replace('.', '__')
            unset_data[f'unset__{key}'] = 1

        super().update(**unset_data)
        self.reload()
        return self

    def append(self, key, data):
        append_data = {}

        field = getattr(self._fields.get(key, {}), 'field', None)
        if field and isinstance(field, EmbeddedDocumentField):
            reference_model = field.document_type_obj
            append_data[f'push__{key}'] = reference_model(**data)
        else:
            append_data[f'push__{key}'] = data

        super().update(**append_data)
        self.reload()
        return self

    def remove(self, key, data):
        remove_data = {
            f'pull__{key}': data
        }
        super().update(**remove_data)
        self.reload()
        return self

    @classmethod
    def get(cls, only=None, **conditions):
        vos = cls.filter(**conditions)

        if vos.count() == 0:
            keys = tuple(conditions.keys())
            values = tuple(conditions.values())

            if len(keys) == 1:
                raise ERROR_NOT_FOUND(key=keys[0], value=values[0])
            else:
                raise ERROR_NOT_FOUND(key=keys, value=values)

        if only:
            vos = vos.only(*only)

        return vos.first()

    @classmethod
    def filter(cls, **conditions):
        change_conditions = {}
        for key, value in conditions.items():
            if isinstance(value, list):
                change_conditions[f'{key}__in'] = value
            else:
                change_conditions[key] = value

        return cls.objects.filter(**change_conditions)

    def to_dict(self):
        return self.to_mongo()

    @staticmethod
    def _check_operator_value(is_multiple, operator, value, condition):
        if is_multiple:
            if not isinstance(value, list):
                raise ERROR_OPERATOR_LIST_VALUE_TYPE(operator=operator, condition=condition)

        else:
            if isinstance(value, list):
                raise ERROR_OPERATOR_VALUE_TYPE(operator=operator, condition=condition)

    @classmethod
    def _check_exact_field(cls, key, value):
        if key in cls._meta.get('exact_fields', []) or value is None:
            return True
        else:
            return False

    @classmethod
    def _check_reference_field(cls, key):
        ref_keys = cls._meta.get('reference_query_keys', {}).keys()
        if key in ref_keys:
            return False
        else:
            return True

    @classmethod
    def _get_reference_model(cls, key):
        for ref_key, ref_model in cls._meta.get('reference_query_keys', {}).items():
            if key.startswith(ref_key) and key[len(ref_key)] == '.':
                ref_model_key = key.replace(f'{ref_key}.', '')
                if ref_model == 'self':
                    return cls, ref_key, ref_model_key
                else:
                    return ref_model, ref_key, ref_model_key

        return None, None, None

    @classmethod
    def _change_reference_condition(cls, key, value, operator, is_exact_field):
        ref_model, ref_key, ref_model_key = cls._get_reference_model(key)
        if ref_model:
            if value is None:
                return ref_key, value, operator, is_exact_field
            else:
                ref_vos, total_count = ref_model.query(
                    filter=[{'k': ref_model_key, 'v': value, 'o': operator}])
                return ref_key, list(ref_vos), 'in', True

        else:
            return key, value, operator, is_exact_field

    @classmethod
    def _make_condition(cls, condition, change_query_keys):
        key = condition.get('key', condition.get('k'))
        value = condition.get('value', condition.get('v'))
        operator = condition.get('operator', condition.get('o'))

        if operator not in _OPERATORS:
            raise ERROR_DB_QUERY(reason=f'Filter condition is invalid : {condition}')

        mongo_operator, is_multiple = _OPERATORS.get(operator)

        cls._check_operator_value(is_multiple, operator, value, condition)
        is_exact_field = cls._check_exact_field(key, value)

        if key and operator:
            if key in change_query_keys:
                key = change_query_keys[key]

            if operator not in ['regex', 'regex_in']:
                if cls._check_reference_field(key):
                    key, value, operator, is_exact_field = \
                        cls._change_reference_condition(key, value, operator, is_exact_field)

                    mongo_operator = _OPERATORS[operator][0]

                key = key.replace('.', '__')

            if callable(mongo_operator):
                return mongo_operator(key, value, is_multiple, is_exact_field)
            else:
                return _default_resolver(key, value, mongo_operator, is_multiple, is_exact_field)
        else:
            raise ERROR_DB_QUERY(reason='Filter condition should have key, value and operator.')

    @classmethod
    def query(cls, *args, only=None, exclude=None, all_fields=False, distinct=None,
              filter=[], filter_or=[], sort={}, page={}, minimal=False, count_only=False, **kwargs):
        _filter = None
        _filter_or = None
        _order_by = None
        minimal_fields = cls._meta.get('minimal_fields')
        change_query_keys = cls._meta.get('change_query_keys', {})

        if len(filter) > 0:
            _filter = reduce(lambda x, y: x & y,
                             map(partial(cls._make_condition, change_query_keys=change_query_keys),
                                 filter))

        if len(filter_or) > 0:
            _filter_or = reduce(lambda x, y: x | y,
                                map(partial(cls._make_condition, change_query_keys=change_query_keys),
                                    filter_or))

        if _filter and _filter_or:
            _filter = _filter & _filter_or
        else:
            _filter = _filter or _filter_or

        if 'key' in sort:
            if sort.get('desc', False):
                _order_by = f'-{sort["key"]}'
            else:
                _order_by = f'{sort["key"]}'

        try:
            vos = cls.objects.filter(_filter)

            if _order_by:
                vos = vos.order_by(_order_by)

            if only:
                vos = vos.only(*only)

            if exclude:
                vos = vos.exclude(*exclude)

            if minimal and minimal_fields:
                vos = vos.only(*minimal_fields)

            if all_fields:
                vos = vos.all_fields()

            if distinct:
                vos = vos.distinct(distinct)

            total_count = vos.count()

            if count_only:
                vos = []

            else:
                if 'limit' in page and page['limit'] > 0:
                    start = page.get('start', 1)
                    if start < 1:
                        start = 1

                    vos = vos[start - 1:start + page['limit'] - 1]

                # vos.select_related(3)

            return vos, total_count

        except Exception as e:
            raise ERROR_DB_QUERY(reason=e)

    @classmethod
    def _get_stat_group_value(cls, group_key, group_value, _reference_group_by):
        if group_key in _reference_group_by.keys():
            ref_info = _reference_group_by[group_key]
            ref_vo = ref_info['model'].get(id=group_value)
            return getattr(ref_vo, ref_info['key'])
        else:
            return group_value

    @classmethod
    def _make_stat_values(cls, cursor, _reference_group_by):
        values = []
        for row in cursor:
            data = {}
            for key, value in row.items():
                if key == '_id':
                    for group_key, group_value in row[key].items():
                        data[group_key] = cls._get_stat_group_value(group_key, group_value, _reference_group_by)
                else:
                    data[key] = value

            values.append(data)

        return values

    @classmethod
    def _make_group_by_condition(cls, group_by):
        _reference_group_by = {}
        _group_by = {
            '$group': {
                '_id': {}
            }
        }

        for condition in group_by:
            key = condition.get('key', condition.get('k'))
            operator = condition.get('operator', condition.get('o'))
            alias = condition.get('alias', condition.get('a'))

            if operator not in _STAT_OPERATORS:
                raise ERROR_DB_QUERY(reason=f"'group_by' condition's operator is invalid : {condition}")

            if operator != 'count' and key is None:
                raise ERROR_DB_QUERY(reason=f"'group_by' condition's key is required : {condition}")

            if operator == 'group':
                alias = alias or key
                ref_model, ref_key, ref_model_key = cls._get_reference_model(key)
                if ref_model:
                    _reference_group_by[alias] = {'model': ref_model, 'key': ref_model_key}
                    _group_by['$group']['_id'].update(_STAT_OPERATORS[operator](ref_key, operator, alias))
                else:
                    _group_by['$group']['_id'].update(_STAT_OPERATORS[operator](key, operator, alias))
            else:
                _group_by['$group'].update(_STAT_OPERATORS[operator](key, operator, alias))

        return _group_by, _reference_group_by

    @classmethod
    def stat(cls, *args, group_by=None, filter=[], filter_or=[], sort={}, limit=None, **kwargs):
        if group_by is None:
            raise ERROR_REQUIRED_PARAMETER(key='query.group_by')

        pipeline = []
        _filter = None
        _filter_or = None
        change_query_keys = cls._meta.get('change_query_keys', {})

        if len(filter) > 0:
            _filter = reduce(lambda x, y: x & y,
                             map(partial(cls._make_condition, change_query_keys=change_query_keys),
                                 filter))

        if len(filter_or) > 0:
            _filter_or = reduce(lambda x, y: x | y,
                                map(partial(cls._make_condition, change_query_keys=change_query_keys),
                                    filter_or))

        if _filter and _filter_or:
            _filter = _filter & _filter_or
        else:
            _filter = _filter or _filter_or

        _group_by, _reference_group_by = cls._make_group_by_condition(group_by)
        pipeline.append(_group_by)

        if 'key' in sort:
            if sort.get('desc', False):
                pipeline.append({
                    '$sort': {sort['key']: 1}
                })
            else:
                pipeline.append({
                    '$sort': {sort['key']: -1}
                })

        if limit:
            pipeline.append({
                '$limit': limit
            })

        try:
            vos = cls.objects.filter(_filter)

            return cls._make_stat_values(vos.aggregate(pipeline), _reference_group_by)

        except Exception as e:
            raise ERROR_DB_QUERY(reason=e)
