import re
path  = r"F:\cloud-storage\backend\app\ML\data_set.txt"


with open (path, "r" , encoding="utf-8") as file :
    for line in file:
        clean_line = line.strip("#").strip() # stripe remove special chrecters from string 
        # print(clean_line)
        if "download" in clean_line:
            # print("this is a download line ")
            match = re.search(r"=\s*(\d+)", clean_line)
            if match:
                number = match.group(1)
                main_number = number
                download  = int(main_number)

        elif "upload" in clean_line:
            # print("this is a upload line ")
            match = re.search(r"=\s*(\d+)", clean_line)
            if match:
                number = match.group(1)
                a = number
                upload = int(a)
        elif "delet" in clean_line:
            # print("this is a delet line")  
            match = re.search(r"=\s*(\d+)", clean_line)
            if match:
                number = match.group(1)
                b = number
                delet = int(b)  
        elif "lebel" in clean_line:
            pice = clean_line.strip().split("=")
            print(download , upload , delet , pice[1].strip() , sep=",") #seperation with coma         