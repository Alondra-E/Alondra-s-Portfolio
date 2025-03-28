# -*- coding: utf-8 -*-
"""Market Basket: Sales Summary, Category, and Products

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Fq5xy44Rv2lkr59jXxneotmWaqyvSHJI
"""

from google.colab import files
uploaded = files.upload()

import pandas as pd

df = pd.read_excel('vb_sales (1).xlsx')
df.head(5)

#a bit of data exploration
#Data spans from (2022-10-01) - (2024-10-04)
df.head()

# Summary of the dataset: data types, non-null values
df.info()

# Summary statistics of numeric columns
df.describe()

# Check for missing values in the dataset
missing_data = df.isnull().sum()
print(missing_data)

#I dont think i'll add this, not sure what I would say about this,
#I think I'll just talk about reports>Sales trends>Gross sales in comparison to last year, and how it is more popular on any other day except mon-tues the most
#qty seems off

# year Ensure 'Qty' is numeric
df['Qty'] = pd.to_numeric(df['Qty'], errors='coerce').fillna(0)

# Calcculate key sales metrics
total_qty_sold = df['Qty'].sum()
total_gross_sales = df['Gross Sales'].sum()
total_discounts = df['Discounts'].sum()
total_net_sales = df['Net Sales'].sum()

# Summary dictionary
sales_summary = {
    'Total Quantity Sold': total_qty_sold,
    'Total Gross Sales': total_gross_sales,
    'Total Discounts': total_discounts,
    'Total Net Sales': total_net_sales
}

# Display summary
for metric, value in sales_summary.items():
    if metric == 'Total Quantity Sold':
        print(f'{metric}: {value:,.0f}')  # Display quantity as numetical
    else:
        print(f'{metric}: ${value:,.2f}')  # Display financial values with dollar sign

s1

# Grouping by both 'item' and 'Category', then summing the 'Qty'
popular_products = df.groupby(['Item', 'Category'])['Qty'].sum().reset_index()

# Sort
popular_products_sorted = popular_products.sort_values(by='Qty', ascending=False)

# Top 10 most popular products based on quantity sold
popular_products_sorted.head(10)

#top 10 products by qty, show quick to explain some things we noticed from the data
import matplotlib.pyplot as plt

top_10 = popular_products_sorted.head(10)

# Concatenate 'Item' and 'Category' into a single label for the bar chart
labels = top_10['Item'] + ' (' + top_10['Category'] + ')'

# Create a bar chart
plt.figure(figsize=(10,8))
plt.barh(labels, top_10['Qty'], color='green')
plt.xlabel('Quantity Sold')
plt.title('Top 10 Most Popular Products by Quantity Sold')
plt.gca().invert_yaxis()
plt.show()

#10 lowest products, maybe talk abit bout how this is benificial to either drop these items or increase innovation expenses to them? IDK if its displayed correctly tho, the qty seems off

# Grouping by both 'Item' and 'Category', then summing the 'Qty'
popular_products = df.groupby(['Item', 'Category'])['Qty'].sum().reset_index()

# Sort ascending from top 10 popular products
least_popular_products_sorted = popular_products.sort_values(by='Qty', ascending=True)

# lowest 10 products based on quantity sold
least_popular_products_sorted.head(10)

#Ideas/Questions
#did he ever mention hours have changed over the last 2 years?
#possible challenges or things we need to do to better our data would be:
#testing for outliers, null values

"""# Market Basket Analysis"""

# Market Basket Analysis
# Import necessary libraries
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

# Load the dataset (replace with your file path)
df = pd.read_excel('cleaned_verde_data.xlsx')

# Step 1: Create a 'Transaction_ID' by combining 'Date' and 'Time'
df['Transaction_ID'] = df['Date'].astype(str) + ' ' + df['Time'].astype(str)

# Step 2: Pivot table to create a binary matrix of transactions and items
basket = df.pivot_table(index='Transaction_ID', columns='Item', values='Qty', aggfunc='sum').fillna(0)

