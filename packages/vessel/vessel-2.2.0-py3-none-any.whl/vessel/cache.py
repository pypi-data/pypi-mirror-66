import pathing
import collections
import copy


__all__ = ('Tree', 'Cache', 'Entry', 'EntryCache', 'RowCache', 'BulkRowCache',
           'AlikeBulkRowCache')


class Tree(dict):

    """
    Simple :class:`BTree` implementation.
    """

    __slots__ = ()

    def _make(self):

        """
        Create a subtree; called with no arguments.
        """

        return ()

    def _crawl(self, keys, stop = True):

        """
        Reach the node corresponding to ``keys``.

        If set to not ``stop``, create subtrees.

        Yield are nodes along the path.
        """

        node = self
        keys = iter(keys)
        while True:
            yield node
            try:
                key = next(keys)
            except StopIteration:
                break
            try:
                node = node[key]
            except KeyError:
                if stop:
                    raise
                args = self._make()
                node[key] = node = self.__class__(*args)

    def select(self, keys):

        """
        Get the value corresponding to ``keys``.
        """

        (*trees, value) = self._crawl(keys)
        return value

    def create(self, keys, value):

        """
        Place a value at ``keys``, creating subtrees.
        """

        (*keys, key) = keys
        (*trees, tree) = self._crawl(keys, stop = False)
        tree[key] = value

    def _brush(self, keys):

        """
        Remove the final value and all empty subtrees along ``keys``.
        """

        trees = self._crawl(keys)
        pairs = tuple(zip(trees, keys))
        for (tree, key) in reversed(pairs):
            yield tree.pop(key)
            if tree:
                break

    def delete(self, keys):

        """
        Remove and return the value at ``keys``, deleting empty subtrees.
        """

        (value, *trees) = self._brush(keys)

        return value

    def switch(self, old, new):

        """
        Move the value at ``old`` to ``new``, deleting and creating subtrees.
        """

        node = Tree.delete(self, old)
        Tree.create(self, new, node)

        return node


class Cache(Tree):

    """
    Same as BTree, but declaring its expected depth allows for floor traversing.
    """

    __slots__ = ('_depth',)

    def __init__(self, depth):

        super().__init__()

        self._depth = depth

    def _make(self):

        depth = self._depth - 1

        return (depth,)

    def traverse(self):

        """
        Yield ``(keys, value)`` pairs.
        """

        yield from pathing.derive(self, min = self._depth, max = self._depth)

    def entries(self):

        """
        Yield all floor values.
        """

        for (keys, value) in self.traverse():

            yield value

    def __repr__(self):

        entries = tuple(self.entries())
        size = len(entries)

        return f'Cache({size})'


class Entry:

    """
    :class:`dict`\-like attribute-accessible and read-only representation of
    data.

    .. code-block:: py

        >>> entry = Entry({'name': 'Pup', 'age': 6})
        >>> entry.name
        'Pup'

    Overwite the ``__make__(data)`` for copying with different ``__init__``\s.
    """

    __slots__ = ('__data__',)

    def __init__(self, data = None, direct = False):

        self.__data__ = {} if data is None else data if direct else data.copy()

    def __getitem__(self, key):

        return self.__data__[key]

    def __getattr__(self, key):

        try:
            value = self[key]
        except KeyError as error:
            raise AttributeError(*error.args) from None

        return value

    def __copy__(self):

        data = self.__data__.copy()
        fake = self.__class__(data, True)

        return fake

    def __deepcopy__(self, memo):

        fake = copy.copy(self)
        data = fake.__data__
        for (key, value) in data.items():
            data[key] = copy.deepcopy(value)

        return fake

    def __repr__(self):

        items = '|'.join(f'{n}={v}' for (n, v) in self.__data__.items())
        return f'<{self.__class__.__name__}({items})>'


def _create(value):

    """
    Create or return an entry from the value.
    """

    return value if isinstance(value, Entry) else Entry(value)


def _modify(entry, data):

    """
    Modify an :class:`Entry` with the data.
    """

    entry.__data__.update(data)


