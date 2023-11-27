#-------------------------------------BizCardX-Extracting Business Card Data with OCR------------------------------------------------------------
#Importing necessary libraries
import streamlit as st
from streamlit_option_menu import option_menu
import easyocr
import re
from PIL import Image
import numpy as np
import pandas as pd
import mysql.connector
#----------------------------------------------------------------------------------------------------------------------------------------- 
#Setting streamlit environment

st.set_page_config(page_title= "BizCardX: Extracting Business Card Data with OCR by Banuprakash V",
                   layout= "wide",
                   page_icon="bussiness_card.png",
                   initial_sidebar_state= "expanded")
with st.sidebar:
    selected = option_menu("Menu", ["Home","Upload and Extract","Store to Database","View/Update/Delete"], 
                                    icons=["house-fill","rocket-takeoff-fill","database-fill-add","sliders2-vertical"],
                                    menu_icon= "grid-fill",
                                    default_index=0,
                                    styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F99AD"},
                                            "nav-link-selected": {"background-color": "green"}})
 
    
 #----------------------------------------------------------------------------------------------------------------------------------------- 
#Creating a function for extracting image information

def extract(uploaded_image):
    image = Image.open(uploaded_image)
    grayscale_image = image.convert('L')                          #Converting RGB image to black and white iamge
    image_to_np_array= np.array(grayscale_image)                  #Converting image into np array
    language_to_read= easyocr.Reader(['en'])                                 #setting to read english language
    card_info_list =language_to_read.readtext(image_to_np_array,detail = 0)  #Reading card information  
    print(card_info_list)
    # card_info_list=['Selva', 'DATA MANAGER', '+123-456-7890', '+123-456-7891', 'WWW XYZI.com', 'hello@XYZ1.com', '123 ABC St , Chennai', 'selva', 'TamilNadu 600113', 'digitals']
    #-----------------------------------------------------------------------------------------------------------------------------------------
    # Pattern making using regular expression

    phone_number_pattern = re.compile(r'\+|[0-9]+[-\s][0-9]+[-\s][0-9]+')
    website_pattern = re.compile(r'[wW]{3}')
    mail_id_pattern = re.compile(r'@')
    address_pattern = re.compile(r'\d+\s[a-zA-Z]+')
    pincode_pattern=re.compile(r'\b(\d{6,7})\b')
    #-----------------------------------------------------------------------------------------------------------------------------------------

    name=[]
    designation=[]
    phone_number_list = []
    mail_id_list=[]
    website_list=[]
    address_list=[]
    pin_code_list=[] 
    company_name_list=[]
    for i in card_info_list :
            phone_number= phone_number_pattern.search(i)
            mail_id = mail_id_pattern.search(i)
            website = website_pattern.search(i)
            address = address_pattern.search(i)
            pincode= pincode_pattern.search(i)
            if i==card_info_list[0]:
                name.append(i)
            if i==card_info_list[1] :
                designation.append(i)
            if phone_number:
                phone_number_list .append(i)
            elif mail_id:
                mail_id_list.append(i)
            elif website:
                website_list.append(i)
            elif address:
                address_list.append(i)
            elif pincode:
                pc = pincode.group(1)
                pin_code_list.append(pc)
                #sometimes in this model state name comes with pincodeline.For moving state name into address list we are using this
                match_checking= re.match(r'^([A-Za-z]+)',i)
                if  match_checking:
                    state_name =  match_checking.group(1)
                    address_list.append(state_name)
            elif i != card_info_list[0] and i !=card_info_list[1]:
                company_name_list.append(i)
              

    return ''.join(name),''.join(designation),','.join(phone_number_list),','.join(mail_id_list),'/'.join( website_list),','.join(address_list),'/'.join(pin_code_list),' '.join(company_name_list)            
#-----------------------------------------------------------------------------------------------------------------------------------------
# Home page

if selected=="Home":
    if selected == "Home":
            st.info("# :white[BizCardX: Extracting Business Card Data with OCR]")
            col1,col2 = st.columns(2,gap="medium")
            col1.markdown("### :orange[Technologies Used :]")
            col1.markdown("### :white[ &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;1.&nbsp;Python]")
            col1.markdown("### :white[ &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;2.&nbsp;OCR]")
            col1.markdown("### :white[ &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;3.&nbsp;Streamlit]")
            col1.markdown("### :white[ &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;4.&nbsp;MySQL]")
            col1.markdown("### :orange[Synopsis:]")
            col1.markdown("### :white[:blue[Step 1]: Import easyocr package in python for extracting text information in an image and also import other neccessary packages.]")
            col1.markdown("### :white[:blue[Step 2]: Set up streamlit environment for uploading image, extracting and storing the processed image data.]")
            col1.markdown("### :white[:blue[Step 3]: Upload business card image and extract information]")
            col1.markdown("### :white[:blue[Step 4]: After extracting image information,store the text data into MYSQL database.]")
            col1.markdown("### :white[:blue[Step 5]: Finally after storing data into MYSQL database various queries such as view,update,delete are carried out.]")
            col2.write("##  ")
            col2.write("##  ")
            col2.write("##  ")
            col2.image("bussiness_logo.png")
