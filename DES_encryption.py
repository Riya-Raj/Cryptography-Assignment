intial_permutation_table = [58, 50, 42, 34, 26, 18, 10, 2,
  60, 52, 44, 36, 28, 20, 12, 4,
  62, 54, 46, 38, 30, 22, 14, 6,
  64, 56, 48, 40, 32, 24, 16, 8,
  57, 49, 41, 33, 25, 17, 9, 1,
  59, 51, 43, 35, 27, 19, 11, 3,
  61, 53, 45, 37, 29, 21, 13, 5,
  63, 55, 47, 39, 31, 23, 15, 7]

pc1 = [ 57, 49, 41, 33, 25, 17, 9,
   1, 58, 50, 42, 34, 26, 18,
  10, 2, 59, 51, 43, 35, 27,
  19, 11, 3, 60, 52, 44, 36,
  63, 55, 47, 39, 31, 23, 15,
   7, 62, 54, 46, 38, 30, 22,
  14, 6, 61, 53, 45, 37, 29,
  21, 13, 5, 28, 20, 12, 4 ]

shift_table = [1, 1, 2, 2,
  2, 2, 2, 2,
  1, 2, 2, 2,
  2, 2, 2, 1]

pc2 = [14, 17, 11, 24, 1, 5,
   3, 28, 15, 6, 21, 10,
  23, 19, 12, 4, 26, 8,
  16, 7, 27, 20, 13, 2,
  41, 52, 31, 37, 47, 55,
  30, 40, 51, 45, 33, 48,
  44, 49, 39, 56, 34, 53,
  46, 42, 50, 36, 29, 32]

ip_inverse = [40, 8, 48, 16, 56, 24, 64, 32,
  39, 7, 47, 15, 55, 23, 63, 31,
  38, 6, 46, 14, 54, 22, 62, 30,
  37, 5, 45, 13, 53, 21, 61, 29,
  36, 4, 44, 12, 52, 20, 60, 28,
  35, 3, 43, 11, 51, 19, 59, 27,
  34, 2, 42, 10, 50, 18, 58, 26,
  33, 1, 41, 9, 49, 17, 57, 25]





def inputMessageAndKey(m):

    lst=[]
    lst[:0]=m
    lst2=[]
    for i in lst:
      lst2.append("{0:04b}".format(int(i, 16)))

    pt=''
    for ele in lst2:
      pt+=ele

    #k = '133457799BBCDFF1'
    key = '0001001100110100010101110111100110011011101111001101111111110001'

    return pt,key

### Can be used for all the rearrangements ###
def rearrange_data(reorder_table, data):
    reordered_m = ''
    for i in range(len(reorder_table)):
        reordered_m += data[reorder_table[i]-1]

    return reordered_m

