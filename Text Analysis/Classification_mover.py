import nltk
import shutil

serial=[]
brand=[]
rating=[]


metadata=open("C:\\Users\\JackLi\\Dropbox\\Text Analysis Dataset\\AmazonMP3Reviews\\Subset of MetaData.xlsx",'r')
for line in metadata:
    tokens=line.split(',')
    serial.append(tokens[0])
    brand.append(tokens[1])
    rating.append(tokens[2])

for i in range():
    #if(i!=0):
    try:
        print(str(i))
        print(str(rating[i]))
        shutil.copy("C:\\Users\\JackLi\\Dropbox\\Text Analysis Dataset\\AmazonMP3Reviews\\Reviews\\"+str(i)+".txt", "C:\\Users\\JackLi\\Dropbox\\Text Analysis Dataset\\AmazonMP3Reviews\\main_branding"+str(rating[i].rstrip()))
        #input=open("C:\\Users\\JackLi\\Documents\\Reviews\\"+str(i)+".txt","r")

        #output=open("C:\\Users\\JackLi\\Documents\\Reviews\\rating"+str(rating[i].rstrip())+"\\"+str(i)+".txt","w")
        #print(input)
        #print(output)
        #for line in input:
            #print(line)
            #output.write(line)

        #input.close()
        #output.close()
    except:
        pass
'''
i=31
input = open("C:\\Users\\JackLi\\Documents\\Reviews\\" + "31" + ".txt", "r")
print(input)
for line in input:
    print(line)

input = open("C:\\Users\\JackLi\\Documents\\Reviews\\" + str(i) + ".txt", "r")
print(input)
for line in input:
    print(line)
'''