# Import python packages
import streamlit as st
import os
import pandas as pd
from snowflake.snowpark.functions import col
from snowflake.snowpark.functions import when_matched

conn = st.connection("snowflake", ttl=os.getenv("SNOWFLAKE_CONNECTION_TTL"))
session = conn.session()
cnx = st.connection("snowflake")
session = cnx.session()


st.title("Customize Your Smoothie :smile:")
st.write("Pick the fruit you want in your custom smoothie")

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your smoothie will be:', name_on_order)

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe, max_selections=5)

if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    my_insert_stmt = """INSERT INTO smoothies.public.orders(ingredients, name_on_order)
                    VALUES ('""" + ingredients_string + """','""" + name_on_order + """')"""

    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
