arr = [90,80,70,60,50,40,30,20,10,1,0]

print(90 < 1)

temp = arr[0]

arr[0] = arr[8]
arr[8] = temp

print(arr)




def sort(data):

    for i in range(len(data)):
        for j in range(len(data)):
            print('============================================')
            print(f'{data} \n')


            print(f"is {data[i]} < {data[j]}")
            print(data[i] < data[j])
            print('============================================')

            if data[i] < data[j]: # >
                temp = data[i]

                data[i] = data[j]
                data[j] = temp

    return data



           # print(data[i], data[j])




print(f'there are {len(arr)} data')


print(sort(arr))



temp_arr = [10,20,30,40]

target = 0


highlight = [f"\0-33[9m{val}\033[0m" if i == target else str(val) for i, val in enumerate(temp_arr)]

print(f"[{', '.join(highlight)}]")
