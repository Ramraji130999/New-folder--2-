import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd
import plotly.express as px
import requests
import json
import PIL as Image
from PIL import Image

#sql connection
mydb=psycopg2.connect(host="localhost",
                      user="postgres",
                      port="5432",
                      database="phonepe_data",
                      password="Ramraji")
cursor=mydb.cursor()

#aggregated insurance dataframe
cursor.execute("SELECT * FROM aggregrated_insurance")
mydb.commit()
table1=cursor.fetchall()

aggregrated_insurance=pd.DataFrame(table1,columns=("States","Years","Quarters","Transaction_type","Transaction_count","Transaction_amount"))

#aggregated transaction dataframe
cursor.execute("SELECT * FROM aggregrated_transaction")
mydb.commit()
table2=cursor.fetchall()

aggregrated_transaction=pd.DataFrame(table2,columns=("States","Years","Quarters","Transaction_type","Transaction_count","Transaction_amount"))

#aggregated user dataframe
cursor.execute("SELECT * FROM aggregrated_user")
mydb.commit()
table3=cursor.fetchall()

aggregrated_user=pd.DataFrame(table3,columns=("States","Years","Quarters","Brands","Transaction_count","Percentage"))

#map insurance dataframe
cursor.execute("SELECT * FROM map_insurance")
mydb.commit()
table4=cursor.fetchall()

map_insurance=pd.DataFrame(table4,columns=("States","Years","Quarters","Districts","Transaction_count","Transaction_amount"))

#map transaction dataframe
cursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table5=cursor.fetchall()

map_transaction=pd.DataFrame(table5,columns=("States","Years","Quarters","Districts","Transaction_count","Transaction_amount"))

#map user dataframe
cursor.execute("SELECT * FROM map_user")
mydb.commit()
table6=cursor.fetchall()

map_user=pd.DataFrame(table6,columns=("States","Years","Quarters","Districts","RegisteredUsers","AppOpens"))


#top insurance dataframe
cursor.execute("SELECT * FROM top_insurance")
mydb.commit()
table7=cursor.fetchall()

top_insurance=pd.DataFrame(table7,columns=("States","Years","Quarters","Pincodes","Transaction_count","Transaction_amount"))


#top transaction dataframe
cursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table8=cursor.fetchall()

top_transaction=pd.DataFrame(table8,columns=("States","Years","Quarters","Pincodes","Transaction_count","Transaction_amount"))


#top user dataframe
cursor.execute("SELECT * FROM top_user")
mydb.commit()
table9=cursor.fetchall()

top_user=pd.DataFrame(table9,columns=("States","Years","Quarters","Pincodes","RegisteredUsers"))

#Transaction_year_based_code

