import streamlit as st
import pandas as pd
import numpy as np
import pickle
import base64



@st.cache_data() #suppress_st_warning=True
def get_fvalue(val):
    feature_dict = {"No":1,"Yes":2}
    for key,value in feature_dict.items():
        if val == key:
            return value

def get_value(val,my_dict):
    for key,value in my_dict.items():
        if val == key:
            return value
       
app_mode = st.sidebar.selectbox('Pilih Menu',['Home','Prediksi'])
if app_mode=='Home':
    st.title('PREDIKSI PINJAMAN BANK')
    st.image('loan_image.jpg') 
    st.write('Dikembangkan oleh: Taofik Krisdiyanto, S.Kom.') 
   
   
   
elif app_mode =='Prediksi':
    
    #csv=pd.read_csv("informations.csv")
    #st.write(csv)

    st.image('loan_image.jpg')

    st.subheader('Bapak/Ibu, Dimohon untuk mengisi semua informasi yang diperlukan untuk mendapatkan balasan atas permintaan pinjaman Anda !')
    st.sidebar.header("Informasi tentang klien :")
    gender_dict = {"Laki-laki":1,"Perempuan":2}
    feature_dict = {"Tidak":1,"Ya":2}
    edu={'Lulus':1,'Belum Lulus':2}
    prop={'Desa':1,'Kota':2,'Semi Kota':3}
    Gender=st.sidebar.radio('Jenis Kelamin',tuple(gender_dict.keys()))
    Married=st.sidebar.radio('Status Menikah',tuple(feature_dict.keys()))
    Self_Employed=st.sidebar.radio('Bekerja Sendiri',tuple(feature_dict.keys()))
    Dependents=st.sidebar.radio('Tanggungan',options=['0','1' , '2' , '3+'])
    Education=st.sidebar.radio('Pendidikan',tuple(edu.keys()))
    ApplicantIncome=st.sidebar.slider('Pendapatan Pemohon',0,10000,0,)
    CoapplicantIncome=st.sidebar.slider('Pendapatan Wakil Pemohon',0,10000,0,)
    LoanAmount=st.sidebar.slider('Jumlah Pinjaman dalam Rp.',9.0,700.0,200.0)
    Loan_Amount_Term=st.sidebar.selectbox('Jangka Waktu Jumlah Pinjaman',(12.0,36.0,60.0,84.0,120.0,180.0,240.0,300.0,360.0))
    Credit_History=st.sidebar.radio('Riwayat Kredit',(0.0,1.0))
    Property_Area=st.sidebar.radio('Area Properti',tuple(prop.keys()))


    class_0 , class_3 , class_1,class_2 = 0,0,0,0
    if Dependents == '0':
        class_0 = 1
    elif Dependents == '1':
        class_1 = 1
    elif Dependents == '2' :
        class_2 = 1
    else:
        class_3= 1

    Rural,Urban,Semiurban=0,0,0
    if Property_Area == 'Urban' :
        Urban = 1
    elif Property_Area == 'Semiurban' :
        Semiurban = 1
    else :
        Rural=1
   
    data1={
    'Gender':Gender,
    'Married':Married,
    'Dependents':[class_0,class_1,class_2,class_3],
    'Education':Education,
    'ApplicantIncome':ApplicantIncome,
    'CoapplicantIncome':CoapplicantIncome,
    'Self Employed':Self_Employed,
    'LoanAmount':LoanAmount,
    'Loan_Amount_Term':Loan_Amount_Term,
    'Credit_History':Credit_History,
    'Property_Area':[Rural,Urban,Semiurban],
    }

    feature_list=[ApplicantIncome,CoapplicantIncome,LoanAmount,Loan_Amount_Term,Credit_History,get_value(Gender,gender_dict),get_fvalue(Married),data1['Dependents'][0],data1['Dependents'][1],data1['Dependents'][2],data1['Dependents'][3],get_value(Education,edu),get_fvalue(Self_Employed),data1['Property_Area'][0],data1['Property_Area'][1],data1['Property_Area'][2]]

    single_sample = np.array(feature_list).reshape(1,-1)

    if st.button("Prediksi"):
        file_ = open("6m-rain.gif", "rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()
   
        file = open("green-cola-no.gif", "rb")
        contents = file.read()
        data_url_no = base64.b64encode(contents).decode("utf-8")
        file.close()
   
   
        loaded_model = pickle.load(open('Random_Forest.sav', 'rb'))
        prediction = loaded_model.predict(single_sample)
        if prediction[0] == 0 :
            st.error(
    'Menurut Perhitungan kami, Anda tidak akan mendapatkan pinjaman dari Bank'
    )
            st.markdown(
    f'<img src="data:image/gif;base64,{data_url_no}" alt="cat gif">',
    unsafe_allow_html=True,)
        elif prediction[0] == 1 :
            st.success(
    'Selamat!! Anda akan mendapatkan pinjaman dari Bank'
    )
            st.markdown(
    f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
    unsafe_allow_html=True,
    )





