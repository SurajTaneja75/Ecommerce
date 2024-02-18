import pandas as pd
import matplotlib.pyplot as plt

def post_process(df,query_name):
    df = df.dropna()
    df = df[df['Quantity'] > 0 ]
    df = df[df['UnitPrice'] > 0 ]
    df['Amount'] = df['Quantity'] * df['UnitPrice']
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], format='%m/%d/%Y %H:%M', errors='coerce')
    df['InvoiceDate'] = df['InvoiceDate'].combine_first(pd.to_datetime(df['InvoiceDate'], format='%d-%m-%Y %H:%M', errors='coerce'))
    df['Date'] = df['InvoiceDate'].dt.date
    cust_amount_df = df.groupby('CustomerID')['Amount'].sum().reset_index()
    cust_invoice_df = df.groupby('CustomerID')['InvoiceNo'].count().reset_index()
    amount_invoice_df =  pd.merge(cust_amount_df, cust_invoice_df, on='CustomerID', how='inner')
    amount_invoice_df["AverageOrderValue"] = amount_invoice_df['Amount']/amount_invoice_df['InvoiceNo']
    amount_invoice_df.sort_values("AverageOrderValue",inplace=True,ascending=False)

    most_sold = df.groupby(['StockCode'])['Quantity'].sum().reset_index()
    most_sold = most_sold.sort_values(by=["Quantity"], ascending=False)

    if query_name == 'demand':
        # Bifurcation on demand winodown type (daily)  Quantity and amount
        daily_demand = df.groupby(['Date', 'Description'])['UnitPrice'].sum().reset_index()
        print("Date eise daily demand --> 1",daily_demand)
        pivot_df = daily_demand.pivot(index='Date', columns='Description', values=['Quantity', 'Amount'])

        pivot_df.index = pd.to_datetime(pivot_df.index)    # Plot the data 
        fig, ax1 = plt.subplots(figsize=(12, 8))
        pivot_df['Quantity'].plot(kind='bar', stacked=True, ax=ax1, position=1, width=0.4, color='b', label='Quantity')
        ax2 = ax1.twinx()
        pivot_df['Amount'].plot(kind='bar', stacked=True, ax=ax2, position=0, width=0.4, color='r', label='Amount')

        ax1.set_xlabel('Date')
        ax1.set_ylabel('Quantity', color='b')
        ax2.set_ylabel('Amount', color='r')
        plt.title('Daily Demand Bifurcation Across Categories')
        plt.show()

        print("Demand of Top 5 Stock codes", most_sold.head(5))
        print("Top 5 Countries wise demand", df['Country'].value_counts().head(5))  

    elif query_name == 'price':
        # Bifurcation on price winodow type (daily) - Price
        daily_prices = df.groupby('Date')['UnitPrice'].mean()
        print("Date wise price variation --> 1",daily_prices)

        plt.figure(figsize=(12, 8))
        plt.plot(daily_prices, marker='o', linestyle='-')

        # Set plot labels and title
        plt.xlabel('Date')
        plt.ylabel('Average Unit Price')
        plt.title('Daily Price Variation')

        # Show the plot
        plt.show()
    # unit price variation across countries can also be a measure

    
    if query_name == "customer":
        print("Top 5 Customers by order value", amount_invoice_df.head(5))
    