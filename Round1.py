T = int(input())

while(T>0):
    N, K = map(int, input().split())   

    categories = [int(x) for x in input().split()]
    time = [int(x) for x in input().split()]

    Min_dict = {}

    for i in range(len(categories)):
        try:
            Min_dict[categories[i]] = min(time[i], Min_dict[categories[i]])
        except KeyError:
            Min_dict[categories[i]] = time[i]

    sorted_time = sorted(Min_dict.values())

    time_taken = 0
    categories_eaten = 0
    
    for i in sorted_time:
        if categories_eaten >= K:
            break
        time_taken += i
        categories_eaten +=1

    if categories_eaten < K:
        print(-1)
        T-=1
        continue

    print(time_taken)

    T-=1