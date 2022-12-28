#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

goodreads_file = pd.read_csv("goodreads_library_export.csv")


# In[3]:


#Converting the goodreads 'Date Read' column into datetime format
books_2022 = goodreads_file[pd.to_datetime(goodreads_file['Date Read'], format = "%Y/%m/%d") >= "2022-01-01"]
books_2022 = books_2022.reset_index(drop = True)
#dropping the columns we don't need
books_2022 = books_2022.drop(['Publisher','Binding','Book Id','Author l-f','Additional Authors','ISBN','ISBN13' ,'Bookshelves','Bookshelves with positions', 'Exclusive Shelf', 'My Review','Spoiler','Private Notes','Read Count', 'Owned Copies', 'Year Published'], axis = 1,inplace = False)
books_2022.loc[52] = ['The Metamorphosis','Franz Kafka', 5, 3.84, 201.0, 1915.0, pd.to_datetime('2022/03/22').date().strftime('%Y/%m/%d'), pd.to_datetime('2021/01/23').date().strftime('%Y/%m/%d')]
books_2022.loc[53] = ['The Railway Children','E. Nesbit', 4, 4.02, 188.0, 1906.0, pd.to_datetime('2022/08/25').date().strftime('%Y/%m/%d'), pd.to_datetime('2022/08/20').date().strftime('%Y/%m/%d')]
#Dropping columns for cummulative graph
cb = books_2022.drop(['Title','Author', 'My Rating', 'Average Rating','Original Publication Year','Date Added'], axis = 1, inplace = False)
#dropping columns for ratings graph
r = books_2022.drop(['Author','Number of Pages', 'Original Publication Year', 'Date Read', 'Date Added'], axis = 1, inplace = False)


# In[4]:


df_subset = books_2022.loc[books_2022['Original Publication Year'] != 1853]

#grouping the books by the year they were published in
books_grouped = df_subset.groupby('Original Publication Year').count()

#Bar graph of books published in different years
plt.figure(figsize=(12, 6))
plt.bar(books_grouped.index, books_grouped['Title'], width = 1.0, color=(0.2, 0.4, 0.6, 0.6))
plt.title('Number of Books read from particular year')
plt.xlabel('Publication Year')
plt.ylabel('Number of Books read')
plt.xticks(np.arange(1902,2023,6), rotation = 90)
plt.show()


# In[5]:


#setting the chart style
sns.set_style("darkgrid")
sns.set_context("talk")

# Convert the Date Read column to a datetime data type
cb["Date Read"] = pd.to_datetime(cb["Date Read"], format = '%Y/%m/%d')
cb["month"] = cb["Date Read"].dt.strftime("%m")
#sorting by month and creating a new column
cb_sorted = cb.sort_values(by="month")
#dropping the date read
cb_sorted = cb_sorted.drop('Date Read', axis = 1)
# Use the groupby and cumsum functions to create a new data frame with the cumulative number of books and pages read by month
cb_sorted_combined = cb_sorted.groupby("month")["Number of Pages"].sum()
cb_sorted_combined = cb_sorted_combined.reset_index()
cb_sorted_combined["month"] = pd.to_datetime(cb_sorted_combined["month"], format = '%m')
cb_sorted_combined["month"] = cb_sorted_combined["month"].dt.strftime("%B")
cb_sorted_combined.loc[-1] = ['January', 0]
cb_sorted_combined.index = cb_sorted_combined.index + 1
cb_sorted_combined.sort_index(inplace = True)

#graph parameters
cb_sorted_combined.plot(kind='bar', x='month', y='Number of Pages', 
        figsize=(10, 8), legend=False, color='powderblue', rot=0);
plt.title("Number of pages read in each month", y=1.01, fontsize=20)
plt.ylabel("Number of pages read", labelpad=15)
plt.xlabel("Months", labelpad=15)
plt.xticks(rotation = 90)





# In[6]:


#cumsum graph
cb_sorted_combined['pages_total'] = cb_sorted_combined['Number of Pages'].cumsum()

cb_sorted_combined.plot(x='month', y='pages_total', kind='line', figsize=(15, 10), legend=False, style='yo-', label="count students graduated running total")
plt.title("Running total of number of pages read", y=1.01, fontsize=20)
plt.ylabel("Number of pages", labelpad=15)
plt.xlabel("Months", labelpad=10)
month_names = ["January", "February", "March", "April", "June", "July", "August", "September", "October", "November", "December"]
plt.xticks(cb_sorted_combined.index, [month_names[i] for i in cb_sorted_combined.index], rotation = 90)


# In[9]:


sns.set_style("darkgrid")
sns.set_context("talk")

r = r.assign(ratings=lambda x: x['My Rating'] - x['Average Rating'])
r_sorted = r.sort_values('ratings')
r_sorted.plot.barh(y='ratings', x= 'Title', width = 1, figsize = (10,18), legend = False)
plt.xlabel("Difference between My rating and Average good reads rating", labelpad=15)
plt.ylabel("Title", labelpad=10)


mean_my = r['My Rating'].mean()
mean_avg= r['Average Rating'].mean()
print(mean_my,mean_avg)


# In[14]:


titles = books_2022[['Title', 'Date Read']].copy()
titles["Date Read"] = pd.to_datetime(titles["Date Read"], format = '%Y/%m/%d')
titles_sorted = titles.sort_values(by="Date Read")

titles_sorted["Date Read"] = titles_sorted["Date Read"].dt.strftime("%B")
#print (titles_sorted)

month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

# Group the data by month
groups = titles_sorted.groupby('Date Read')

# Sort the groups by the index of the month name in the month_names list
sorted_groups = sorted(groups, key=lambda x: month_names.index(x[0]))


for name, group in sorted_groups:
    # print the month
    month_str =f"<div style='text-align:center;font-weight:bold;font-size:20px'>{name}</div>"
    display(HTML(month_str))
    print()
    # iterate over the book titles in the group
    for title in group['Title']:
        # print the title
        title_str = f"<div style='text-align:center'>{title}</div>"
        display(HTML(title_str))
    print() 


# In[ ]:




