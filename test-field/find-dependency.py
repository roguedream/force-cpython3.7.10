import os

package_name = "termios"

files = os.listdir("sample-1")
list_files = []

for file in files:
    file_handle = open(os.path.join("sample-1",file),"r")
    try:
        content = file_handle.readlines()
        for line in content:
            if(package_name in line):
                if(file not in list_files):
                    list_files.append(file)
    except:
        print(file)
    file_handle.close()

output_file = open(package_name+".txt","w")
for file in list_files:
    output_file.write(file+"\n")
output_file.close()


