from textblob import TextBlob
import re
import json
import pandas as pd

#storing 2017-11-01 twitter data in df1
df1=pd.read_json('https://query.data.world/s/kpf4LLqAll5dYbMpV5WYbXkwQh6Bpq')

#storing 2017-11-02 twitter data in df2
df2=pd.read_json('https://query.data.world/s/dYtdFJPEQdsAbA8oXDYTQJj0cWWoAR')

#storing 2017-11-03 twitter data in df3
df3=pd.read_json('https://query.data.world/s/43i9j7GxCK7wCl1InvdLAgLsvEuewx')

#converting df1 in to list and storing in list1
list1=df1.values.tolist()

#converting df2 in to list and storing in list2
list2=df2.values.tolist()

#converting df3 in to list and storing in list3
list3=df3.values.tolist()

#concating list1, list2, list3
c=[list1,list2,list3]
data=sum(c,[])

#function remove link, tags from text
def clean_text(text):
    
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())

#function to analyze given text it return 1 if sentence is +ve otherwise return 0
def analize_sentiment(text):
   
    analysis = TextBlob(clean_text(text))
    if analysis.sentiment.polarity > 0:
        return 1
    elif analysis.sentiment.polarity == 0:
        return 0
    else:
        return 0


#storing positive word in alist
positive_bow=["Good","good","very good","Very Good","Nice","nice"]

#variable to check referces in text belongs to Donald Trump
ref="@realDonaldTrump"

#declaring count and x variable
x=0;
count=0

#iterating in the list 
for l in data:
    x=0
    #checking text is reference to donald trump or not
    if ref in l[4]:
        #cleaning the text 
        cleaned_text=clean_text(l[4])
        #checking any positive word present in cleaned_text
        for positive_word in positive_bow:
            if positive_word in cleaned_text:
                #if positive word is present chexk the polarity of text
                x=analize_sentiment(cleaned_text)
                #if polarity is 1 increase count by 1
                if(x==1):
                    count=count+1


#calculating percentage of positive tweet refernced to Donald Trump
a=(float(count)/float(len(references)))*100

print("Total % of tweets that are positive in nature "+str(a))


