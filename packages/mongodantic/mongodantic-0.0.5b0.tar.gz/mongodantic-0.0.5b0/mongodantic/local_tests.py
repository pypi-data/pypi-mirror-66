from mongodantic.logical import Query as Q
from typing import List
from mongodantic import init_db_connection_params
from mongodantic.types import ObjectIdStr
from urllib.parse import quote_plus as quote
from bson import ObjectId
MONGO_URL = 'mongodb://{user}:{pw}@{hosts}/?replicaSet={rs}&authSource={auth_src}'.format(
        user=quote('test'),
        pw=quote('2310zavbdJ'),
        hosts=','.join([
            # 'rc1c-h6o0trfu8tyxe4f4.mdb.yandexcloud.net:27018'
            'rc1c-xtmirfqttmz6j2fh.mdb.yandexcloud.net:27018'
        ]),
        rs='rs01',
        auth_src='test_db')
MONGO_DATABASE_NAME = 'test_db'
init_db_connection_params(MONGO_URL, MONGO_DATABASE_NAME)
from mongodantic.models import MongoModel


class Test(MongoModel):
    name: str
    position: int


class ReferTest(MongoModel):
    name: str
    test_id: ObjectIdStr


ReferTest.find_one()
Test.aggregate_lookup(local_field='_id', from_collection=ReferTest, foreign_field='test_id', name='first').first()


f = ReferTest.aggregate_lookup(local_field='test_id', from_collection=Test, with_unwing=False)
for i in f:
    i


s = Q(name=123) | Q(name__ne=124) & Q(position=1) | Q(position=2)
Test.find_with_count(s)
t = Test.find()
t.first()
Test.find_one(sort=-1)