#-----------------------------------------------------------------------------------------------------------------------------------------
# Uplopad and Extract 

if selected=="Upload and Extract":
            st.info('## Upload and Extract')   
            #Uploading bussiness card
            image_upload = st.file_uploader('Kindly upload your Image')    
            if image_upload !=None: #for streamlit display error we are using this if condition and nothing in this.........
                  image = Image.open(image_upload)
                  #Resizeing the uploaded image for display convinience and image preview
                  resized_image = image.resize((500,300))
                  st.subheader('Bussiness Card Preview')
                  st.image(resized_image)      
            #-----------------------------------------------------------------------------------------------------------------------------------------
            #Creating the extract button
            extract_button = st.button('Extract')

            if extract_button:
                with st.spinner('Please Wait for few seconds...'):
                 if image_upload is not None:
                    name,designation,phone_number,email_id,website,address,pincode,company_name = extract(image_upload)
                    
                    data = [company_name,name,designation,phone_number,email_id,website,address,pincode]
                    list = []
                    list.append(data)                
                    df = pd.DataFrame(list,columns = ['Company_name','Name','Designation','Phone_number','Email_id','Website','Address','Pincode'])
                    st.dataframe(df)  
                    st.subheader(f':green[Company_name] : {company_name}')
                    st.subheader(f':green[Name] :        {name}')
                    st.subheader(f':green[Designation] : {designation}')
                    st.subheader(f':green[Phone no] :    {phone_number}')
                    st.subheader(f':green[Email_id] :    {email_id}')
                    st.subheader(f':green[Website] :     {website}')
                    st.subheader(f':green[Address] :     {address}')
                    st.subheader(f':green[Pincode] :     {pincode}')
                    st.success("Data Extracted Successfully !!!...")
#-----------------------------------------------------------------------------------------------------------------------------------------
# Storing into SQL Database 

if selected=="Store to Database": 
    st.info('## Upload extracted data into MYSQL Database')
    mydb = mysql.connector.connect(
                            host="localhost",
                            user="root",
                            password="952427",
                            # database="bizcard_database",
                        )
    mycursor = mydb.cursor(buffered=True) #buffered =True means fetches all data to the temporary memory and reduces query processing time but it leads to storage issue.
    mycursor.execute('create database if not exists bizcard_database;')
    mydb.commit()
    mycursor.execute('use bizcard_database;')
    mydb.commit()
    image_upload = st.file_uploader('Kindly upload your Image')

    #Create unique_id for each data for data fetching.
    st.subheader(':green[Enter ID:]')
    id = st.text_input('Create &nbsp;unique ID for the businees card details')
    #Upload button
    upload_button= st.button('Upload into MYSQL Database')
    if upload_button:
       
        with st.spinner('Please wait...'):
                #Creating table
                name,designation,phone_number,email_id,website,address,pincode,company_name = extract(image_upload)
                table_creation_query=table_creation_query = "CREATE TABLE IF NOT EXISTS bizcard_data (id VARCHAR(100),company_name VARCHAR(60),name VARCHAR(50), designation VARCHAR(100), phone_number VARCHAR(100), website VARCHAR(100), mail_id VARCHAR(100), address VARCHAR(150), pincode INT(10));"
                mycursor.execute( table_creation_query)

                query = 'INSERT INTO bizcard_data (id,company_name,name,designation,phone_number,website,mail_id,address,pincode) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);'
                values = (id,company_name,name,designation,phone_number,email_id,website,address,pincode)
                mycursor.execute(query,values)
                mydb.commit()
                st.success("Data uploaded Successfully !!!")
                
#-----------------------------------------------------------------------------------------------------------------------------------------
# View/Update/Delete