def Transaction_amount_count_year(df,year):

   tacy=df[df["Years"]==year]
   tacy.reset_index(drop=True,inplace=True)

   tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
   tacyg.reset_index(inplace=True)

   col1,col2=st.columns(2)
   with col1:

      fig_amount=px.bar(tacyg,x="States",y="Transaction_amount",title=f"{year} TRANSACTION_AMOUNT",color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
      st.plotly_chart(fig_amount)

   with col2:

      fig_count=px.bar(tacyg,x="States",y="Transaction_count",title=f"{year} TRANSACTION_COUNT",color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=600)
      st.plotly_chart(fig_count)

   col1,col2=st.columns(2)

   with col1:
      url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
      response=requests.get(url)
      data1=json.loads(response.content)
      states_name=[]
      for feature in data1["features"]:
         states_name.append(feature["properties"]["ST_NM"])

      states_name.sort()

      fig_india_1=px.choropleth(tacyg,geojson=data1,locations="States",featureidkey="properties.ST_NM",
                              color="Transaction_amount",color_continuous_scale="Rainbow",range_color=(tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                              hover_name="States",title=f"{year} TRANSACTION AMOUNT",fitbounds="locations",
                              height=600,width=600)
      fig_india_1.update_geos(visible=False)
      st.plotly_chart(fig_india_1)

   with col2:
      fig_india_2=px.choropleth(tacyg,geojson=data1,locations="States",featureidkey="properties.ST_NM",
                              color="Transaction_count",color_continuous_scale="Rainbow",range_color=(tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),
                              hover_name="States",title=f"{year} TRANSACTION COUNT",fitbounds="locations",
                              height=600,width=600)
      fig_india_2.update_geos(visible=False)
      st.plotly_chart(fig_india_2)  

   return tacy 

#Transaction_quarter_based_code

def Transaction_amount_count_year_quarter(df,quarter):

   tacy=df[df["Quarters"]==quarter]
   tacy.reset_index(drop=True,inplace=True)

   tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
   tacyg.reset_index(inplace=True)

   col1,col2=st.columns(2)
   with col1:

      fig_amount=px.bar(tacyg,x="States",y="Transaction_amount",title=f"{tacy['Years'].min()} YEAR {quarter} QUARTERS TRANSACTION_AMOUNT",color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
      st.plotly_chart(fig_amount)

   with col2:

      fig_count=px.bar(tacyg,x="States",y="Transaction_count",title=f"{tacy['Years'].min()} YEAR {quarter} QUARTERS TRANSACTION_COUNT",color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=600)
      st.plotly_chart(fig_count)

   col1,col2=st.columns(2)

   with col1:
      url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
      response=requests.get(url)
      data1=json.loads(response.content)
      states_name=[]
      for feature in data1["features"]:
         states_name.append(feature["properties"]["ST_NM"])

      states_name.sort()

      fig_india_1=px.choropleth(tacyg,geojson=data1,locations="States",featureidkey="properties.ST_NM",
                              color="Transaction_amount",color_continuous_scale="Rainbow",range_color=(tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                              hover_name="States",title=f"{tacy['Years'].min()} YEAR {quarter} QUARTERS TRANSACTION AMOUNT",fitbounds="locations",
                              height=600,width=600)
      fig_india_1.update_geos(visible=False)
      st.plotly_chart(fig_india_1)

   with col2:
      fig_india_2=px.choropleth(tacyg,geojson=data1,locations="States",featureidkey="properties.ST_NM",
                              color="Transaction_count",color_continuous_scale="Rainbow",range_color=(tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),
                              hover_name="States",title=f"{tacy['Years'].min()} YEAR {quarter} QUARTERS TRANSACTION COUNT",fitbounds="locations",
                              height=600,width=600)
      fig_india_2.update_geos(visible=False)
      st.plotly_chart(fig_india_2)  

   return tacy

#Transaction_type_based_code
      
def Agg_trans_Trans_type(df,state):

   tacy=df[df["States"]==state]
   tacy.reset_index(drop=True,inplace=True)

   tacyg=tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
   tacyg.reset_index(inplace=True)

   col1,col2=st.columns(2)

   with col1:

      fig_pie_1=px.pie(data_frame=tacyg,names="Transaction_type",values="Transaction_amount",width=600,title=f"{state.upper()} TRANSACTION AMOUNT",hole=0.5)
      st.plotly_chart(fig_pie_1)

   with col2:

      fig_pie_2=px.pie(data_frame=tacyg,names="Transaction_type",values="Transaction_count",width=600,title=f"{state.upper()} TRANSACTION COUNT",hole=0.5)
      st.plotly_chart(fig_pie_2)

#Aggregated user year based code
      
def Aggr_user_year(df,year):
    aguy=df[df["Years"]==year]
    aguy.reset_index(drop=True,inplace=True)

    aguyg=pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace=True)

    fig_bar_1=px.bar(aguyg,x="Brands",y="Transaction_count",title=f"{year} BRANDS AND TRANSACTION COUNT",width=1000,color_discrete_sequence=px.colors.sequential.haline,hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguy   

#Aggregated user quarter based code

def Aggr_user_year_quarter(df,quarter):
    aguyq=df[df["Quarters"]==quarter]
    aguyq.reset_index(drop=True,inplace=True)

    aguyqg=pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace=True)

    fig_bar_1=px.bar(aguyqg,x="Brands",y="Transaction_count",title=f"{quarter} QUARTERS BRANDS AND TRANSACTION COUNT",width=1000,color_discrete_sequence=px.colors.sequential.Magma,hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguyq 

#Aggregated user state wise based code

def Aggr_user_year_quarter_state(df,state): 
   aguyqs=df[df["States"]==state]
   aguyqs.reset_index(drop=True,inplace=True) 

   fig_line_1=px.line(aguyqs,x="Brands",y="Transaction_count",hover_data="Percentage",title=f"{state.upper()} BRANDS, TRANSACTION COUNT, PERCENTAGE",width=1000,markers=True)
   st.plotly_chart(fig_line_1)

#Map Transaction type
def Map_trans_type_Dis(df,state):

   tacy=df[df["States"]==state]
   tacy.reset_index(drop=True,inplace=True)

   tacyg=tacy.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
   tacyg.reset_index(inplace=True)

   col1,col2=st.columns(2)

   with col1:

      fig_bar_1=px.bar(data_frame=tacyg,x="Transaction_amount",y="Districts",orientation="h",height=1000,title=f"{state.upper()} DISTRICTS AND TRANSACTION AMOUNT",color_discrete_sequence=px.colors.sequential.Mint_r)
      st.plotly_chart(fig_bar_1)

   with col2:

      fig_bar_2=px.bar(data_frame=tacyg,x="Transaction_count",y="Districts",orientation="h",height=1000,title=f"{state.upper()} DISTRICTS AND TRANSACTION COUNT",color_discrete_sequence=px.colors.sequential.Blackbody)
      st.plotly_chart(fig_bar_2)  

#map user year based code
def map_user_year(df,year):
    muy=df[df["Years"]==year]
    muy.reset_index(drop=True,inplace=True)

    muyg=muy.groupby("States")[["RegisteredUsers","AppOpens"]].sum()
    muyg.reset_index(inplace=True)

    fig_line_1=px.line(muyg,x="States",y=["RegisteredUsers","AppOpens"],title=f"{year} REGISTER USERS AND APPOPENS ",width=1000,height=800,markers=True)
    st.plotly_chart(fig_line_1)

    return muy  

#map user quarter based code
def map_user_quarter(df,quarter):
    muyq=df[df["Quarters"]==quarter]
    muyq.reset_index(drop=True,inplace=True)

    muyqg=muyq.groupby("States")[["RegisteredUsers","AppOpens"]].sum()
    muyqg.reset_index(inplace=True)

    fig_line_1=px.line(muyqg,x="States",y=["RegisteredUsers","AppOpens"],title=f"{df['Years'].min()} YEAR {quarter} REGISTER USERS AND APPOPENS ",width=1000,height=800,markers=True,color_discrete_sequence=px.colors.sequential.Rainbow)
    st.plotly_chart(fig_line_1)

    return muyq  

#map user state based code
def map_user_states(df,state):
    muyqs=df[df["States"]==state]
    muyqs.reset_index(drop=True,inplace=True)

    col1,col2=st.columns(2)
    with col1:
       
      fig_bar_1=px.bar(muyqs,x="RegisteredUsers",y="Districts",orientation="h",title= f"{states.upper()} REGISTERED USERS",height=800,color_discrete_sequence=px.colors.sequential.Rainbow)
      st.plotly_chart(fig_bar_1)

    with col2:
    
      fig_bar_2=px.bar(muyqs,x="AppOpens",y="Districts",orientation="h",title= f"{states.upper()} APPOPENS",height=800,color_discrete_sequence=px.colors.sequential.Rainbow_r)
      st.plotly_chart(fig_bar_2)

#top insurance state based code   
def top_ins_states(df,state):
    tiy=df[df["States"]==state]
    tiy.reset_index(drop=True,inplace=True)

    col1,col2=st.columns(2)
    with col1:
       
      fig_bar_1=px.bar(tiy,x="Quarters",y="Transaction_amount",hover_data="Pincodes",title= "TRANSACTION AMOUNT",height=650,width=600,color_discrete_sequence=px.colors.sequential.Rainbow)
      st.plotly_chart(fig_bar_1)

    with col2:
    
      fig_bar_2=px.bar(tiy,x="Quarters",y="Transaction_count",hover_data="Pincodes",title= "TRANSACTION COUNT",height=650,width=600,color_discrete_sequence=px.colors.sequential.Rainbow_r)
      st.plotly_chart(fig_bar_2)

#top user year based code   
def top_user_year(df,year):
    tuy=df[df["Years"]==year]
    tuy.reset_index(drop=True,inplace=True)

    tuyg = pd.DataFrame(tuy.groupby(["States", "Quarters"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace=True)

    fig_bar_1=px.bar(tuyg,x="States",y="RegisteredUsers",color="Quarters",hover_name="States",color_discrete_sequence=px.colors.sequential.Bluyl,title=f"{year} REGISTER USERS",width=1000,height=800)
    st.plotly_chart(fig_bar_1)

    return tuy 

#top user state based code
def top_user_states(df,state):
    tuys=df[df["States"]==state]
    tuys.reset_index(drop=True,inplace=True)

       
    fig_bar_1=px.bar(tuys,x="Quarters",y="RegisteredUsers",hover_data="Pincodes",color="RegisteredUsers",title= "REGISTERED USERS, PINCODES AND QUARTERS",height=800,width=1000,color_continuous_scale=px.colors.sequential.Magma)
    st.plotly_chart(fig_bar_1)

#Question query transaction amount related code
def top_chart_transaction_amount(table_name):
#sql connection
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe_data",
                        password="Ramraji")
    cursor=mydb.cursor()

    #Question 1 query:
    query1=f'''SELECT states,SUM(transaction_amount) AS transaction_amount
            FROM {table_name}
            GROUP BY states
            ORDER BY transaction_amount DESC
            LIMIT 10;'''

    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1,columns=("states","transaction_amount"))

    col1,col2=st.columns(2)
    with col1:

      fig_bar_1=px.bar(df_1,x="states",y="transaction_amount",title="TOP LIST 10 STATES AND TRANSACTION AMOUNT",hover_name="states",color_discrete_sequence=px.colors.sequential.Agsunset_r,height=650,width=600)
      st.plotly_chart(fig_bar_1)

    #Question 2 query:
    query2=f'''SELECT states,SUM(transaction_amount) AS transaction_amount
            FROM {table_name}
            GROUP BY states
            ORDER BY transaction_amount 
            LIMIT 10;'''

    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2,columns=("states","transaction_amount"))

    with col2:

     fig_bar_2=px.bar(df_2,x="states",y="transaction_amount",title="LIST 10 STATES AND TRANSACTION AMOUNT",hover_name="states",color_discrete_sequence=px.colors.sequential.Magenta_r,height=650,width=600)
     st.plotly_chart(fig_bar_2)

    #Question 3 query:
    query3=f'''SELECT states,AVG(transaction_amount) AS transaction_amount
            FROM {table_name}
            GROUP BY states
            ORDER BY transaction_amount;'''

    cursor.execute(query3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3,columns=("states","transaction_amount"))

    fig_bar_3=px.bar(df_3,x="transaction_amount",y="states",orientation="h",title="AVERAGE OF TRANSACTION AMOUNT",hover_name="states",color_discrete_sequence=px.colors.sequential.Blackbody,height=800,width=1000)
    st.plotly_chart(fig_bar_3)  

#Question query transaction count related code
def top_chart_transaction_count(table_name):
#sql connection
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe_data",
                        password="Ramraji")
    cursor=mydb.cursor()

    #Question 1 query:
    query1=f'''SELECT states,SUM(transaction_count) AS transaction_count
            FROM {table_name}
            GROUP BY states
            ORDER BY transaction_count DESC
            LIMIT 10;'''

    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1,columns=("states","transaction_count"))

    col1,col2=st.columns(2)
    with col1:

      fig_bar_1=px.bar(df_1,x="states",y="transaction_count",title="TOP LIST 10 STATES AND TRANSACTION COUNT",hover_name="states",color_discrete_sequence=px.colors.sequential.Agsunset,height=650,width=600)
      st.plotly_chart(fig_bar_1)

    #Question 2 query:
    query2=f'''SELECT states,SUM(transaction_count) AS transaction_count
            FROM {table_name}
            GROUP BY states
            ORDER BY transaction_count 
            LIMIT 10;'''

    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2,columns=("states","transaction_count"))

    with col2:

     fig_bar_2=px.bar(df_2,x="states",y="transaction_count",title="LIST 10 STATES AND TRANSACTION COUNT",hover_name="states",color_discrete_sequence=px.colors.sequential.Magenta,height=650,width=600)
     st.plotly_chart(fig_bar_2)

    #Question 3 query:
    query3=f'''SELECT states,AVG(transaction_count) AS transaction_count
            FROM {table_name}
            GROUP BY states
            ORDER BY transaction_count;'''

    cursor.execute(query3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3,columns=("states","transaction_count"))

    fig_bar_3=px.bar(df_3,x="transaction_count",y="states",orientation="h",title="AVERAGE OF TRANSACTION COUNT",hover_name="states",color_discrete_sequence=px.colors.sequential.Blackbody_r,height=800,width=1000)
    st.plotly_chart(fig_bar_3)    

