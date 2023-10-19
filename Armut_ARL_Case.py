#####################################################
# PROJECT : ARMUT Association RUle Learning
# ABOUT DATA SET
# UserId         int64 : Customer ID
# ServiceId      int64 : Service ID, service id dependent to category id.
# CategoryId     int64 : Category ID
# CreateDate    object : Timestamp
#####################################################


# imports and settings
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.width', 500)
pd.set_option('display.expand_frame_repr', False)
from mlxtend.frequent_patterns import apriori, association_rules
from Src.utils import check_df
from Src.utils import grab_col_names

"""DUTY 1 : Prepare Data """
"""Stage 1 : Read armut_data.csv"""
df_ = pd.read_csv("Datasets/armut_data.csv")
df = df_.copy()
""" Examine Data """
check_df(df)
df.describe(np.arange(0.1,1,0.1)).T
df.head()
############ veri görselleştir.
df.hist()
plt.show(block=True)
########################
"""Stage 2: Add dataframe a new  variable by join Categori and service id. hizmet = ServiceID_CategoryID"""
df["Hizmet"] = df.apply(lambda x: str(x["ServiceId"]) + "_" + str(x["CategoryId"]) , axis=1)
"""Stage 3 : create a new variable New_Date as following format New_date = date  = for createDate """
df["New_Date"] = df.apply(lambda x: str(pd.to_datetime(x["CreateDate"]).year) + "-" + str(pd.to_datetime(x["CreateDate"]).month), axis= 1)
df["SepetID"] = df.apply(lambda x: str(x["UserId"]) + "_" + str(x["New_Date"]) , axis=1 )

###############################################################
# DUTY 2 : Create Association Rules and Recommend customers.
###############################################################.
"""Stage 1: Create a pivot table that includes SepetID values in the rows and Hizmet values in the columns """
pvt_df = df.groupby(["SepetID","Hizmet"]).agg({"UserId":"count"}). \
             unstack(). \
             fillna(0). \
             applymap(lambda x: 1 if x > 0 else 0)
pvt_df.columns = pvt_df.columns.droplevel(0)

#####################################################
# test = pd.pivot_table(data=df, index=["SepetID"],columns=["Hizmet"],values="UserId",aggfunc=["count"])
# test = test.applymap(lambda x: 1 if x > 0 else 0)
# test.columns = test.columns.droplevel(0)
####################################################

## for test  pvt_df.iloc[0:10,0:20]
"""Stage 2 : Create association rules """
frequent_hizmetlist = apriori(pvt_df,
                            min_support=0.01,
                            use_colnames=True)
frequent_hizmetlist.head()
frequent_hizmetlist.sort_values("support", ascending=False)

rules = association_rules(frequent_hizmetlist,
                          metric="support",
                          min_threshold=0.01)

rules.head()
rules[(rules["support"]>0.01) & (rules["confidence"]>0.1) & (rules["lift"]>2)]

def arl_recommender(rules_df, product_id, rec_count=1):
    sorted_rules = rules_df.sort_values("lift", ascending=False)
    recommendation_list = []
    for i, product in enumerate(sorted_rules["antecedents"]):
        for j in list(product):
            if j == product_id:
                recommendation_list.append(list(sorted_rules.iloc[i]["consequents"])[0])
    return recommendation_list[0:rec_count]

arl_recommender(rules,"2_0",2) ## recommended_service_list : 22_0 , 25_0