#Connecting to MYSQL data_base
if selected=="View/Update/Delete":
    st.info('## View-Update-Delete')
    mydb = mysql.connector.connect(
                            host="localhost",
                            user="root",
                            password="952427",
                            database="bizcard_database",
                        )
    mycursor = mydb.cursor(buffered=True) 
    #-----------------------------------------------------------------------------------------------------------------------------------------
    #Display the data from database 

    st.subheader(':green[View Data:]')
    id = st.text_input('Enter your Id')
    submit = st.button('View Details')
    if id is not None:
        if submit:
            with st.spinner('Please wait..'):
                view_query = 'select id,company_name,name,designation,phone_number,website,mail_id,address,pincode from bizcard_data where id = %s;'
                values = [id]
                mycursor.execute(view_query,values)
                data = mycursor.fetchall()
                df = pd.DataFrame(data,columns = ["Id","company_name","name","designation","phone_number","website","mail_id","address","pincode"])
                st.dataframe(df) 
                st.success("Data fetched Succesfully!!!")
    #-----------------------------------------------------------------------------------------------------------------------------------------
    #Update the data in database  
         
    st.subheader(':green[Update Data:]')
    select_options = st.selectbox('select any one field that you want to update',options=['Select any one','company_name','name','designation','phone_number','website','mail_id','address','pin_code'])

    if select_options == 'company_name':
        company_name = st.text_input('Enter your company_name')
        update = st.button('Update your details')
        if update:
            update_query = 'UPDATE bizcard_data SET company_name= %s WHERE id = %s;'
            values = (company_name,id)
            mycursor.execute(update_query,values)
            mydb.commit()
            st.success("Data updated Succesfully!!!")
    if select_options == 'name':
        name = st.text_input('Enter your name')
        update = st.button('Update your details')
        if update:
            update_query = 'UPDATE bizcard_data SET name = %s WHERE id = %s;'
            values = (name,id)
            mycursor.execute(update_query,values)
            mydb.commit()
            st.success("Data updated Succesfully!!!")


    elif select_options == 'designation':
        designation = st.text_input('Enter your designation')
        update = st.button('Update your details')
        if update:
            update_query = 'UPDATE bizcard_data SET designation = %s WHERE id = %s;'
            values = (designation,id)
            mycursor.execute(update_query,values)
            mydb.commit()
            st.success("Data updated Succesfully!!!")
    elif select_options == 'phone_number':
        phone_number = st.text_input('Enter your phone_number')
        update = st.button('Update your details')
        if update:
            update_query = 'UPDATE bizcard_data SET phone_number = %s WHERE id = %s;'
            values = [phone_number,id]
            mycursor.execute(update_query,values)
            mydb.commit()
            st.success("Data updated Succesfully!!!")

    elif select_options == 'website':
        website = st.text_input('Enter your phone_no')
        update = st.button('Update your details')
        if update:
            update_query = 'UPDATE bizcard_data SET website = %s WHERE id = %s;'
            values = (website,id)
            mycursor.execute(update_query,values)
            mydb.commit()
            st.success("Data updated Succesfully!!!")

    elif select_options == 'mail_id':
        mail_id = st.text_input('Enter your mail_id')
        update = st.button('Update your details')
        if update:
            update_query = 'UPDATE bizcard_data SET mail_id = %s WHERE id = %s;'
            values = (mail_id,id)
            mycursor.execute(update_query,values)
            mydb.commit()
            st.success("Data updated Succesfully!!!")

    elif select_options == 'address':
        address = st.text_input('Enter your address')
        update = st.button('Update your details')
        if update:
            update_query = 'UPDATE bizcard_data SET address = %s WHERE id = %s;'
            values = (address,id)
            mycursor.execute(update_query,values)
            mydb.commit()
            st.success("Data updated Succesfully!!!")

    elif select_options == 'pin_code':
        pincode = st.text_input('Enter your pincode')
        update = st.button('Update your details')
        if update:
            update_query = 'UPDATE bizcard_data SET pincode = %s WHERE id = %s;'
            values = (pincode,id)
            mycursor.execute(update_query,values)
            mydb.commit()
            st.success("Data updated Succesfully!!!")
    #-----------------------------------------------------------------------------------------------------------------------------------------
    #Delete the data from database

    st.subheader(':green[Delete Data:]')
    delete_id = st.text_input('Enter your id')
    delete = st.button('Delete your details')
    if delete:
        with st.spinner('Please wait..'):
            delete_query = 'DELETE FROM bizcard_data where id = %s;'
            values = (delete_id,)
            mycursor.execute(delete_query,values)
            mydb.commit()
            st.success("Data deleted Succesfully!!!")

#-----------------------------------------------------------------------------------------------------------------------------------------
#Closing the database connection
    mydb.close()
#-----------------------------------------------------------------------------------------------------------------------------------------