#Question query transaction count related code
def top_chart_registered_users(table_name,states):
#sql connection
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe_data",
                        password="Ramraji")
    cursor=mydb.cursor()

    #Question 1 query:
    query1=f'''SELECT districts,SUM(registeredusers) AS registeredusers
            FROM {table_name}
            WHERE states= '{states}'
            GROUP BY districts
            ORDER BY registeredusers DESC
            LIMIT 10;'''

    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1,columns=("districts","registeredusers"))

    col1,col2=st.columns(2)
    with col1:

      fig_bar_1=px.bar(df_1,x="districts",y="registeredusers",title="TOP LIST 10 DISTRICTS AND REGISTERED USERS",hover_name="districts",color_discrete_sequence=px.colors.sequential.Agsunset,height=650,width=600)
      st.plotly_chart(fig_bar_1)

    #Question 2 query:
    query2=f'''SELECT districts,SUM(registeredusers) AS registeredusers
            FROM {table_name}
            WHERE states= '{states}'
            GROUP BY districts
            ORDER BY registeredusers 
            LIMIT 10;'''

    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2,columns=("districts","registeredusers"))

    with col2:

     fig_bar_2=px.bar(df_2,x="districts",y="registeredusers",title="LAST 10 DISTRICTS AND REGISTERED USERS",hover_name="districts",color_discrete_sequence=px.colors.sequential.Magenta,height=650,width=600)
     st.plotly_chart(fig_bar_2)

