import pandas as pd
import json

#storing 2017-11-01 twitter data in df1
df1=pd.read_json('https://query.data.world/s/kpf4LLqAll5dYbMpV5WYbXkwQh6Bpq')

#storing 2017-11-02 twitter data in df2
df2=pd.read_json('https://query.data.world/s/dYtdFJPEQdsAbA8oXDYTQJj0cWWoAR')

#storing 2017-11-03 twitter data in df3
df3=pd.read_json('https://query.data.world/s/43i9j7GxCK7wCl1InvdLAgLsvEuewx')

#joining all three dataframes from 2017-11-01 to 2017-11-03 in to one dataframe
df4=[df1, df2, df3]
df=pd.concat(df4)

#finding all references to Donald Trump
references=df[df['text'].str.contains("@realDonaldTrump")]
#printing all refernces
print("The account referncing donald trump are:\n")
print(references)

#finding total number of accounts
total_accounts=df.groupby('user_id').size().shape
#finding total number of accounts referencing donald trump
donaldtrump_related_accounts=references.groupby('user_id').size().shape

#findin total percentage of accounts tweeting about Donald Trump
total_percentage=(float(donaldtrump_related_accounts[0])/float(total_accounts[0]))*100
#printing total percentage
test=str(total_percentage)
print("The total % of account tweeting about donald trump is "+test)

#counting number of tweets referencing Donald Trump from each user accounts
frequency=references.groupby(['user_id','screen_name'])['text'].count()
#sorting user'id based on the count in descending order
accounts_in_descending_order=frequency.nlargest(donaldtrump_related_accounts[0])
#printng the accounts
print("The accounts in descending order of frequency:")
print(accounts_in_descending_order)
