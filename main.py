import streamlit as st
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.expand_frame_repr', False)


def outlier_thresholds(dataframe, variable):
    quartile1 = dataframe[variable].quantile(0.01)
    quartile3 = dataframe[variable].quantile(0.99)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return low_limit, up_limit
def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit

def get_stock_name(dataframe, stock_code):
    product_name = dataframe[dataframe["StockCode"] == stock_code][["Description"]].values[0].tolist()
    return product_name

def arl_recommender(rules_df, xproduct_id, rec_count=1):
    sorted_rules = rules_df.sort_values("lift", ascending=False)
    recommendation_list = set()
    for i, product in enumerate(sorted_rules["antecedents"]):
        for j in list(product):
            if j == xproduct_id:
                recommendation_list.add(list(sorted_rules.iloc[i]["consequents"])[0])

    return list(recommendation_list)[0:rec_count]

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    st.set_page_config(
        page_title="ARL Recommendation",
        layout="centered",
        initial_sidebar_state="expanded",
    )
    st.title('ARL Based Recommender System')
    st.header("İş Problemi")
    st.markdown(
        """        
        Aşağıda 3 farklı kullanıcının sepet bilgileri verilmiştir. Bu sepet bilgilerine en
        uygun ürün önerisini birliktelik kuralı kullanarak yapınız. Ürün önerileri 1 tane
        ya da 1'den fazla olabilir. Karar kurallarını 2010-2011 Germany müşterileri
        üzerinden türetiniz. Örnek ürün idleri : (21987 , 23235 ,  22747)
        ***
        """
    )
    st.image("sepet2.png", width=300)
    ###################################################
    # Read Data and Prepare
    ###################################################
    df_ = pd.read_excel("datasets/online_retail_II.xlsx",sheet_name="Year 2010-2011")
    df = df_.copy()

    df.dropna(inplace=True)
    df = df[df["StockCode"] != "POST"]
    df = df[~df["Invoice"].str.contains("C", na=False)]
    df = df[df["Quantity"] > 0]
    df = df[df["Price"] > 0]
    replace_with_thresholds(df, "Quantity")
    replace_with_thresholds(df, "Price")

    # i query for German customers.
    dfg = df[df['Country'] == "Germany"]
    # i create a pivot table for invoice,stockcode matrix.
    inv_stock_pvt = dfg.pivot_table(index="Invoice", columns="StockCode", values="Quantity", aggfunc="sum")
    inv_stock_pvt = inv_stock_pvt.fillna(0).applymap(lambda x: 1 if x > 0 else 0)
    # for test
##    inv_stock_pvt.iloc[0:25, 0:10]

    ############################################
    # 3. Get Association Rules.
    ############################################
    frequent_itemsets = apriori(inv_stock_pvt,
                                min_support=0.01,
                                use_colnames=True)

    frequent_itemsets.sort_values("support", ascending=False)

    rules = association_rules(frequent_itemsets,
                              metric="support",
                              min_threshold=0.01)

    #rules.shape  ## 18370
    rules.sort_values("support", ascending=False)
    rules.sort_values("confidence", ascending=False)

    ## rules[(rules["support"]>0.05) & (rules["confidence"]>0.1) & (rules["lift"]>5)] only 2 records.

    ############################################
    # 5. Recommend products
    ############################################
    ### sample products 21987,23235,22747
    sample_list = [21987, 23235, 22747]

    for sample in sample_list:
        product_desc = get_stock_name(dfg, sample)
        st.write("********************************************************************")
        st.write(f"Recommendation List for {sample} - {product_desc} ")
        recommended_list = arl_recommender(rules, sample, 3)
        for skod in recommended_list:
            sdesc = get_stock_name(dfg, skod)
            st.write(f"{skod} - {sdesc}")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
