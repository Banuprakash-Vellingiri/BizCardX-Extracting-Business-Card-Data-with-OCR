# BizCardX-Extracting-Business-Card-Data-with-OCR

## What is EasyOCR?

   EasyOCR, as the name suggests, is a Python package that allows computer vision developers to effortlessly perform Optical Character Recognition.It is a Python library for Optical Character Recognition (OCR) that allows you to easily extract text from images and scanned documents. In my project I am using easyOCR to extract text from **business cards.**
   
   When it comes to OCR, EasyOCR is by far the most straightforward way to apply Optical Character Recognition:

   - The EasyOCR package can be installed with a single pip command.
   - The dependencies on the EasyOCR package are minimal, making it easy to configure your OCR development environment.
   - Once EasyOCR is installed, only one import statement is required to import the package into your project.
   - From there, all you need is two lines of code to perform OCR — one to initialize the Reader class and then another to OCR the image via the readtext function.

## Project Overview
 
   BizCardX is a user-friendly tool for extracting information from business cards. The tool uses OCR technology to recognize text on business cards and extracts the data into a SQL database after classification using regular expressions. Users can access the extracted information using a GUI built using streamlit.
   The BizCardX application is a simple and intuitive user interface that guides users through the process of uploading the business card image and extracting its information. The extracted information would be displayed in a clean and organized manner, and users would be able to easily add it to the database with the click of a button. Further the data stored in database can be easily Read, updated and deleted by user as per the requirement.

   ### Libraries/Modules used for the project!
   - Pandas - (To Create a DataFrame with the scraped data)
   - Postgesql - (To store and retrieve the data)
   - Streamlit - (To Create Graphical user Interface)
   - EasyOCR - (To extract text from images)
# BizCardX-Extracting Business Card Data by using easyOCR (Optical Character Recognition)

## Introduction
- In today's fast-paced business environment, efficiently managing and organizing contact information is crucial for successful networking and communication. With the advent of digital tools and technologies, manual entry of business card details into a database can be time-consuming and prone to errors. To overcome these challenges, developers can leverage the power of optical character recognition (OCR) and databases to automate the process of extracting relevant information from business cards and storing it for easy access.

- One powerful OCR library that facilitates the extraction of text from images is EasyOCR. EasyOCR is an open-source Python library that utilizes deep learning models to accurately recognize and extract text from various languages. By integrating EasyOCR with a MySQL database, developers can streamline the process of capturing business card data and storing it in a structured and organized manner.

## Developer Guide

### 1. Tools Install
    - Virtual code.
    - Jupyter notebook.
    - Python 3.11.0 or higher.
    - MySQL.

### 2. Requirement Libraries to Install
   - pip install -r requirement.txt

### 3. Import Libraries
#### Scanning library
    - import easyocr # (Optical Character Recognition)
    - import numpy as np
    - from PIL import Image, ImageDraw
    - import cv2
    - import os
    - import re

#### Data frame libraries
    - import pandas as pd

#### Database Library
    - import sqlalchemy
    - import mysql.connector
    - from sqlalchemy import create_engine, inspect

#### Dashboard library
    - import streamlit as st

### 4. E T L Process

#### a) Extract data
    - Extract relevant information from business cards by using the easyOCR library

#### b) Process and Transform the data
    - After the extraction process, process the extracted data based on Company name, Card Holder, Designation, Mobile Number, Email, Website, Area, City, State, and Pincode is converted into a data frame.

#### c) Load data
    - After the transformation process, the data is stored in the MySQL database.


## User Guide

#### Step 1. Data collection zone
    - Click the 'Browse Files' button and select an image

#### Step 2. Data upload
    - Click the 'Upload to MySQL DB' button to upload the data to the Mysql database

#### Step 3. Modification zone
    - In this 'Modification zone' you can able to modify the information also you can delete the previous data
