facebook=open("facebook_combined.txt/facebook_combined.txt")
facebook_sub=open("17CS30030/subgraphs/facebook.elist","w")
while True :
    line=facebook.readline()
    if len(line) ==0 :
        break
    a,b=[int(i) for i in line.split()]
    if a%5!=0 and b%5!=0 :
        print(a,b,file=facebook_sub)


twitter=open("twitter_combined.txt/twitter_combined.txt")
twitter_sub=open("17CS30030/subgraphs/twitter.elist","w")
while True :
    line=twitter.readline()
    if len(line) ==0 :
        break
    a,b=[int(i) for i in line.split()]
    # print(a,b)
    if a%4==0 and b%4==0 :
        print(a,b,file=twitter_sub)