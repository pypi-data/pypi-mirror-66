from wechatpy.enterprise import WeChatClient
from wechatpy.session import SessionStorage
from wechatpy.utils import to_text
from wechatpy.utils import json
from ..aa import get_env


def get_wx_client_work(db):  # SsDB
    # redis_client = Redis.from_url('redis://127.0.0.1:60002/0')
    session_interface = _SSDBStorageForWX(
        db,
        prefix="wechatpy"
    )
    env = get_env()
    client = WeChatClient(
        env.wx_work_corp_id,
        env.wx_work_app_secret,
        session=session_interface
    )
    return client


class _SSDBStorageForWX(SessionStorage):
    def __init__(self, db, prefix='wechatpy'):
        self.db = db
        self.prefix = prefix

    def key_name(self, key):
        return '{0}:{1}'.format(self.prefix, key)

    def get(self, key, default=None):
        key = self.key_name(key)
        value = self.db.get(key)
        if not value:
            return default
        return json.loads(to_text(value))

    def set(self, key, value, ttl=None):
        if value is None:
            return
        key = self.key_name(key)
        value = json.dumps(value)
        self.db.setx(key, value, ttl)

    def delete(self, key):
        key = self.key_name(key)
        self.db.delete(key)
