import numpy as np
import pandas as pd
import streamlit as st 
from sklearn import preprocessing
import pickle

clf = pickle.load(open('models/treepickle_file', 'rb'))  

  
def main(): 
    st.title("Submission Finder")
    html_temp = """
    <h2 style="color:white;text-align:center;">Submission Finder </h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html = True)
    
    gender = st.selectbox("Gender",["Female","Male"]) 
    weight = st.text_input("weight","95") 
    height= st.text_input("height","179") 
    cols=['height', 'weight','gender']
    if st.button("Predict"): 
        
        data = {'height': int(height), 'weight': int(weight),'gender':gender }
        df=pd.DataFrame([list(data.values())], columns=[['height', 'weight','gender']])
        df['gender_num']=df['gender']=='Male'
        features=['height','weight','gender_num']
        X=df[features].to_numpy()      
        # X=scaler.transform(X)
        y=clf.predict(X)


        st.success('Submission is {}'.format(y[0]))
      
if __name__=='__main__': 
    main()