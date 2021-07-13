logfile = open("C:\\Users\\User\\Desktop\\test-field\\output\\mylog-3.7.txt","r")
full_coverage = [0] * 10000
for line in logfile:
    if(": Coverage: " in line):
        line = line.split(": ")[2]
        part = line.split(",")[:-1]
        for element in part:
            if(" - ") in element:
                left = int(element.split(" - ")[0])
                right = int(element.split(" - ")[1])
                while(left <= right):
                    full_coverage[left] = 1
                    left = left + 1
            else:
                full_coverage[int(element)] = 1

index = 0
count = 0
while index < 10000:
    if full_coverage[index] == 1:
        search_index = index + 1
        while ((full_coverage[search_index] == 1) and (search_index < 10000)):
            search_index = search_index + 1
        if(search_index == index + 1):
            print(index)
            count = count + 1
        else:
            print(str(index) + " - " + str(search_index))
            count = count + (search_index - index) + 1
        index = search_index
    else:
        index = index + 1
print(count)
code_lines = [0] * 10000
codefile = open("C:\\Users\\User\\Desktop\\test-field\\test-now.py","r")
