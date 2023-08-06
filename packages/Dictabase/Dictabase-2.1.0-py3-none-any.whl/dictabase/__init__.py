import json

import dataset
import sys

DEBUG = False

oldPrint = print
if DEBUG is False:
    print = lambda *a, **k: None


def RegisterDBURI(dburi=None):
    global _DB
    global _DBURI
    if dburi is None:
        if sys.platform.startswith('win'):
            dburi = 'sqlite:///MyDatabase.db'
        else:  # linux
            dburi = 'sqlite:////MyDatabase.db'

    _DBURI = dburi
    _DB = dataset.connect(dburi)
    print('_DB=', _DB)


class BaseTable(dict):
    def __init__(self, *a, **k):
        for key, value in k.items():
            if isinstance(value, bytes):
                raise TypeError('Dont pass bytes-type, instead use b''.decode()')

        self._initComplete = False
        super().__init__(*a, **k)
        self._insideUpsert = False
        self._initComplete = True

    def __setitem__(self, key, value):
        '''
        Any time a value is set to this newObj, the change will be updated in the database
        :param key:
        :param value:
        :return:
        '''
        print('__setitem__', key, value)

        try:
            value = json.dumps(value)
            print('48 __setitem__', key, value)
        except Exception as e:
            print('__setitem__ Exception:', e)

        super().__setitem__(key, value)
        if self._initComplete and not key.startswith('_'):
            _Upsert(self)  # save changes to DB

    def __getitem__(self, key):
        print('__getitem__(', key)
        value = super().__getitem__(key)
        try:
            value = json.loads(value)
            print('60 value=', value)
        except Exception as e:
            print('__getitem__ Exception:', e)
        return value

    def get(self, *a, **k):
        print('get(', *a, **k)
        value = super().get(*a, **k)
        try:
            value = json.loads(value)
            print('70 value=', value)
        except Exception as e:
            print('get Exception:', e)
        return value

    def items(self, *a, **k):
        print('items(', *a, **k)
        for key, value in super().items(*a, **k):
            if not self._insideUpsert:
                try:
                    value = json.loads(value)
                    print('70 value=', value, 'type=', type(value))
                except Exception as e:
                    print('items Exception:', e)
            yield key, value

    def __str__(self):
        '''

        :return: string like '<BaseDictabaseTable: email=me@website.com, name=John>'
        '''
        itemsList = []
        for k, v, in self.items():
            if isinstance(v, str) and len(v) > 25:
                v = v[:25]
            itemsList.append(('{}={}(type={})'.format(k, v, type(v).__name__)))
        if DEBUG:
            itemsList.append(('_insideUpsert={}'.format(self._insideUpsert)))

        return '<{}: {}>'.format(
            type(self).__name__,
            ', '.join(itemsList)
        )

    def __repr__(self):
        return str(self)


def New(cls, **k):
    '''
    Creates a new row in the table(cls)
    Returns the new dict-like object

    cls should inherit from BaseTable
    '''
    # print('New(cls=', cls, ', k=', k)
    newObj = cls(**k)

    tableName = cls.__name__
    _DB.begin()
    ID = _DB[tableName].insert(newObj)
    _DB.commit()

    newObj.update({'id': ID})
    return newObj


def _Upsert(obj):
    print('_Upsert(obj=', obj)
    obj._insideUpsert = True
    tableName = type(obj).__name__
    _DB.begin()
    _DB[tableName].upsert(obj, ['id'])  # find row with matching 'id' and update it
    _DB.commit()
    obj._insideUpsert = False
    print('_Upsert end')


def FindOne(cls, **k):
    # _DB.begin() # dont do this
    print('_DB.tables=', _DB.tables)
    dbName = cls.__name__
    tbl = _DB[dbName]
    ret = tbl.find_one(**k)
    print('FindOne ret=', ret)

    if ret:

        return cls(ret)
    else:
        return None


def FindAll(cls, **k):
    # special kwargs
    reverse = k.pop('_reverse', False)  # bool
    orderBy = k.pop('_orderBy', None)  # str
    if reverse is True:
        if orderBy is not None:
            orderBy = '-' + orderBy
        else:
            orderBy = '-id'

    # do look up
    dbName = cls.__name__
    if len(k) is 0:
        ret = _DB[dbName].all(order_by=[f'{orderBy}'])
    else:
        if orderBy is not None:
            ret = _DB[dbName].find(order_by=['{}'.format(orderBy)], **k)
        else:
            ret = _DB[dbName].find(**k)

    # yield type-cast items one by one
    for item in ret:
        yield cls(item)


def Drop(cls, confirm=False):
    global _DB
    if confirm:
        _DB.begin()
        tableName = cls.__name__
        _DB[tableName].drop()
        _DB.commit()

        _DB = dataset.connect(_DBURI)
    else:
        raise Exception('Cannot drop unless you pass confirm=True as kwarg')


def Delete(obj):
    _DB.begin()
    dbName = type(obj).__name__
    _DB[dbName].delete(**obj)
    _DB.commit()