#Question 3 query:
    query3=f'''SELECT districts,AVG(registeredusers) AS registeredusers
            FROM {table_name}
            WHERE states='{states}'
            GROUP BY districts
            ORDER BY registeredusers;'''

    cursor.execute(query3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3,columns=("districts","registeredusers"))

    fig_bar_3=px.bar(df_3,y="districts",x="registeredusers",orientation="h",title="AVERAGE OF REGISTERED USERS",hover_name="districts",color_discrete_sequence=px.colors.sequential.Blackbody_r,height=800,width=1000)
    st.plotly_chart(fig_bar_3)

#Question query transaction count related code
def top_chart_appopens(table_name,states):
#sql connection
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe_data",
                        password="Ramraji")
    cursor=mydb.cursor()

    #Question 1 query:
    query1=f'''SELECT districts,SUM(appopens) AS appopens
            FROM {table_name}
            WHERE states= '{states}'
            GROUP BY districts
            ORDER BY appopens DESC
            LIMIT 10;'''

    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1,columns=("districts","appopens"))

    col1,col2=st.columns(2)
    with col1:

      fig_bar_1=px.bar(df_1,x="districts",y="appopens",title="TOP LIST 10 DISTRICTS AND APPOPENS",hover_name="districts",color_discrete_sequence=px.colors.sequential.Agsunset,height=650,width=600)
      st.plotly_chart(fig_bar_1)

    #Question 2 query:
    query2=f'''SELECT districts,SUM(appopens) AS appopens
            FROM {table_name}
            WHERE states= '{states}'
            GROUP BY districts
            ORDER BY appopens 
            LIMIT 10;'''

    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2,columns=("districts","appopens"))

    with col2:

     fig_bar_2=px.bar(df_2,x="districts",y="appopens",title="LAST 10 DISTRICTS AND APPOPENS",hover_name="districts",color_discrete_sequence=px.colors.sequential.Magenta,height=650,width=600)
     st.plotly_chart(fig_bar_2)

#Question 3 query:
    query3=f'''SELECT districts,AVG(appopens) AS appopens
            FROM {table_name}
            WHERE states='{states}'
            GROUP BY districts
            ORDER BY appopens;'''

    cursor.execute(query3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3,columns=("districts","appopens"))

    fig_bar_3=px.bar(df_3,y="districts",x="appopens",orientation="h",title="AVERAGE OF APPOPENS",hover_name="districts",color_discrete_sequence=px.colors.sequential.Blackbody_r,height=800,width=1000)
    st.plotly_chart(fig_bar_3)  

#Question query transaction count related code
def top_chart_registered_users_top(table_name):
#sql connection
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe_data",
                        password="Ramraji")
    cursor=mydb.cursor()

    #Question 1 query:
    query1=f'''SELECT states,SUM(registeredusers) AS registeredusers
            FROM {table_name}
            GROUP BY states
            ORDER BY registeredusers DESC
            LIMIT 10;'''

    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1,columns=("states","registeredusers"))

    col1,col2=st.columns(2)
    with col1:

      fig_bar_1=px.bar(df_1,x="states",y="registeredusers",title="TOP LIST 10 REGISTERED USERS",hover_name="states",color_discrete_sequence=px.colors.sequential.Agsunset,height=650,width=600)
      st.plotly_chart(fig_bar_1)

    #Question 2 query:
    query2=f'''SELECT states,SUM(registeredusers) AS registeredusers
            FROM {table_name}
            GROUP BY states
            ORDER BY registeredusers 
            LIMIT 10;'''

    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2,columns=("states","registeredusers"))

    with col2:

     fig_bar_2=px.bar(df_2,x="states",y="registeredusers",title="LAST 10 REGISTERED USERS",hover_name="states",color_discrete_sequence=px.colors.sequential.Magenta,height=650,width=600)
     st.plotly_chart(fig_bar_2)

#Question 3 query:
    query3=f'''SELECT states,AVG(registeredusers) AS registeredusers
            FROM {table_name}
            GROUP BY states
            ORDER BY registeredusers;'''

    cursor.execute(query3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3,columns=("states","registeredusers"))

    fig_bar_3=px.bar(df_3,y="states",x="registeredusers",orientation="h",title="AVERAGE OF REGISTERED USERS",hover_name="states",color_discrete_sequence=px.colors.sequential.Blackbody_r,height=800,width=1000)
    st.plotly_chart(fig_bar_3)

#streamlit visualization part

st.set_page_config(layout= "wide")
st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")

with st.sidebar:

   select=option_menu("MAIN MENU",["HOME","DATA EXPLORATION","TOP CHARTS"])

if select=="HOME":
      
      col1,col2=st.columns(2)

      with col1:
       st.header("PHONEPE")
       st.subheader("INDIA'S BEST TRANSACTION APP")
       st.markdown("PhonePe - India's Payment App. PhonePe is a mobile payment platform using which you can transfer money using UPI, recharge phone numbers, pay utility bills, etc. PhonePe works on the Unified Payment Interface (UPI) system and all you need is to feed in your bank account details and create a UPI ID")
       st.write("****FEATURES****")
       st.write("****CREDIT AND DEBIT CARD LINKING****")
       st.write("****RECHARGE AND PAY BILLS****")
       st.write("****CHECK BANK BALANCE****")
       st.write("****TRANSFER MONEY TO BANK OR UPI ID****")
       st.write("****TRAVEL BOOKINGS****")
       st.write("****INSURANCE FOR CAR,BIKE AND HEALTH****")
       st.write("****PIN AUTHORIZATION****")
       st.download_button("DOWNLOAD THE APP NOW","https://www.phonepe.com/app-download/")

      with col2:
       st.image(Image.open(r"C:\Users\nandh\Desktop\New folder (2)\app_download_for_all_web-2x.png"),width=500)

      col3,col4=st.columns(2) 

      with col3:
       st.video(r"C:\Users\nandh\Desktop\New folder (2)\WhatsApp Video 2024-03-21 at 10.41.52 PM.mp4")

      with col4:
        st.write("****Easy Transactions****")
        st.write("****One App for all payments****")
        st.write("****QR COde for easy tranfers****")
        st.write("****Earn Great Rewards****") 
        
