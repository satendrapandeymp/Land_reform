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
    col_sum = [0 for k in range(y)]
    temp = []    
    for j in range(x):
        for i in range(y):
            flag = randint(1,2)
            if flag == 1 or ( i ==y-1 and sum(temp) == 0):
                temp.append(randint(1,8))
                col_sum[i] += temp[i] 
            else:
                temp.append(0)
        row_sum.append(sum(temp))
        arr.append(temp)
        temp = []
    return arr, row_sum, col_sum

num = 30
sector = 10
temp = []
result = []

while(True):
    print "Trying to generate random number"
    arr, row_sum, col_sum = generator(num-1,sector)
    if max(col_sum,"", sector) <= 76:
        for i in range(sector):
            temp.append(76-col_sum[i])
        arr.append(temp)
        row_sum.append(sum(temp))
        break

File_name = "Data.csv"
f = open(File_name, "w")
for wp in arr:
    for wpn in wp:
        f.write(str(wpn) + ",")  
    f.write("\n")  
f.close()
    
    
col_sum = [76 for t in range(sector)]

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
        temp = {'owner':owner, 'sector':pos, 'amount':row[pos]}
        row[pos] = 0
        result.append(temp)
        
    owner += 1

# Now index sector wise
index = [0 for t in range(sector+1)]
index_detail = [[] for t in range(sector+1)]
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
    _, pos = max(index, 'n', sector)
    if pos == sector:
        break
    index[pos] = 0
    
    temp = index_detail[pos]
    
    for i in range(len(temp)):  
        # cross matching case
        count = 0
        for owner in residue:
            if owner['amount'] == col_sum[pos]:
                    print "You got a cross fit here"
                    res = {'owner':owner['owner'], 'sector':pos, 'amount':owner['amount']}
                    result.append(res)            
                    col_sum[pos] -= owner['amount']
                    residue.remove(residue[count])
                    break
            count += 1
        
        amount = 200
        check = 0
        count = 0        
        for owner in temp:
            if owner['amount'] < amount:
                amount = owner['amount']
                check = count
            count += 1
            
        amount = row_sum[temp[check]['owner']]
        
        if col_sum[pos] >= amount + 10:
            
            temp[check]['amount'] = 1000
            
            # checking for perfect fit
            
            opt = -1
            for k in checked:
                if col_sum[k] == amount:
                    opt = k
                    break
            
            if opt == -1:
                res = {'owner':temp[check]['owner'], 'sector':pos, 'amount':amount}
                result.append(res)            
                col_sum[pos] -= amount
            else:
                print "You got a fit here"
                res = {'owner':temp[check]['owner'], 'sector':opt, 'amount':amount}
                result.append(res)            
                col_sum[opt] -= amount
                
        else:
            for owner in temp:
                if owner['amount'] != 1000:
                    residue.append(owner)            
            break
    checked.append(pos)
    
# final steps
# removing perfect fit from resude

count = 0
flag = -1
print residue, col_sum
for temp in residue:
    for k in range(sector):
        if temp['amount'] == col_sum[k]:
            flag = count
            col_sum[k] = 0
            print "You got lucky here dude"
            break
    if flag != -1:
        flag = -1
        residue.remove(residue[count])
    count += 1


# Now we just have to take care of a few pwople
# Will take care of this part tomorrow
col_sum_final = []
count = 0
for final in col_sum:
    temp = {"sector":count, "amount":final}
    col_sum_final.append(temp)
    count += 1
    
col_sum_final = sorted(col_sum_final, key=lambda left:left['amount'])
residue = sorted(residue, key=lambda left: left['amount'])


print col_sum, residue