if __name__ == '__main__':
    import time
    import random

    RegisterDBURI(
        # 'postgres://xfgkxpzruxledr:5b83aece4fbad7827cb1d9df48bf5b9c9ad2b33538662308a9ef1d8701bfda4b@ec2-35-174-88-65.compute-1.amazonaws.com:5432/d8832su8tgbh82'
        None,  # use default sqllite
    )


    def TestA():
        class A(BaseTable):
            pass

        Drop(A, confirm=True)

        for i in range(10):
            New(A, time=time.asctime(), count=i)

        oldPrint('FindAll(A)=', list(FindAll(A)))
        oldPrint('FindOne(A, count=5)=', FindOne(A, count=5))

        for item in FindAll(A):
            item['count'] += 10

        oldPrint('FindAll(A)=', list(FindAll(A)))

        for i in range(0, 10, 2):
            obj = FindOne(A, count=i + 10)
            if obj:
                Delete(obj)

        oldPrint('FindAll(A)=', list(FindAll(A)))


    def TestBytes():
        # test bytes type
        class B(BaseTable):
            pass

        Drop(B, confirm=True)

        d = ('0' * 100).encode()
        try:
            large = New(B, data=d)

        except Exception as e:
            oldPrint(e)
        large = New(B, data=d.decode())
        oldPrint("large['data'] == d is", large['data'] == d)

        largeID = large['id']

        findLarge = FindOne(B, id=largeID)
        oldPrint("findLarge['data'] == d is", findLarge['data'].encode() == d)


    def TestTypes():

        class Person(BaseTable):
            # Each subclass of BaseTable produces another table in the db
            pass

        class Animal(BaseTable):
            pass

        # For testing, delete all tables first
        # Comment these out to make data persistant
        Drop(Person, confirm=True)
        Drop(Animal, confirm=True)

        # Create tables with random data
        for i in range(10):
            # Instantiating a new Person newObj adds a new row in the db
            newPerson = New(Person,
                            name='Name{}'.format(i),
                            age=random.randint(1, 100),
                            )
            oldPrint('newPerson=', newPerson)

            newAnimal = New(Animal,
                            kind=random.choice(['Cat', 'Dog']),
                            name='Fluffy{}'.format(i),
                            age=random.randint(1, 10),
                            )
            oldPrint('newAnimal=', newAnimal)

        # FindAll() returns all items from the database that match
        # you can also use keywords like '_limit', '_reverse', '_orderBy'
        oldPrint('Number of animals of age 5: {}'.format(
            len(list(FindAll(Animal, age=5))))
        )

        # FindOne() returns an newObj found in the database
        person5 = FindOne(Person, name='Name5')
        oldPrint('Age of Person5=', person5['age'])

        # Remove any animals with age >= 5
        for animal in FindAll(Animal):
            if animal['age'] >= 5:
                oldPrint('Removing animal=', animal)
                Delete(animal)

        oldPrint('Remaining Animals=', FindAll(Animal))

        # Test Relational Mapping

        class Book(BaseTable):
            pass

        class Page(BaseTable):
            pass

        Drop(Book, confirm=True)
        Drop(Page, confirm=True)

        book = Book(title='Title')
        page1 = Page(words='Words1')
        page2 = Page(words='Words2')

        oldPrint('77 book=', book)
        oldPrint('78 page1=', page1)
        oldPrint('79 page2=', page2)

        book['pages'] = [page1, page2]
        page1['book'] = book
        page2['book'] = book

        oldPrint('book["pages"]=', book['pages'])
        oldPrint('page1["book"]=', page1['book'])
        oldPrint('page2["book"]=', page2['book'])


    def TestList():
        class TestListTable(BaseTable):
            pass

        Drop(TestListTable, confirm=True)
        item = New(TestListTable)
        item['list'] = [1, 2, 3]

        findItem = FindOne(TestListTable)
        oldPrint('findItem=', findItem)

        for k, v in findItem.items():
            oldPrint(327, k, '=', v, 'type=', type(v))
            if k == 'list':
                if not isinstance(v, list):
                    raise TypeError('Should be type list')

        for k in findItem:
            v = findItem.get(k)
            oldPrint(319, k, '=', v, 'type=', type(v))
            if k == 'list':
                if not isinstance(v, list):
                    raise TypeError('Should be type list')

        for k in findItem:
            v = findItem[k]
            oldPrint(325, k, '=', v, 'type=', type(v))
            if k == 'list':
                if not isinstance(v, list):
                    raise TypeError('Should be type list')


    def TestNew():
        class Thingamajig(BaseTable):
            pass

        obj = New(Thingamajig, key1='value1')
        if 'id' not in obj:
            raise Exception('Should have returned a new ID')
        oldPrint('New Thingamajig=', obj)

    def TestDict():
        class TestDictTable(BaseTable):
            pass

        Drop(TestDictTable, confirm=True)
        item = New(TestDictTable)
        item['dict'] = {1: 'one', '2':'two', 'three':3, 'four': '4'}

        findItem = FindOne(TestDictTable, id=item['id'])
        oldPrint('findItem=', findItem)

        for k, v in findItem.items():
            oldPrint(327, k, '=', v, 'type=', type(v))
            if k == 'dict':
                if not isinstance(v, dict):
                    raise TypeError('Should be type dict')

        for k in findItem:
            v = findItem.get(k)
            oldPrint(319, k, '=', v, 'type=', type(v))
            if k == 'dict':
                if not isinstance(v, dict):
                    raise TypeError('Should be type dict')

        for k in findItem:
            v = findItem[k]
            oldPrint(325, k, '=', v, 'type=', type(v))
            if k == 'dict':
                if not isinstance(v, dict):
                    raise TypeError('Should be type dict')
    #################
    # TestA()
    # TestBytes()
    # TestTypes()
    # TestList()
    # TestNew()
    TestDict()
