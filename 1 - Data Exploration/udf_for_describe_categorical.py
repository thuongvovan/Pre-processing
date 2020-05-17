# Import library
import pandas as pd
import numpy as np 
import seaborn as sns 
import matplotlib.pyplot as plt 
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff


# Definded function
## Class of formart text
class formart_text:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

# Functinon for create summary table
def create_summary_table(table, head= None):
    if head == None:
        head= 20
    table.index= table.index.astype(str)
    notna_table= table[table.index != 'nan']
    head_table= notna_table.head(head)
    na_table= table[table.index == 'nan']
    if na_table.shape[0] > 0:
        na_table.index= ['Missing value(s)']
    other_table= notna_table.drop(head_table.index)
    other_sum= other_table.sum(0)
    n_other= other_table.shape[0]
    summary_table= head_table.copy()
    if table.shape[0] >= head:
        summary_table.loc['{} Other group(s)'.format(n_other), other_sum.index.tolist()]= other_sum.tolist()
    summary_table= summary_table.append(na_table)
    return summary_table

# Functinon for print table
def print_table(table, index_name= None):
    table= pd.DataFrame(table)
    for column in table.columns[table.dtypes != 'object']:
        table[column]= table[column].apply(lambda x: round(x, 2))
    if index_name != None:
        table= table.reset_index().rename(columns={'index': index_name})
    width= 500
    height= 130 + (table.shape[0] - 5) * 20
    if height > 300:
        height= 300
    layout = go.Layout(
                autosize=False,
                width= width, height= height,
                margin=go.layout.Margin(
                    l=30,
                    r=30,
                    b=0,
                    t=0,
                    pad = 4)
                )
    fig = go.Figure(data=[go.Table(
    header=dict(values=list(table.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values= [table[colum] for colum in table.columns],
               fill_color='lavender',
               align='left'))],
    layout= layout)
    
    fig.show()

# Create pie chart
def create_pie_chart(table):
    table= table.reset_index()
    fig = px.pie(table, values='Frequency', names='index', title='Pie Chart',
                labels={'index':'Group'})
    fig.show()
    
# Functinon for create bar chart
def create_bar_chart(table):
    table= table.reset_index()
    fig = px.bar(table, y='Frequency', x='index',
                 text='Frequency', labels={'index':'Group'},
                title= 'Bar Chart')
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.show()

# Functinon for describe category variable
def describe_categorical_variable(data, cat_var):
    n_string= int((80 - len(cat_var)) / 2)
    print(formart_text.GREEN + '-' * n_string + cat_var +'-' * n_string + formart_text.END)

    data[cat_var]= pd.Categorical(data[cat_var]) # Convert variable to category

    ## Print describe of variable
    n_record= data.shape[0] # Number of records in dataset
    n_na= data[cat_var].isna().sum() # Number of missing values
    per_na= (n_na * 100)/ n_record # Percentage of missing values
    if int(per_na) == per_na:
        per_na= int(per_na)
    else:
        per_na= round(per_na, 2)
    n_available= data[cat_var].count() # Number of available values
    per_available= (n_available * 100)/ n_record # Percentage of available values
    if int(per_available) == per_available:
        per_available= int(per_available)
    else:
        per_available= round(per_available, 2)

    n_group= data[cat_var].value_counts(dropna= True).shape[0] # Number of distinct values

    print('* Describe:'.upper())
    print('- Number of records in dataset:', n_record)    
    print('- Number of missing values in {cat_var} variable: {n_na} ({per_na}%)'
           .format(cat_var= cat_var, n_na= n_na, per_na= per_na))
    print('- Number of available values in {cat_var} variable: {n_available} ({per_available}%)'
           .format(cat_var= cat_var, n_available= n_available, per_available= per_available))

    print('- Number of group(s) in {cat_var} variable: {n_group}'.format(cat_var= cat_var, n_group= n_group))
    # Warning
    if n_group >= 20:
        print(formart_text.RED + 'Warning: Too much groups for category variable' + formart_text.END)

    ## Print One-Way Table
    print()
    print('* One-Way Table:'.upper())
    # Frequency
    frep_table= data[cat_var].value_counts(dropna= False).rename('Frequency')
    frep_table= pd.DataFrame(frep_table)
    # Percentage
    perc_table= data[cat_var].value_counts(dropna= False, normalize= True).rename('Percentage')
    perc_table= pd.DataFrame(perc_table)
    # Frequency & Percentage
    table= pd.merge(left= frep_table, left_index= True, right= perc_table, right_index= True)
    table.index= table.index.astype(str)
    table['Frequency']= table['Frequency'].apply(lambda x: int(x))
    summary_table= create_summary_table(table)
    print_table(summary_table, index_name= 'Group')
    print('* Visual Chart'.upper())
    if n_group <= 10:
        create_pie_chart(summary_table)
    else:
        create_bar_chart(summary_table)