# Step 3: Convert all quantities to 1 (purchased) or 0 (not purchased)
basket = basket.applymap(lambda x: 1 if x > 0 else 0)

# Step 4: Apply Apriori algorithm to find frequent itemsets
frequent_itemsets = apriori(basket, min_support=0.05, use_colnames=True)

# Step 5: Generate association rules
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0)

# Step 6: Sort frequent itemsets by support in descending order for better insights
frequent_itemsets_sorted = frequent_itemsets.sort_values(by='support', ascending=False)

# Step 7: Sort rules by confidence for better insights
rules_sorted = rules.sort_values(by='support', ascending=False)

# Display the top frequent itemsets and association rules
print("Top Frequent Itemsets:\n", frequent_itemsets_sorted)
print("\nTop Association Rules:\n", rules_sorted)



"""Strategies for Frequent Itemsets:
*   Focus on High-Support Items: Items like BBQ Pork and Blue Sky Hazy should be the focus of promotions. These items can be bundled or positioned as the centerpiece of combo meals.
*   Promote Moderate-Support Items: Items like Chicken Sandwich, Elote Dog/Bowl, and Dark Lager have moderate demand but could be pushed further through cross-selling or discounts.
*   Experiment with Lesser-Popular Items: Items like Chips and Flight show less demand but can be paired with more popular items. For instance, offering BBQ Pork with Chips could encourage customers to pick both.

Strategies for Association Rule:


*   Leverage Strong Associations:
The strongest rule here is between Soda and Nachos with a high confidence of 0.5723 and a lift of 1.6717. This suggests a strong relationship where people buying soda are likely to buy nachos as well. Offer Nachos + Soda combos or promotions. This pairing is likely to drive higher sales.

*   Cross-Promote BBQ Pork and Gold Buckle:
While the lift is modest (~1.07), there’s still a positive association between BBQ Pork and Gold Buckle items. Could offer a special deal (e.g., a combo platter) involving these two items, incentivizing customers to purchase them together.

*  Pairings with Nachos:
Nachos appear to be a common item in several rules, paired both with Gold Buckle and Soda. This means Nachos could be a central item for upselling or cross-promoting other items. For example, Nachos + Soda can be a combo deal, while Nachos + BBQ Pork or Gold Buckle can be highlighted as meal upgrades.

Heat Map
"""



# Nachos and Soda: There is a strong association between these two items, implying they are frequently purchased together.
# Gold Buckle and Nachos: There is a weaker association between these two, as indicated by the lighter and thinner line, but there is still a notable connection.
# BBQ Pork and Gold Buckle: These two are connected, meaning they are likely bought together at times, though the association appears weaker compared to the "Nachos-Soda" pair.

"""



*   Cross-selling opportunities: Verde could run a promotion where buying Nachos leads to a discount on Soda since these items are frequently bought together.
*   Place frequently bought-together items near each other, improving customer convenience and increasing sales



"""

import seaborn as sns
import matplotlib.pyplot as plt

def plot_heatmap(rules):
    # Create a pivot table for the heatmap (lift)
    heatmap_data = rules.pivot_table(index='antecedents', columns='consequents', values='lift')

    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_data, annot=True, cmap="YlGnBu")
    plt.title('Heatmap of Lift for Association Rules')
    plt.show()

# Call the function
plot_heatmap(rules)

"""*   The pair (Soda → Nachos) has a lift of 1.7, meaning that customers who buy soda are 1.7 times more likely to buy nachos compared to customers who don’t buy soda
*   The pair (BBQ Pork → BBQ Pork) has a lift of 1.1, which is close to 1, indicating a weak or neutral association (customers who buy BBQ Pork are slightly more likely to buy BBQ Pork again).

```
# This is formatted as code
```
"""

import matplotlib.pyplot as plt
from matplotlib_venn import venn2

