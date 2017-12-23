import numpy as np
from random import randint, uniform

def sum(arr):
    sum = 0
    for t in arr:
        sum += t
    return sum

def max(arr, flag, sector):
    max = 0
    count = -1
    temp = sector
    for t in arr:
        count += 1
        if t>max:
            temp = count
            max = t
    if flag == "n":
        return max, temp
    return max

def generator(x,y):
    arr = []
    row_sum = []
    col_sum = [0,0,0,0]
    temp = []    
    for j in range(x):
        for i in range(y):
            flag = randint(1,2)
            if flag == 1 or ( i ==3 and sum(temp) == 0):
                temp.append(randint(1,10))
                col_sum[i] += temp[i] 
            else:
                temp.append(0)
        row_sum.append(sum(temp))
        arr.append(temp)
        temp = []
    return arr, row_sum, col_sum

num = 35
sector = 4
temp = []
result = []
while(True):
    arr, row_sum, col_sum = generator(num-1,sector)
    if max(col_sum,"", sector) <= 76:
        for i in range(sector):
            temp.append(76-col_sum[i])
        arr.append(temp)
        row_sum.append(sum(temp))
        break
    
col_sum = [76,76,76,76]

# removing owners who have land just in one section
owner = 0
for row in arr:
    pos = 0
    count = 0
    for i in range(sector):
        if row[i] != 0:
            count +=1
            pos = i
    if count == 1:
        col_sum[pos] -= row[pos] 
        row_sum[owner] = 0
        temp = {'owner':owner, 'sector':pos, 'Amount':row[pos]}
        row[pos] = 0
        result.append(temp)
        
    owner += 1

# Now index sector wise
index = [0,0,0,0,0]
index_detail = [[],[],[],[],[]]
for i in range(num):
    test, check = max(arr[i], 'n', sector)
    index[check] += 1
    index_detail[check].append({'owner':i, 'amount':row_sum[i]})

index.pop()
index_detail.pop()

# Coming back to solving the problem
# solving the sector with maximum indexing

residue = []
checked = []

while(True):
    print col_sum, residue
    _, pos = max(index, 'n', sector)
    if pos == sector:
        break
    index[pos] = 0
    
    temp = index_detail[pos]
    
    for i in range(len(temp)):  
        amount = 200
        check = 0
        count = 0
        for owner in temp:
            if owner['amount'] < amount:
                amount = owner['amount']
                check = count
            count += 1
            
        amount = row_sum[temp[check]['owner']]
        print amount, col_sum, pos, row_sum
        
        if col_sum[pos] >= amount:
            
            temp[check]['amount'] = 1000
            
            # checking for perfect fit
            
            opt = -1
            for k in checked:
                if col_sum[k] == amount:
                    opt = k
                    break
            
            if opt == -1:
                res = {'owner':temp[check]['owner'], 'sector':pos, 'Amount':amount}
                result.append(res)            
                col_sum[pos] -= amount
            else:
                print "You got a fit here"
                res = {'owner':temp[check]['owner'], 'sector':opt, 'Amount':amount}
                result.append(res)            
                col_sum[opt] -= amount
                
        else:
            for owner in temp:
                if owner['amount'] != 1000:
                    residue.append(owner)            
            break
    checked.append(pos)
    
# final steps
# Now we just have to take care of a few pwople
# Will take care of this part tomorrow
for temp in residue:
    print temp['amount']