flag = 0
for i in range(len(residue)):
    amount = residue[i-1]['amount']
    id = residue[i-1]['owner']
    av_amount = col_sum_final[-1]['amount']
    sectors = col_sum_final[-1]['sector']    
    if flag == 0:
        flag = 1
        if amount/3 > col_sum_final[0]['amount'] and amount/3 < col_sum_final[-1]['amount']:
            for k in range(sector):
                if col_sum_final[k]['amount'] > amount/3:
                    break
                
            if k != sector-1:
                if col_sum_final[-1]['amount'] - amount +  col_sum_final[k]['amount']  + col_sum_final[k-1]['amount'] < 0:
                    k += 1
            
                result.append({"owner":id, "amount":amount - col_sum_final[k]['amount'] - col_sum_final[k-1]['amount'] , "sector":sectors})
                result.append({"owner":id, "amount":col_sum_final[k]['amount'], "sector":col_sum_final[k]['sector']})
                result.append({"owner":id, "amount":col_sum_final[k-1]['amount'], "sector":col_sum_final[k-1]['sector']})
                residue[i-1]['amount'] = 0
                col_sum_final[-1]['amount'] -= amount -  col_sum_final[k]['amount']  - col_sum_final[k-1]['amount']  
                col_sum_final[k]['amount'] = 0
                col_sum_final[k-1]['amount'] = 0       
                
            else:
                
                result.append({"owner":id, "amount":amount - col_sum_final[k-1]['amount'] - col_sum_final[k-2]['amount'] , "sector":sectors})
                result.append({"owner":id, "amount":col_sum_final[k-1]['amount'], "sector":col_sum_final[k-1]['sector']})
                result.append({"owner":id, "amount":col_sum_final[k-2]['amount'], "sector":col_sum_final[k-2]['sector']})
                residue[i-1]['amount'] = 0
                col_sum_final[-1]['amount'] -= amount -  col_sum_final[k-2]['amount']  - col_sum_final[k-1]['amount']  
                col_sum_final[k-2]['amount'] = 0
                col_sum_final[k-1]['amount'] = 0                 
                    
        elif amount/2 > col_sum_final[0]['amount'] and amount/2 < col_sum_final[-1]['amount']:
            for k in range(sector):
                if col_sum_final[k]['amount'] > amount/2:
                    break
            
            if k == sector-1:
                k -=1
            
            result.append({"owner":id, "amount":amount - col_sum_final[k]['amount'], "sector":sectors})
            result.append({"owner":id, "amount":col_sum_final[k]['amount'], "sector":col_sum_final[k]['sector']})
            col_sum_final[-1]['amount'] -= amount -  col_sum_final[k]['amount']  
            residue[i-1]['amount'] = 0
            col_sum_final[k]['amount'] = 0            
            
        else:
            print 'lol lol'
            
    else:
        
        if av_amount >= amount:
            result.append({"owner":id, "amount":amount, "sector":sectors})
            residue[i-1]['amount'] = 0
            col_sum_final[-1]['amount'] -= amount
            
        elif av_amount + col_sum_final[-2]['amount'] >= amount:
            result.append({"owner":id, "amount":amount - col_sum_final[-2]['amount'], "sector":sectors})
            result.append({"owner":id, "amount":col_sum_final[-2]['amount'], "sector":col_sum_final[-2]['sector']})
            residue[i-1]['amount'] = 0
            col_sum_final[-1]['amount'] -= amount -  col_sum_final[-2]['amount']
            col_sum_final[-2]['amount'] = 0
        else:
            print 'lola'
        
    col_sum_final = sorted(col_sum_final, key=lambda left:left['amount'])

print residue, col_sum_final

result = sorted(result, key=lambda left:left['owner'])
sol = []
count = 0

for i in range(num):
    final = [ 0 for j in range(sector) ]
    if result[count]['owner'] == i:
        final[result[count]['sector']] = result[count]['amount']
        count += 1
    try:
        if result[count]['owner'] == i:
            final[result[count]['sector']] = result[count]['amount']
            count += 1    
        if result[count]['owner'] == i:
            final[result[count]['sector']] = result[count]['amount']
            count += 1
    except:
        a = 1
        
    sol.append(final)
    
    
File_name = "Data1.csv"
f = open(File_name, "w")
for wp in sol:
    for wpn in wp:
        f.write(str(wpn) + ",")  
    f.write("\n")  
f.close()