import aioredis
from aioredis.errors import MasterNotFoundError

MasterNotFoundError = MasterNotFoundError
MasterResetError = ConnectionResetError


class ServerCommandsMixin:
    async def flushdb(self) -> int:
        """清除db数据
            Returns:
                int -- 是否成功
        """
        res = await self._con.flushdb()
        return res


class GenericCommandsMixin:
    async def delete(self, key, *keys):
        """
        删除key和它下面所有的依赖对象
        :param key:
        :param keys:
        :return:
        """
        res = await self._con.delete(key, *keys)
        return res

    async def exists(self, key, *keys):
        """
        检查key是否存在,可以判断列表,字符串等等,如果传入多个可以则返回对应存在的个数
        :param key:
        :param keys:
        :return:
        """
        res = await self._con.exists(key, *keys)
        return res

    async def expire(self, key, timeout):
        """
        设置key超时时间
        :param key:
        :param timeout:
        :return:
        """
        res = await self._con.expire(key, timeout)
        return res

    async def keys(self, pattern):
        """
        返回所有匹配模式的key
        """
        res = await self._con.keys(pattern)
        return res


class StringCommandsMixin:
    async def get(self, key):
        """
        获取key对应的value
        :param key:
        :return:
        """
        res = await self._con.get(key)
        return res

    async def set(self, key, value):
        """
        设置一组键值对
        :param key:
        :param value:
        :return:
        """
        res = await self._con.set(key, value)
        return res


class ListCommandsMixin:
    async def lpush(self, key, value, *values):
        """
        value全部加入到key对应的队列尾部
        :param key:
        :param value:
        :param values:
        :return:
        """
        res = await self._con.rpush(key, value, *values)
        return res

    async def lpop(self, key, number=1):
        """
        返回并删除列表前number个元素 ,number默认值为1
        :param key:
        :param number:
        :return:
        """
        if number == 1:
            res = [await self._con.lpop(key)]
        else:
            tr = self._con.multi_exec()
            tr.lrange(key, 0, number - 1)
            tr.ltrim(key, number, -1)
            res, res2 = await tr.execute()
        return res

    async def llen(self, key):
        """
        返回key中的存储长度,不存在的列表返回0
        :param key:
        :return:
        """
        res = await self._con.llen(key)
        return res

    async def lrem(self, key, value):
        """
        value删除
        :param key:
        :param value:
        :return:
        """
        res = await self._con.lrem(key, 0, value)
        return res

    async def lrange(self, key, start, end):
        """
        分片获取数据
        :param key:
        :param value:
        :return:
        """
        res = await self._con.lrange(key, start, end)
        return res


class SetCommandMixin:
    async def sadd(self, key, member, *members):
        """
        增加集合成员
        :param key:
        :param member:
        :param members:
        :return:
        """
        res = await self._con.sadd(key, member, *members)
        return res

    async def srem(self, key, member, *members):
        """
        删除集合成员
        :param key:
        :param member:
        :param members:
        :return:
        """
        res = await self._con.srem(key, member, *members)
        return res

    async def smembers(self, key):
        """
        获取所有成员
        :param key:
        :return:
        """
        res = await self._con.smembers(key)
        return res


class HashCommandMixin:

    async def hset(self, key, field, value, *pairs):
        """
        设置hash字段
        pairs长度必须是偶数
        """
        res = await self._con.hmset(key, field, value, *pairs)
        return res

    async def hget(self, key, field, *fields):
        """
        获取hash字段值
        """
        res = await self._con.hmget(key, field, *fields)
        return res

    async def hdel(self, key, field, *fields):
        """
        删除hash字段
        """
        res = await self._con.hdel(key, field, *fields)
        return res

    async def hgetall(self, key):
        """
        获取hash字段所有字段与值
        """
        res = await self._con.hgetall(key)
        return res

    async def hkeys(self, key):
        """
        获取hash字段所有字段
        """
        res = await self._con.hkeys(key)
        return res

    async def hvals(self, key):
        """
        获取hash字段所有值
        """
        res = await self._con.hvals(key)
        return res

    async def hlen(self, key):
        """
        获取hash字段长度
        """
        res = await self._con.hlen(key)
        return res

    async def hincrby(self, key, field, increment=1):
        return await self._con.hincrby(key, field, increment)


class SortedSetCommandMixin:

    async def zadd(self, key, score: (int, float), member, *pairs):
        """
        增加有序集一个或多个成员
        :param key:
        :param score:
        :param member:
        :param pairs: 长度必须是偶数,不然会报TypeError
        :return:
        """
        if len(pairs) % 2 != 0:
            raise TypeError("length of pairs must be even number")
        res = await self._con.zadd(key, score, member, *pairs)
        return res

    async def zlen(self, key):
        """
        返回key对应的有序集长度,无此有序集则为0
        :param key:
        :return:
        """
        res = await self._con.zcard(key)
        return res

    async def zrem(self, key, member, *members):
        return await self._con.zrem(key, member, *members)

    async def zrange(self, key, start=0, number=1, autodel=True, withscores=False):
        """
        返回有序集key前从start开始的number个成员,默认自动删除
        :param key:
        :param start:
        :param number:
        :param autodel:
        :param withscores: 是否返回score 默认False,如果为True则返回list(tuple(member,score))
        :return:
        """
        return await self._zrange2(key, start, number, autodel, withscores)
        # res = await self._con.zrange(key, start, number - 1, withscores)
        # if res and autodel:
        #     if withscores:
        #         await self._con.zrem(key, *map(lambda x: x[0], res))
        #     else:
        #         await self._con.zrem(key, *res)
        # return res

    async def _zrange2(self, key, start=0, number=1, autodel=True, withscores=False):
        """
        返回有序集key前从start开始的number个成员,默认自动删除
        :param key:
        :param start:
        :param number:
        :param autodel:
        :param withscores: 是否返回score 默认False,如果为True则返回list(tuple(member,score))
        :return:
        """
        tr = self._con.multi_exec()
        tr.zrange(key, start, number - 1, withscores)
        if autodel:
            tr.zremrangebyrank(key, start, number - 1)
        res, res2 = await tr.execute()
        return res

    async def zremrangebyscore(self, key, start, stop):
        """
        删除某个数值端内的值,包括 start stop
        :param key:
        :param start:
        :param stop:
        :return:
        """
        res = await self._con.zremrangebyscore(key, start, stop)
        return res

    async def zrangebyscore(self, key, start, stop, withscores=False, offset=None, count=None):
        """
        获取某个数值端内的值,包括 start stop
        :param key:
        :param start:
        :param stop:
        :return:
        """

        res = await self._con.zrangebyscore(key, start, stop, withscores, offset=offset, count=count)
        return res


class MemoryDB(ServerCommandsMixin, GenericCommandsMixin, StringCommandsMixin, ListCommandsMixin, SortedSetCommandMixin, SetCommandMixin, HashCommandMixin):
    """
        内存数据库封装
    """

    def __init__(self, sentinels: (list, tuple), db=0, master_name='mymaster', password='123456'):
        self.master_name = master_name
        self.sentinels = sentinels
        self.password = password
        self.db = db

    async def open(self):
        """
        打开数据库连接
        :return: None
        """
        self._sentinel = await aioredis.create_sentinel(
            self.sentinels, password=self.password, db=self.db)
        self._con = self._sentinel.master_for(
            self.master_name)

    async def close(self):
        """
        关闭数据库连接
        :return:None
        """
        self._sentinel.close()
        await self._sentinel.wait_closed()
