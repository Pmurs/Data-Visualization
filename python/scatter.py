import sqlite3
import pandas as pd
import numpy as np
import math

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcol

DB_FILE = "../recruit.db"

try:
    connection = sqlite3.connect(DB_FILE)

    query = "select * from customer"

    df_customer = pd.read_sql(query, connection)
    df_customer.set_index('id', inplace=True)

    print(df_customer.head())

    pairs = df_customer[["youtube_user_rank", "facebook_user_rank"]].as_matrix()
    pairs = [tuple(x) for x in pairs]

    pairs_hash = {}

    for pair in pairs:
        if pair not in pairs_hash:
            pairs_hash[pair] = 1
        else:
            pairs_hash[pair] += 1

    #_, ax = plt.subplots()

    #for key in pairs_hash:
    #    ax.scatter(key[0], key[1], c=pairs_hash[key]/1000, cmap=plt.cm.GnBu)

    #outlier = pairs_hash.pop(('01','01'))

    redpurpleblue = mcol.LinearSegmentedColormap.from_list("MyCmapName",["r","b"])

    xy, z = zip(*pairs_hash.items())
    x, y = zip(*xy)
    z = tuple(map(lambda x: math.sqrt(math.sqrt(x)), z)) # square root scale to dampen the effects of outliers on the colormap
    plt.scatter(x, y, c=z, cmap=plt.cm.Blues)

    plt.title("Heat Map of YouTube and Facebook Usage")
    plt.xlabel("YouTube User Rank")
    plt.ylabel("Facebook User Rank")
    
    plt.show()

    #c.execute(query)
    #for row in c.fetchall():
    #    print(row)

except Exception as e:
    print("Unexpected error:", e)
else:
    connection.close()