def left_shift(shift_table, kplus):
    kc, kd = kplus[:len(kplus)//2], kplus[len(kplus)//2:]
    cn_dn = []
    cd0 = []
    cd0.append(kc)
    cd0.append(kd)
    cn_dn.append(cd0)
    for i in range(len(shift_table)):
        temp = []
        for j in range(len(cn_dn[0])):
            partone = cn_dn[i][j][0:shift_table[i]]
            partwo = cn_dn[i][j][shift_table[i]:]
            comb = partwo + partone
            temp.append(comb)
        cn_dn.append(temp)
    cn_dn.pop(0)
    return cn_dn

#subkeys generation
def subkeysGeneration(pc2,cndn):
    subkeys = []
    for i in range(len(cndn)):
        ki = cndn[i][0]+cndn[i][1]
        ki_p = rearrange_data(pc2, ki)
        subkeys.append(ki_p)

    return subkeys

##defining the funtion F in the relation : Ri = Li-1 + F(Ri-1,Ki)

def function_F(R,K):
  a1 = expansion(R)
  #print("len = ",len(a1))
  a2 = xor(a1,K)
  #print("a2=",a2,"len =",len(a2))
  a3 = substitution(a2)
  final = permutation_F(a3)
  return final

##Expansion of Ri-1 from 32 to 48 bits, both and input and output are in the form of strings

def expansion(R):
  expansion_dbox = [32, 1, 2, 3, 4, 5,
                    4, 5, 6, 7, 8, 9,
                    8, 9, 10, 11, 12, 13,
                    12, 13, 14, 15, 16, 17,
                    16, 17, 18, 19, 20, 21,
                    20, 21, 22, 23, 24, 25,
                    24, 25, 26, 27, 28, 29,
                    28, 29, 30, 31, 32, 1]
  lst=[]
  lst[:0]=R
  #print(lst)
  ans_list = [None]*48
  for i in range(len(ans_list)):
    #print(expansion_dbox[i])
    ans_list[i] = lst[(expansion_dbox[i])-1]
  ans = ""
  for ele in ans_list:
      ans += ele
  return ans


##To substitute the result of the XOR of expanded Ri-1 and Ki from 48 bits to 32 bits
##Input and output are in the form of strings

def substitution(SB):
  s_boxes = [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
   	0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
      4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
    	15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],

   [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
    	3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
      0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
     13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],

   [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
     13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
     13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
   	1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],

   [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
    13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
    10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
     3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],

   [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
    14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
     4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
    11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],

   [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
     10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
      9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
      4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],


  [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
   13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
    1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
    6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],

 [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
    1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
    7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
    2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]


  group_list = [(SB[i:i+6]) for i in range(0, len(SB), 6)]
  count=0
  str=''
  for i in group_list:
    row = i[0] + i[5]
    col = i[1] + i[2] + i[3] + i[4]
    #print(row)
    #print(col)
    row_int = int('0b'+row,2) + 1
    col_int = int('0b'+col,2) + 1
    #print(row_int)
    #print(col_int)
    pos = 16*(row_int-1) + col_int
    #print(pos)
    each_box = s_boxes[count]
    ans = each_box[pos-1]
    #print(ans)
    count=count+1
    x=bin(ans).replace("0b", "")
    zero_filled=x.zfill(4)
    str=str+zero_filled
    each_box.clear()
  return str

##permutation performed after substitution, input and output are in the form of strings

def permutation_F(P):
  straight_perm_table = [16, 7, 20, 21,
  29, 12, 28, 17,
   1, 15, 23, 26,
   5, 18, 31, 10,
   2, 8, 24, 14,
  32, 27, 3, 9,
  19, 13, 30, 6,
  22, 11, 4, 25]

  lst=[]
  lst[:0]=P
  #print(lst)
  ans_list = [None]*32
  for i in range(len(ans_list)):
    #print(expansion_dbox[i])
    ans_list[i] = lst[(straight_perm_table[i])-1]
  ans = ""
  for ele in ans_list:
      ans += ele
  return ans

def xor(a, b):
    ans = ""
    for i in range(len(a)):
        if (a[i] == b[i]):
            ans += "0"
        else:
            ans += "1"
    return ans


def EncryptingTheData(subkeys,ip):
    lm0, rm0 = ip[:len(ip)//2], ip[len(ip)//2:]
    for i in range(16):
        lm1 = rm0
        p = function_F(rm0,subkeys[i])
        rmn1 = xor(lm0,p)
        lm0 = lm1
        rm0 = rmn1
    #print(lm0,rm0)
    semifinal = rm0+lm0
    final = rearrange_data(ip_inverse, semifinal)
    final_divided = [(final[i:i+4]) for i in range(0, len(final), 4)]
    lst3=[]
    lst4=[]
    for i in final_divided:
      lst3.append(hex(int(i,2)))

    for j in lst3:
      lst4.append(j[2])

    final_hex=''

    for ele in lst4:
      final_hex+=ele

    #print('The encrypted text is:',final_hex.upper())
    return final_hex.upper()

def des_encrypt(m):
    m,key = inputMessageAndKey(m)
    ip = rearrange_data(intial_permutation_table, m)
    kplus = rearrange_data(pc1,key)
    cndn = left_shift(shift_table, kplus)
    subkeys = subkeysGeneration(pc2,cndn)
    encrypted_message = EncryptingTheData(subkeys,ip)
    return encrypted_message

def des256(data):
    y = ''
    for i in range(0,64,16):
        x = data[i:i+16]
        a = des_encrypt(x)
        y += a
    return y 
