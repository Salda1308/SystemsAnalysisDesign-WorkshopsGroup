import pandas as pd
import matplotlib.pyplot as plt
import math
import statsmodels.api as sm
from statsmodels.formula.api import ols

train = pd.read_csv("data_training.csv")


# We can see what type of data we have and perform a basic statistical analysis
print(train.info())
print(train.describe())

# Additionally, we check if we have missing data
print(train.isnull().sum())

''' I will define each column to better understand the data before any analysis

Id - Region the chocolate company is operating in
Marketing Campaigns (noted in number of GRPs per region)


Web_GRP - Audience reached via web campaigns
TV_GRP - Audience reached via TV campaigns
Facebook_GRP - Audience reached via Facebook campaigns
Tone_of_Ad - Tone of advertisement ("emotional", "serious", "funny")
No_of_Web_Banners - Number of web banners used on the home page

Regional Specifics

Weather - The general weather in the region (i.e., "sunny", "cloudy", "rainy")
Avg_Temperature - Average high temperature in the region in degrees celsius
No_of_Rabbits - Number of rabbits in region, in thousands
Network_Five_G - Existence of 5G network (0 = no, 1 = yes)
No_of_iPhone_14_Sold - Number of iPhone 14 sold per year in region, in thousands
No_of_Big_Cities - Number of big cities in region
Health_Index - Health index of region (high values indicate high health awareness)
Sustainability_Index - Sustainability index of region (high values indicate high sustainability)
Choc_Capital_Distance - Distance to Brussels, Belgium, the "Chocolate Capital of the World", in km
No_of_Competitors - Number of competitors operating in region (only big companies included)
Import_Regulations - Existence of import regulations for region (0 = no, 1 = yes)
Time_in_Region - Time the chocolate company is operating in that region in months
Customers

Percent_Internet_Access - Percent of population in region that has access to the internet
Percent_Uni_Degrees - Percent of population in region with a university degree
Percent_Unemployed - Unemployment rate in region
Gender - Gender (male = 0, female = 1)
Coffee_Consumption - Coffee consumption in region (i.e., "low", "medium", "high")
Avg_No_of_Cust_Complaints - Average number of customer complaints in year in region
Avg_Customer_Age - Average age of customers in years

'''

# I want to visualize the data, for that I will define the range using Velleman's rule, that is, my 750^(1/2)
Range = math.ceil(750**(1/2))
print("The range will be ", Range)

counts, bins, patches = plt.hist(train['sales'], bins=Range)

plt.title("Sales Distribution")
plt.show()

# Now I want to see the frequency of each range
hist_df = pd.DataFrame({
    "Range": [f"{bins[i]:.0f} - {bins[i+1]:.0f}" for i in range(len(bins) - 1)],
    "Frequency": counts.astype(int)
})
print(hist_df)

print("\nTop 10 values for Time_in_Region:")
print(train['Time_in_Region'].head(10))


# It won't let me do the correlation because I have str data, so I can assign numerical values to them to see if I can do the correlation this way
#train.corr()['sales'].sort_values(ascending=False)
# I will see which columns are object and their value on how I can assign numerical values without overwriting the data
print(train.dtypes)

# I see which columns are object
print(train.select_dtypes(include=['object']).columns)
# I see the unique values of each object column
print(train['Tone_of_Ad'].unique())
print(train['Weather'].unique())
print(train['Coffee_Consumption'].unique())

# I assign numerical values to each object column
train['Tone_of_Ad'] = train['Tone_of_Ad'].map({'funny': 2, 'emotional': 1, 'serious': 0})
train['Weather'] = train['Weather'].map({'sunny': 2, 'cloudy': 1, 'rainy': 0})
train['Coffee_Consumption'] = train['Coffee_Consumption'].map({'high': 2, 'medium': 1, 'low': 0})

# I verify that there are no more object columns
print(train.select_dtypes(include=['object']).columns)


# Now I can do the correlation
correlation = train.corr()['sales'].sort_values(ascending=False)
print(correlation)


# Create ANOVA model
model = ols('sales ~ Web_GRP + TV_GRP + Facebook_GRP + Tone_of_Ad + No_of_Web_Banners + Weather + Avg_Temperature + No_of_Rabbits + Network_Five_G + No_of_iPhone_14_Sold + No_of_Big_Cities + Health_Index + Sustainability_Index + Choc_Capital_Distance + No_of_Competitors + Import_Regulations + Time_in_Region + Percent_Internet_Access + Percent_Uni_Degrees + Percent_Unemployed + Gender + Coffee_Consumption + Avg_No_of_Cust_Complaints + Avg_Customer_Age', data=train).fit()

anova_table = sm.stats.anova_lm(model, typ=2)
print(anova_table.sort_values('PR(>F)'))