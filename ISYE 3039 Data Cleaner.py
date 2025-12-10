import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as plx

def csv_cleaner(input_file):
    # Reading the input file
    df = pd.read_csv(input_file)

    # Filtering by Pollutant and State
    df = df[df["Defining Parameter"]=="Ozone"]
    # print(df["Defining Parameter"])
    df = df[df["state_name"]=="Georgia"]
    df = df[df["city_ascii"].isin(["Atlanta","Macon","Athens","Americus"])]

    # Removing Unnecessary Columns
    df = df.dropna(inplace=False, axis=0)
    df.reset_index(inplace=True)
    df.drop(["index","Unnamed: 0","CBSA Code","Category","Number of Sites Reporting","state_id","state_name","lat","lng","population","density","timezone"],axis=1,inplace=True)
    # print(df)

    # Getting Weekly AQI
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.groupby(["city_ascii","Defining Parameter",pd.Grouper(key="Date", freq='W')]).mean()
    # df.set_index("city_ascii",inplace=True)
    # print(df[["AQI","city_ascii"]].groupby("city_ascii").mean())
    # df["Weekly Avg."] = df["AQI"].mean()
    # weekly = df.groupby("city_ascii",pd.Grouper(key="Date",freq="W")).mean()
    df.reset_index(inplace=True)
    print(df)
    
    # Saving Cleaned File
    df.to_csv("cleaned_US_AQI.csv",index=False)

# csv_cleaner("US_AQI.csv")

def data_visualizer(input_file):
    df = pd.read_csv(input_file)
    # print(df)
    fig1 = plx.line(df[df["city_ascii"]=="Americus"],x="Date",y="AQI",color="city_ascii")
    fig2 = plx.line(df[df["city_ascii"]=="Athens"],x="Date",y="AQI",color="city_ascii")
    fig3 = plx.line(df[df["city_ascii"]=="Atlanta"],x="Date",y="AQI",color="city_ascii")
    fig4 = plx.line(df[df["city_ascii"]=="Macon"],x="Date",y="AQI",color="city_ascii")
    fig1.show()
    fig2.show()
    fig3.show()
    fig4.show()

# data_visualizer("cleaned_US_AQI.csv")

def data_stats(input_file):
    df = pd.read_csv(input_file)
    for i in ["Americus","Athens","Atlanta","Macon"]:
        print(f"{i}'s AQI Mean is: {df[df['city_ascii']==i]["AQI"].mean()}")
        print(f"{i}'s AQI STD is: {df[df['city_ascii']==i]["AQI"].std()}")
        print(f"{i}'s AQI Min. is: {df[df['city_ascii']==i]["AQI"].min()}")
        print(f"{i}'s AQI Max. is: {df[df['city_ascii']==i]["AQI"].max()}")

# data_stats("cleaned_US_AQI.csv")

def histogram(input_file):
    df = pd.read_csv(input_file)
    for i in ["Americus","Athens","Atlanta","Macon"]:
        fig = plx.histogram(df[df["city_ascii"]==i],x="AQI",color="city_ascii")
        fig.show()

histogram("cleaned_US_AQI.csv")