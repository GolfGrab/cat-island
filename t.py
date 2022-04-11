data1 = {"a": {"1": 1, "2": 2}, "b": {"2": 2, "3": 3}}
data2 = {"a": {"2": 2}, "b": {"3": 3}}

# data1- data2

ans = dict((k1, dict((k2, v2)
           for k2, v2 in v1.items() if k2 not in data2[k1]))if k1 in data2 else (k1, v1) for k1, v1 in data1.items() if k1 not in data2 or v1 != data2[k1])

print(ans)
