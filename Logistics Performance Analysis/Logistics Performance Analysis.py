!pip install kagglehub

import kagglehub
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Download latest version
path = kagglehub.dataset_download("shahriarkabir/us-logistics-performance-dataset")
file_path = r"C:\Users\abiol\.cache\kagglehub\datasets\shahriarkabir\us-logistics-performance-dataset\versions\1\logistics_shipments_dataset.csv"
df = pd.read_csv(
               file_path, 
               parse_dates=["Shipment_Date", "Delivery_Date"],
               index_col = False,
               dtype={
                    "Shipment ID": "int8",
                    "Origin_Warehouse": "string",
                    "Destination": "string",
                    "Carrier": "string"             
                    
                }
        )

#1   Shipment Volume Trends

#1.1 How many shipments are made per month/week?
df['Shipment_Date']= pd.to_datetime(df['Shipment_Date'])
shipment_per_month = df.groupby(df['Shipment_Date'].dt.to_period("M")).size()
shipment_per_week = df.groupby(df['Shipment_Date'].dt.to_period("W")).size()

#1.2 Are there peak periods?
avg = shipment_per_week.mean()
std = shipment_per_week.std()
peak_weeks= shipment_per_week[shipment_per_week>avg+std]


#2   Delivery Performance

#2.1 What is the average Transit_Days?
avg_transit_days = df['Transit_Days'].mean()

#2.2 Which carriers have the fastest or slowest deliveries?
avg_delivery_times_carrier= round(df.groupby(['Carrier'])['Transit_Days'].mean().sort_values(),2)


#3   Cost Analysis

#3.1 What is the average shipment Cost by Origin_Warehouse or Carrier?
avg_shipment_cost= df['Cost'].mean()
Cost_by_Origin_Warehouse = round(df.groupby('Origin_Warehouse')['Cost'].mean().sort_values(),2)
Cost_by_Carrier = round(df.groupby('Carrier')['Cost'].mean().sort_values(),2)

#3.2 Which routes are the most expensive?
Cost_by_destination = round(df.groupby('Destination')['Cost'].mean().sort_values(ascending=False),2)


#4   Weight & Distance Analysis

#4.1 How does Weight_kg relate to Cost?
correlation_of_weight_cost = round(df['Weight_kg'].corr( df['Cost']),2)

#4.2 Which routes cover the longest distances?
Long_ditances_by_destination = df.groupby('Destination')['Distance_miles'].sum().sort_values(ascending=False)


#5   Status Monitoring

#5.1 What percentage of shipments are Delivered, In Transit, Delayed, etc.?
status_percentages= (df['Status'].value_counts()/len(df))*100

#5.2 Are certain routes more prone to delays?
df['Is_delayed']= df['Status'].str.strip().str.title() == 'Delayed'
delayed_routes= df.groupby('Destination')['Is_delayed'].mean().sort_values(ascending=False).mul(100)


#6   Carrier Performance

#6.1 Which Carrier ships the most parcels?
Carrier_with_most_parcels = df.groupby('Carrier')['Shipment_ID'].size().sort_values(ascending=False)

#6.2 Which carrier has the lowest average Transit_Days?
Carrier_Min_Transit = df.groupby('Carrier')['Transit_Days'].mean().sort_values(ascending=False).round(2)


#7 Route Popularity

#7.1 Which Origin_Warehouse to Destination combinations are most frequent?
Warehouse_to_Destination_combinations = df.groupby(['Origin_Warehouse', 'Destination'])['Shipment_ID'].size().sort_values(ascending=False)


#8  Transit Efficiency

#8.1 Is there a correlation between Distance_miles and Transit_Days?
Distance_Transit_Days_Correlation= df['Distance_miles'].corr(df['Transit_Days']).round(2)


#9   Cost Efficiency

#9.1  Which shipments have the lowest cost per mile or per kg?
df['cost_per_kg']= df['Cost']/df['Weight_kg']
df['cost_per_mile']= df['Cost']/df['Distance_miles']
lowest_cost_per_mile_Shipment = df.sort_values('cost_per_mile', ascending= False).head(10)
lowest_cost_per_kg_Shipment = df.sort_values('cost_per_kg', ascending= False).head(10)
lowest_cost_per_kg_Shipment


#10   Shipment Patterns

#10.1  Are there patterns in delivery dates (weekdays vs weekends)?
df['Delivery_Date'] = pd.to_datetime(df['Delivery_Date'])
df['Weekday']=df['Delivery_Date'].dt.dayofweek
df['day_type'] = df['Weekday'].apply(lambda x:"Weekend" if x >= 5 else "Weekday")
delivery_counts = df['day_type'].value_counts(normalize=True).mul(100).round(2)



shipment_counts = df.groupby('Shipment_Date').size()

plt.figure(figsize=(12,6))
shipment_counts.plot()
plt.title("Shipments Over Time")
plt.xlabel("Shipment Date")
plt.ylabel("Number of Shipments")
plt.show()



avg_transit = df.groupby('Carrier')['Transit_Days'].mean().sort_values()

plt.figure(figsize=(10,6))
sns.barplot(x=avg_transit.values, y=avg_transit.index)
plt.title("Average Transit Days by Carrier")
plt.xlabel("Carrier")
plt.ylabel("Average Transit Days")
plt.show()



plt.figure(figsize=(10,6))
sns.scatterplot(data=df, x='Weight_kg', y='Cost', hue='Carrier')
plt.title("Shipment Cost vs Weight")
plt.xlabel("Weight (kg)")
plt.ylabel("Cost ($)")
plt.show()