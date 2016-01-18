# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
import csv
import pandas as pd
import numpy as np
from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Owner, Lists, Items

engine = create_engine('sqlite:///finalProject.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

## Define these variables for filenames
report_filename = 'dataitems.csv'

wkdir = os.getcwd()
print wkdir

##create dataframe
report_df = pd.read_csv(wkdir + '/' + report_filename)
pd.set_option('display.max_colwidth', -1) #so filenames don't get truncated

print report_df.columns
for i in report_df.columns:
    print i
for index, row in report_df.iterrows():
    print row['name'][3:-1]
    print row['id']
    print row['url'][3:-1]
    print row['description'][3:-1]
    print row['rank']
    print row['list_id']

    newItem = Items(name = row['name'][3:-1], description = row['description'][3:-1],
        url = row['url'][3:-1],
        id = row['id'], lists_id = row['list_id'], rank=row['rank'])
    session.add(newItem)
    session.commit()

