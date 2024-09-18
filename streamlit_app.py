# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)
cnx=st.connection("snowflake")  
session=cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))

pd_df=my_dataframe.to_pandas()
name_on_order = st.text_input("Name on Smoothie:", "")
st.write('The name on the Smoothie will be :',name_on_order)

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:"
    ,my_dataframe
    ,max_selections=5
)
ingredients_string=''
if ingredients_list:
    for fruit_chosen in ingredients_list:
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        ingredients_string+=fruit_chosen+' '
        st.subheader(fruit_chosen+' Nutrition Infomation')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+search_on)
        fv_dataframe=st.dataframe(data=fruityvice_response.json(),use_container_width=True)

my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
        values ('""" + ingredients_string + """','"""+name_on_order+"""')"""
    
    # st.write(my_insert_stmt)
    # st.stop()
time_to_insert=st.button('Submit Order')

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered,'+name_on_order+'!', icon="✅")
    