class EntryCache(Cache):

    """
    Store, create and modify :class:`Entry` instances.
    """

    __slots__ = ('_manage',)

    _Asset = collections.namedtuple('Asset', 'create modify')

    def __init__(self, depth, create = _create, modify = _modify):

        super().__init__(depth)
        self._manage = self._Asset(create, modify)

    def _make(self, *args, **kwargs):

        args = super()._make()

        return (*args, self._manage.create, self._manage.modify)

    def create(self, keys, data):

        """
        Create and put an entry at ``keys``.
        """

        entry = self._manage.create(data)
        super().create(keys, entry)

        return entry

    def modify(self, keys, data):

        """
        Modify the entry at ``keys``\'s with ``data`` and return ``(old, new)``.
        """

        entry = Tree.select(self, keys)
        dummy = copy.deepcopy(entry)
        self._manage.modify(entry, data)

        return (dummy, entry)


class RowCache(EntryCache):

    """
    Like :class:`EntryCache`, but knowing primary allows for better handling.
    """

    __slots__ = ('_primary',)

    def __init__(self, primary):

        super().__init__(len(primary))

        self._primary = primary

    def _make(self):

        primary = self._primary[:1]

        return (primary,)

    def query(self, data):

        """
        Get all available values against the ``data``\'s primary keys.
        """

        store = []

        try:
            store.extend(data[key] for key in self._primary)
        except KeyError:
            pass

        return tuple(store)

    def create(self, data):

        """
        Create and put an entry in the spot designated by its primary keys.
        """

        keys = self.query(data)
        result = super().create(keys, data)

        return result

    def modify(self, keys, data):

        """
        Modify an entry and change its spot if necessary.
        """

        result = super().modify(keys, data)

        new = self.query(data)
        size = len(new)
        old = keys[:size]
        if not tuple(old) == new:
            super().switch(old, new)

        return result


class BulkRowCache(RowCache):

    """
    Like :class:`RowCache`, but data inputs should be arrays of data.
    """

    __slots__ = ()

    def create(self, data):

        """
        Create and retur all entries.
        """

        results = []
        for data in data:
            result = super().create(data)
            results.append(result)

        return tuple(results)

    @classmethod
    def _flat(cls, node):

        """
        Turn the node into either a tree's entries or a single-item array.
        """

        return tuple(node.entries) if isinstance(node, cls) else (node,)

    def modify(self, keys, data):

        """
        Modify all entries at ``keys`` and change their spot if necessary.

        The keys don't need to be a full path to specific entries.

        For example, if two entries exists at ``(0, 1, 2)`` and ``(0, 1, 4)``,
        then updating at ``(0, 1)`` would require ``data`` to be a two-item
        array, with each meant to modify its respective entry in order.
        """

        node = super().select(keys)
        depth = self._depth - len(keys)

        if depth == 0:
            keys = (keys,)
        else:
            items = pathing.derive(node, max = depth, min = depth)
            (subkeys, _entries) = zip(*items)

        results = []
        for (subkeys, data) in zip(subkeys, data):
            curkeys = (*keys, *subkeys)
            result = super().modify(curkeys, data)
            results.append(result)

        return results


class AlikeBulkRowCache(BulkRowCache):

    """
    Same as :class:`BulkRowCache`, but:
        - Active methods accept ``(keys, data)``.
        - Methods always return an array of entries.
    """

    __slots__ = ()

    @classmethod
    def _flat(cls, node):

        return tuple(node.entries()) if isinstance(node, cls) else (node,)

    def select(self, keys):

        """
        Same as :meth:`BulkRowCache.select`, except it always returns
        """

        node = super().select(keys)
        result = self._flat(node)

        return result

    def create(self, keys, data):

        """
        ``data`` is used, ``keys`` is not.

        Refer to :meth:`BulkRowCache.create`.
        """

        result = super().create(data)

        return result

    def modify(self, keys, data):

        """
        ``data`` and ``keys`` are used.

        Refer to :meth:`BulkRowCache.modify`.
        """

        result = super().modify(keys, data)

        return result

    def delete(self, keys, data):

        """
        ``keys`` is used, ``data`` is not.

        Refer to :meth:`BulkRowCache.delete`.
        """

        node = super().delete(keys)
        result = self._flat(node)

        return result
