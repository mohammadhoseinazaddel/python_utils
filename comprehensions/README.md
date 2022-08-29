```python
t=[[1,2,3],["a","b"],[1,2,3,4,5]]

j = [l for i in t if len(i) > 2 for l in i ]

j = [l for i in t if len(i) > 2 for l in i  if len(i) > 4 ]

print(j)
```


list extend

```python
t = [1,2,3,4,5]
j=[7,8,9,0]
temp=("jj","gGG")
t.extend(f for f in j if f==8)
t.extend("mohsen")
t.extend(temp)
print(t)
```
