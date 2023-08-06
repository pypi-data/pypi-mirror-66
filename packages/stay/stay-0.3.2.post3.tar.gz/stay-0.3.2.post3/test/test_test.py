from pytest import mark, fixture

class Decoder:
	def __call__(self, x):
		return x ** 2


@fixture
def decode():
    return Decoder()


def test_a(decode):
	assert decode(3) == 9