# Set the sizes of each set
total_nachos = 35
total_gold_buckle = 30
nachos_and_buckle = 12

# Venn diagram
plt.figure(figsize=(7, 7))
venn = venn2(subsets=(total_nachos - nachos_and_buckle, total_gold_buckle - nachos_and_buckle, nachos_and_buckle),
             set_labels=('Nachos', 'Gold Buckle'),
             set_colors=('#243a5eff', '#24371bff'))  # Set colors for the two sets

venn.get_label_by_id('10').set_text(f"{total_nachos - nachos_and_buckle}%")
venn.get_label_by_id('01').set_text(f"{total_gold_buckle - nachos_and_buckle}%")
venn.get_label_by_id('11').set_text(f"{nachos_and_buckle}%")
plt.title("Venn Diagram of Nachos and Gold Buckle")

# Change the color of the intersection
for label in venn.set_labels:
    label.set_color('#454545ff')  # Set color for the labels

plt.show()

import matplotlib.pyplot as plt
import pandas as pd

# Data for visualization (Combination products)
data_combination = {
    'itemsets': [
        'Nachos, Gold Buckle', 'Nachos, Wildflower', 'Nachos, BBQ Pork',
        'Gold Buckle, BBQ Pork', 'Nachos, Soda', 'Wildflower, Gold Buckle'
    ],
    'support': [
        0.113979, 0.073382, 0.064383, 0.063114, 0.052728, 0.052410
    ]
}

df_combination = pd.DataFrame(data_combination)

# Plot combination items with smaller chart and smaller labels
plt.figure(figsize=(8, 4))  # Smaller figure size
bars = plt.bar(df_combination['itemsets'], df_combination['support'], color='#7f7f60ff')

# Set labels and title with smaller font sizes
plt.xlabel('Itemsets', fontsize=10)   # Smaller x-axis label font size
plt.ylabel('Support', fontsize=10)    # Smaller y-axis label font size
plt.title('Support for Combination Items', fontsize=12)  # Smaller title font size

# Set horizontal x-axis labels with even smaller font size
plt.xticks(rotation=0, fontsize=6, ha='center')

# Remove gridlines
plt.grid(False)

# Add values on top of each bar
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 4),
             ha='center', va='bottom', fontsize=8)

# Adjust layout
plt.tight_layout()
plt.show()

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Data for the top association rules
data = {
    'antecedents': [
        'Nachos → Gold Buckle', 'Gold Buckle → Nachos',
        'Gold Buckle → BBQ Pork', 'BBQ Pork → Gold Buckle',
        'Nachos → Soda', 'Soda → Nachos'
    ],
    'support': [
        0.113979, 0.113979, 0.063114, 0.063114,
        0.052728, 0.052728
    ],
    'confidence': [
        0.332947, 0.372216, 0.206111, 0.327842,
        0.154024, 0.572289
    ],
    'lift': [
        1.087295, 1.087295, 1.070622, 1.070622,
        1.671734, 1.671734
    ]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Set the figure size
plt.figure(figsize=(10, 6))

# Melt the DataFrame for easier plotting
df_melted = df.melt(id_vars='antecedents',
                    value_vars=['support', 'confidence', 'lift'],
                    var_name='metric', value_name='value')

# Create a bar plot
ax = sns.barplot(x='antecedents', y='value', hue='metric', data=df_melted, palette='Set2')

# Add titles and labels
plt.title('Top Association Rules Metrics')
plt.xlabel('Association Rules')
plt.ylabel('Value')

# Set the x-axis labels to be horizontal and smaller
plt.xticks(rotation=0, fontsize=8)

# Add the value on top of each bar
for p in ax.patches:
    ax.annotate(f'{p.get_height():.2f}',
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', fontsize=8, color='black',
                xytext=(0, 5),
                textcoords='offset points')

# Remove the gridlines
plt.grid(False)

# Show the plot
plt.tight_layout()
plt.show()