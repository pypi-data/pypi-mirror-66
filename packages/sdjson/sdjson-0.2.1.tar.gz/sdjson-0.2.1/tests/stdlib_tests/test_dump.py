# stdlib
from io import StringIO

# 3rd party
import pytest

# this package
import sdjson


def test_dump():
	sio = StringIO()
	sdjson.json.dump({}, sio)
	assert sio.getvalue() == '{}'


def test_dumps():
	assert sdjson.dumps({}) == '{}'


def test_dump_skipkeys():
	v = {b'invalid_key': False, 'valid_key': True}
	with pytest.raises(TypeError):
		sdjson.json.dumps(v)
	
	s = sdjson.json.dumps(v, skipkeys=True)
	o = sdjson.json.loads(s)
	assert 'valid_key' in o
	assert b'invalid_key' not in o


def test_encode_truefalse():
	assert sdjson.dumps(
			{True: False, False: True}, sort_keys=True) == \
		   '{"false": true, "true": false}'
	assert sdjson.dumps(
			{2: 3.0, 4.0: 5, False: 1, 6: True}, sort_keys=True) == \
		   '{"false": 1, "2": 3.0, "4.0": 5, "6": true}'


# Issue 16228: Crash on encoding resized list
def test_encode_mutated():
	a = [object()] * 10
	
	def crasher(obj):
		del a[-1]
	
	assert sdjson.dumps(a, default=crasher) == \
		   '[null, null, null, null, null]'


# Issue 24094
def test_encode_evil_dict():
	class D(dict):
		def keys(self):
			return L
	
	class X:
		def __hash__(self):
			del L[0]
			return 1337
		
		def __lt__(self, o):
			return 0
	
	L = [X() for i in range(1122)]
	d = D()
	d[1337] = "true.dat"
	assert sdjson.dumps(d, sort_keys=True) == '{"1337": "true.dat"}'
