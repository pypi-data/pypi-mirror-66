from datetime import datetime

from spintop.persistence.base import PersistenceFacade

from ..models import PersistenceRecordCollection, Query, get_json_serializer, SerializedPersistenceRecord

from .schemas import records_schema, record_count_schema

class SpintopAPIPersistenceFacade(PersistenceFacade):
    def __init__(self, spintop_api):
        self.spintop_api = spintop_api
        self.serializer = get_json_serializer()
        super().__init__(self.serializer)

    @classmethod
    def from_env(self, uri, database_name=None, env=None):
        # database_name is the org_id
        api = env.spintop_factory()
        return api.records

    @property
    def session(self):
        return self.spintop_api.session

    def _create(self, records):
        serialized = self._records_in_schema(records)
        return self.session.post(self.spintop_api.get_link('records.create'), json=serialized)
        
    def _records_in_schema(self, records):
        return records_schema.dump({'records': [record.as_dict() for record in records]})

    def _retrieve(self, query, limit_range=None, with_data=True):
        query_dict = query.as_dict()
        if limit_range:
            query_dict['limit_range_inf'] = limit_range[0]
            query_dict['limit_range_sup'] = limit_range[1]
            
        query_dict['with_data'] = with_data

        resp = self.session.get(self.spintop_api.get_link('records.retrieve'), params=query_dict)
        records = records_schema.load(resp.json())['records']
        return (SerializedPersistenceRecord(record) for record in records)
        
    def _count(self, query):
        query_dict = query.as_dict()
        resp = self.session.get(self.spintop_api.get_link('records.count'), params=query_dict)
        return record_count_schema.load(resp.json())['count']

    def _update(self, records, upsert=True):
        serialized = self._records_in_schema(records)
        return self.session.put(self.spintop_api.get_link('records.update'), json=serialized)
    
    def _delete(self, query):
        query_dict = query.as_dict()
        return self.session.delete(self.spintop_api.get_link('records.delete'), params=query_dict)