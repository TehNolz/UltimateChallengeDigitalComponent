import os
i = 1
for file in os.listdir():
    os.rename(file, "card-base-"+str(i)+".png")
    i+=1
