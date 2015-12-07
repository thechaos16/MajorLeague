import os,sys
import math

## step one:
## same length, dic
## MSE
def MSE(a,b):
    ans = []
    for i in range(len(a[0])):
        ans.append(0.0)
    for i in range(len(a)):
        for j in range(len(a[i])):
            diff = a[i][j]-b[i][j]
            ans[j]+=diff*diff
    ans = map(lambda x:x/len(a),ans)
    return ans

## 

