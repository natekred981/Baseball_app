import mysql.connector as msql
import pandas as pd

"""
connect_database: connects to the mysql database created from the 
                  lahman2016 database built via the the queries
                  listed in the db directory

create_table: pulls data from different player statistics and 
              organizes it into one dataframe

"""
def connect_database():
    mydb = msql.connect(
        host="localhost",
        user="root",
        passwd=",s;s_ghi&9=A",
        database="lahman2016"
    )
    return mydb

def create_table():
    mydb = connect_database()
    """First SQL_Query designed to QUERY batting statistics
       Three additional statistics are added to the dataframe

       Second SQL_Query designed to QUERY pitching statistics
       One additional statistic added

       Third SQL_Query holds the classifications as either a
       player who was nominated for the hall of fame or a player
       who was not

       The dataframes are then merged
             """
    SQL_Query = pd.read_sql_query(
        ''' SELECT
            playerID,count(yearID) as years, floor(avg(yearID)) as era_of_play, sum(G) as G,sum(AB) as AB,sum(H) as H,sum(2B) as 2B,sum(3B) as 3B,sum(HR) as HR,sum(RBI) as RBI,sum(SB) as SB,sum(BB) as BB FROM
            Batting 
            group by playerID''', mydb
    )
    # creating three other columns out of pre-existin columns
    df = pd.DataFrame(SQL_Query)
    df["AVG"] = (df["H"])/(df["AB"])
    df["OBP"] = (df['H'] + df['BB']) / (df['AB'] + df["BB"])
    df['SLG'] = ((df['H'] - df['2B'] - df['3B'] - df['HR']) +
                df['2B'] * 2 + df['3B']*3 + df['HR']*4)/(df["AB"])

    # pitching statistics
    SQL_Query = pd.read_sql_query(
        ''' SELECT
            playerID, sum(W) as W, sum(GS) as GS, sum(SV) as SV, sum(SO) as SO, AVG(ERA) as ERA, sum(BB) as BB, sum(H) as H, sum(IPouts/3) as IP FROM
            Pitching 
            group by playerID''', mydb
    )
    df2 = pd.DataFrame(SQL_Query)
    df2['WHIP'] = (df2['BB'] + df2['H'])/df2['IP']
    SQL_Query = pd.read_sql_query(
        ''' SELECT playerID FROM HallOfFame where  (category = 'Player' and votedBy = "BBWAA") or (votedBy = "Veterans" and category='Player')
        ''', mydb
    )
    df3 = pd.DataFrame(SQL_Query)
    
    df = pd.merge(
        df,
        df2,
        how="outer",
        on="playerID")
    df = df.drop(columns=['BB_y', 'H_y', 'IP'])
    df['nominated'] = (df['playerID'].isin(df3['playerID'])).astype(int)
    df = df.fillna(0)
    players = df['playerID']
    df = df.drop(columns=['playerID'])

    df.to_csv("thedata.csv")
    return(df,players)
