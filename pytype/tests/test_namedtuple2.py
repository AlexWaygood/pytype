"""Tests for the namedtuple implementation in collections_overlay.py."""

from pytype.tests import test_base


class NamedtupleTests(test_base.BaseTest):
  """Tests for collections.namedtuple."""

  def test_namedtuple_match(self):
    self.Check("""
        import collections
        from typing import Any, Dict

        X = collections.namedtuple("X", ["a"])

        def GetRefillSeekerRanks() -> Dict[str, X]:
          return {"hello": X(__any_object__)}
        """)

  def test_namedtuple_different_name(self):
    with self.DepTree([("foo.py", """
      import collections
      X1 = collections.namedtuple("X", ["a", "b"])
      X2 = collections.namedtuple("X", ["c", "d"])
    """)]):
      self.Check("""
        import foo
        def f() -> foo.X2:
          return foo.X2(0, 0)
      """)


class NamedtupleTestsPy3(test_base.BaseTest):
  """Tests for collections.namedtuple in Python 3."""

  def test_bad_call(self):
    """The last two arguments are kwonly in 3.6."""
    self.InferWithErrors("""
        import collections
        collections.namedtuple()  # missing-parameter
        collections.namedtuple("_")  # missing-parameter
        collections.namedtuple("_", "", True)  # wrong-arg-count
        collections.namedtuple("_", "", True, True)  # wrong-arg-count
        collections.namedtuple("_", "", True, True, True)  # wrong-arg-count
    """)

  def test_nested_namedtuple(self):
    self.Check("""
      from typing import NamedTuple
      class Bar:
        class Foo(NamedTuple):
          x: int
        foo = Foo(x=0)
    """)

  def test_namedtuple_defaults(self):
    self.Check("""
      import collections
      X = collections.namedtuple('X', ['a', 'b'], defaults=[0])
      X('a')
      X('a', 'b')
    """)


if __name__ == "__main__":
  test_base.main()