elif select=="DATA EXPLORATION":
      
      tab1,tab2,tab3=st.tabs(["Aggregrated Analysis","Map Analysis","Top Analysis"])

      with tab1:

         method_1=st.radio("Select The Method",["Aggregrated Insurance","Aggregrated Transaction","Aggregrated User"])

         if method_1=="Aggregrated Insurance":

            col1,col2=st.columns(2)

            with col1:
             years_ins=st.slider("Select The Year_ins",aggregrated_insurance["Years"].min(),aggregrated_insurance["Years"].max(),aggregrated_insurance["Years"].min())
            tacy_Y_ins=Transaction_amount_count_year(aggregrated_insurance,years_ins)

            col1,col2=st.columns(2)

            with col1:
             quarters_ins=st.slider("Select The Quarter_ins",tacy_Y_ins["Quarters"].min(),tacy_Y_ins["Quarters"].max(),tacy_Y_ins["Quarters"].min())
            tacy_Y_Q=Transaction_amount_count_year_quarter(tacy_Y_ins,quarters_ins)

         elif method_1=="Aggregrated Transaction":

            col1,col2=st.columns(2)

            with col1:
             years_trans=st.slider("Select The Year_trans",aggregrated_transaction["Years"].min(),aggregrated_transaction["Years"].max(),aggregrated_transaction["Years"].min())
            tacy_Y_trans=Transaction_amount_count_year(aggregrated_transaction,years_trans)

            col1,col2=st.columns(2)

            with col1:
             states=st.selectbox("Select The State",tacy_Y_trans["States"].unique())
            Agg_trans_Trans_type(tacy_Y_trans,states)

            col1,col2=st.columns(2)

            with col1:
             quarters_trans=st.slider("Select The Quarter_trans",tacy_Y_trans["Quarters"].min(),tacy_Y_trans["Quarters"].max(),tacy_Y_trans["Quarters"].min())
            tacy_Y_trans_quarter=Transaction_amount_count_year_quarter(tacy_Y_trans,quarters_trans)

            col1,col2=st.columns(2)

            with col1:
             states=st.selectbox("Select The State_Type",tacy_Y_trans_quarter["States"].unique())
            Agg_trans_Trans_type(tacy_Y_trans_quarter,states)

         elif method_1=="Aggregrated User":
            col1,col2=st.columns(2)

            with col1:
             years_user=st.slider("Select The Year_user",aggregrated_user["Years"].min(),aggregrated_user["Years"].max(),aggregrated_user["Years"].min())
            tacy_Y_user=Aggr_user_year(aggregrated_user,years_user)

            col1,col2=st.columns(2)

            with col1:
             quarters_user=st.slider("Select The Quarter_user",tacy_Y_user["Quarters"].min(),tacy_Y_user["Quarters"].max(),tacy_Y_user["Quarters"].min())
            tacy_Y_user_Q=Aggr_user_year_quarter(tacy_Y_user,quarters_user)

            col1,col2=st.columns(2)

            with col1:
             states=st.selectbox("Select The State",tacy_Y_user_Q["States"].unique())
            Aggr_user_year_quarter_state(tacy_Y_user_Q,states)

      with tab2:

         method_2=st.radio("Select The Method",["Map Insurance","Map Transaction","Map User"])      

         if method_2=="Map Insurance":
            col1,col2=st.columns(2)

            with col1:
             years_map=st.slider("Select The Year_map",map_insurance["Years"].min(),map_insurance["Years"].max(),map_insurance["Years"].min())
            map_ins_year=Transaction_amount_count_year(map_insurance,years_map)

            col1,col2=st.columns(2)

            with col1:
             states=st.selectbox("Select The State_Dis",map_ins_year["States"].unique())
            Map_trans_type_Dis(map_ins_year,states)

            col1,col2=st.columns(2)

            with col1:
             quarters=st.slider("Select The Quarter_in",map_ins_year["Quarters"].min(),map_ins_year["Quarters"].max(),map_ins_year["Quarters"].min())
            map_ins_year_quarter=Transaction_amount_count_year_quarter(map_ins_year,quarters)

            col1,col2=st.columns(2)

            with col1:
             states=st.selectbox("Select The State_Type",map_ins_year_quarter["States"].unique())
            Map_trans_type_Dis(map_ins_year_quarter,states)

         elif method_2=="Map Transaction":
            col1,col2=st.columns(2)

            with col1:
             years=st.slider("Select The Year",map_transaction["Years"].min(),map_transaction["Years"].max(),map_transaction["Years"].min())
            map_trans_year=Transaction_amount_count_year(map_transaction,years)

            col1,col2=st.columns(2)

            with col1:
             states=st.selectbox("Select The State_Dis",map_trans_year["States"].unique())
            Map_trans_type_Dis(map_trans_year,states)

            col1,col2=st.columns(2)

            with col1:
             quarters=st.slider("Select The Quarter_tr",map_trans_year["Quarters"].min(),map_trans_year["Quarters"].max(),map_trans_year["Quarters"].min())
            map_trans_year_quarter=Transaction_amount_count_year_quarter(map_trans_year,quarters)

            col1,col2=st.columns(2)

            with col1:
             states=st.selectbox("Select The State_Type",map_trans_year_quarter["States"].unique())
            Map_trans_type_Dis(map_trans_year_quarter,states)

         elif method_2=="Map User":
            col1,col2=st.columns(2)

            with col1:
             years=st.slider("Select The Year_user",map_user["Years"].min(),map_user["Years"].max(),map_user["Years"].min())
            map_user_Y=map_user_year(map_user,years)

            col1,col2=st.columns(2)

            with col1:
             quarters=st.slider("Select The Quarter_us",map_user_Y["Quarters"].min(),map_user_Y["Quarters"].max(),map_user_Y["Quarters"].min())
            map_user_year_quarter=map_user_quarter(map_user_Y,quarters)

            col1,col2=st.columns(2)

            with col1:
             states=st.selectbox("Select The State_mu",map_user_year_quarter["States"].unique())
            map_user_states(map_user_year_quarter,states)


      with tab3:

         method_3=st.radio("Select The Method",["Top Insurance","Top Transaction","Top User"])      

         if method_3=="Top Insurance":

            col1,col2=st.columns(2)

            with col1:
             years_top=st.slider("Select The Year_top",top_insurance["Years"].min(),top_insurance["Years"].max(),top_insurance["Years"].min())
            top_ins_year=Transaction_amount_count_year(top_insurance,years_top)

            col1,col2=st.columns(2)

            with col1:
             states=st.selectbox("Select The State_ti",top_ins_year["States"].unique())
            top_ins_states(top_ins_year,states)

            col1,col2=st.columns(2)

            with col1:
             quarters=st.slider("Select The Quarter_ti",top_ins_year["Quarters"].min(),top_ins_year["Quarters"].max(),top_ins_year["Quarters"].min())
            top_user_year_quarter=Transaction_amount_count_year_quarter(top_ins_year,quarters)

         elif method_3=="Top Transaction":
            col1,col2=st.columns(2)

            with col1:
             years_top=st.slider("Select The Year_top",top_transaction["Years"].min(),top_transaction["Years"].max(),top_transaction["Years"].min())
            top_trans_year=Transaction_amount_count_year(top_transaction,years_top)

            col1,col2=st.columns(2)

            with col1:
             states=st.selectbox("Select The State_tt",top_trans_year["States"].unique())
            top_ins_states(top_trans_year,states)

            col1,col2=st.columns(2)

            with col1:
             quarters=st.slider("Select The Quarter_tt",top_trans_year["Quarters"].min(),top_trans_year["Quarters"].max(),top_trans_year["Quarters"].min())
            top_trans_year_quarter=Transaction_amount_count_year_quarter(top_trans_year,quarters)

         elif method_3=="Top User":

            col1,col2=st.columns(2)

            with col1:
             years_top=st.slider("Select The Year_top",top_user["Years"].min(),top_user["Years"].max(),top_user["Years"].min())
            top_user_Y=top_user_year(top_user,years_top)  

            col1,col2=st.columns(2)

            with col1:
             states=st.selectbox("Select The State_tU",top_user_Y["States"].unique())
            top_user_states(top_user_Y,states)   

