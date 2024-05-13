import numpy as np
import pandas as pd
import streamlit as st 
import pickle
from streamlit.connections import SQLConnection
from sqlalchemy.sql import text
from datetime import timedelta

def main(): 
    clf = pickle.load(open('models/treepickle_file', 'rb'))  

    # Initialize connection.
    conn = st.connection("postgresql", type="sql")

    # # Perform query.
    # df = conn.query('SELECT * FROM physical_stats;', ttl="10s")

    # # Print results.
    # Data= conn.query("Select * FROM physical_stats; ", ttl=timedelta(seconds=5))
    # st.dataframe(Data)


    st.title("Submission Finder")
    html_temp = """
    <h2 style="color:white;text-align:center;">Submission Finder </h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html = True)

    gender = st.selectbox("Gender",["Female","Male"]) 
    weight = st.text_input("Weight","95") 
    height= st.text_input("Height","179") 
    fav_sub=st.text_input("High percentage submission")



    if st.button("Predict"): 
        
        data = {'height': int(height), 'weight': int(weight),'gender':gender }
        df=pd.DataFrame([list(data.values())], columns=[['height', 'weight','gender']])
        df['gender_num']=df['gender']=='Male'
        features=['height','weight','gender_num']
        X=df[features].to_numpy()      
        # X=scaler.transform(X)
        y=clf.predict(X)
        with conn.session as s:
            s.execute(text('INSERT INTO physical_stats (height, weight, gender, submission, predsub) VALUES (:height, :weight, :gender, :submission, :predsub);'),
                params=dict(height=height, weight=weight, gender=gender, submission=fav_sub, predsub=y[0]))
            s.commit()
        st.success('Submission is {}'.format(y[0]))
      
if __name__=='__main__': 
    main()