from types import SimpleNamespace
t = SimpleNamespace(foo='bar')
t.ham = 'spam'
print(t)
print(t.foo)


d = dict(x=[1, 2], y=['a', 'b'])
ns = SimpleNamespace(**d)
print(ns)
print(ns.x)