elif select== "TOP CHARTS":
   question=st.selectbox("SELECT THE QUESTIONS",["1.Transaction Amount and Count of Aggregrated Insurance",
                                                   "2.Transaction Amount and Count of Map Insurance",
                                                   "3.Transaction Amount and Count of Top Insurance",
                                                   "4.Transaction Amount and Count of Aggregrated Transaction",
                                                   "5.Transaction Amount and Count of Map Transaction",
                                                   "6.Transaction Amount and Count of Top Transaction",
                                                   "7.Transaction Count of Aggregrated user",
                                                   "8.Registered users of Map user",
                                                   "9.App Opens of Map user",
                                                   "10.Registered users of Top user"])
   
   if question== "1.Transaction Amount and Count of Aggregrated Insurance":

     st.subheader("TRANSACTION AMOUNT")
     top_chart_transaction_amount("aggregrated_insurance") 

     st.subheader("TRANSACTION COUNT")  
     top_chart_transaction_count("aggregrated_insurance")

   elif question== "2.Transaction Amount and Count of Map Insurance":

     st.subheader("TRANSACTION AMOUNT")
     top_chart_transaction_amount("map_insurance") 

     st.subheader("TRANSACTION COUNT")  
     top_chart_transaction_count("map_insurance") 

   elif question== "3.Transaction Amount and Count of Top Insurance":

     st.subheader("TRANSACTION AMOUNT")
     top_chart_transaction_amount("top_insurance") 

     st.subheader("TRANSACTION COUNT")  
     top_chart_transaction_count("top_insurance")     

   elif question== "4.Transaction Amount and Count of Aggregrated Transaction":

     st.subheader("TRANSACTION AMOUNT")
     top_chart_transaction_amount("aggregrated_transaction") 

     st.subheader("TRANSACTION COUNT")  
     top_chart_transaction_count("aggregrated_transaction")  

   elif question== "5.Transaction Amount and Count of Map Transaction":

     st.subheader("TRANSACTION AMOUNT")
     top_chart_transaction_amount("map_transaction") 

     st.subheader("TRANSACTION COUNT")  
     top_chart_transaction_count("map_transaction")  

   elif question== "6.Transaction Amount and Count of Top Transaction":

     st.subheader("TRANSACTION AMOUNT")
     top_chart_transaction_amount("top_transaction") 

     st.subheader("TRANSACTION COUNT")  
     top_chart_transaction_count("top_transaction")        

   elif question== "7.Transaction Count of Aggregrated user": 

     st.subheader("TRANSACTION COUNT")  
     top_chart_transaction_count("aggregrated_user") 

   elif question== "8.Registered users of Map user": 

     states=st.selectbox("SELECT THE STATE_MU",map_user["States"].unique())
     st.subheader("REGISTERED USERS")  
     top_chart_registered_users("map_user",states)   

   elif question== "9.App Opens of Map user": 

     states=st.selectbox("SELECT THE STATE_MU",map_user["States"].unique())
     st.subheader("APPOPENS")  
     top_chart_appopens("map_user",states)   

   elif question== "10.Registered users of Top user": 

     st.subheader("REGISTERED USERS TOP")  
     top_chart_registered_users_top("top_user")      