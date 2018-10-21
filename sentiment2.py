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


#creating empty list to storing user_id
references=[]
#creating empty list to storing user_id
references1=[]


#variable to check referces in text belongs to Donald Trump
ref="@realDonaldTrump"
#initialising variable
x=0;


#iterating in the list 
for l in data:
    x=0
    #checking text is reference to donald trump or not
    if ref in l[4]: 
        #cleaning the text 
        cleaned_text=clean_text(l[4]) 
        #storing the polarity of given text in x
        x=analize_sentiment(cleaned_text)
        #checking if x is 1 then increasing the % of positive tweet by 1
        if(x==1):
            count=count+1
        #storing user_id in reference
        #storing value of x in reference1
        references.append(l[6])
        references1.append(x)

#appending referece and reference1 in dataframe df by name user_id and x as score
df = pd.DataFrame({'user_id':references,'score':references1})

#finding the mean of score group by user_id and storing in new dataframe in mean_df
mean_df=df.groupby(['user_id']).mean()

#initialising variable to count tweet with positivity greater than 50%
count=0

#finding the number of row in mean_df
length_mean_df=len(mean_df)

#moving in the dataframe
for i in range(0,length_mean_df):
    #checking the mean of score of each account  is greater than 0.5 and if yes than increasing the count
    if(int(mean_df.iloc[i,0:1])>0.5):
        count=count+1

#finding the % of account more than 50% positive tweet
ans=(float(count)/float(length_mean_df))*100

#printing the answer
print("Total % of accounts having positive tweet about Donald Trump "+str(ans)+"%")

