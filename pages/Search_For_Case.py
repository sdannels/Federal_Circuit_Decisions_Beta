# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 20:11:08 2023

@author: samda
"""

import pandas as pd
import streamlit as st

# read in data from first page (stored in session state)
if 'df' in st.session_state:
    df = st.session_state['df']
# if first page was not run yet, will need to read in data again
else:
    # define function to load data
    # st.cache_data means the data is stored and doesn't need to be read again each time the user changes a variable
    @st.cache_data
    def load_data(data_path, state_name):
        '''
        Parameters
        ----------
        data_path : str
            The file path to load the data
        state_name : str
            The name that the DataFrame will be stored as in the session state

        Returns
        -------
        df : DataFrame
        '''
        df = pd.read_csv(data_path, sep = '\t')
        # save the data in the session_state so it can be accessed from other pages
        st.session_state[state_name] = df
        return df
    # read in data
    df = load_data('https://raw.githubusercontent.com/sdannels/Federal_Circuit_Decisions_Beta/main/Data/appeals%202022-12-31%20Release.tab', state_name = 'df')

# set up section for searching for case
case_search_section = st.container()

## case search section
with case_search_section:
    # title section
    st.header('Search for a Specific Case')
    
    # give option to search by case ID or case name
    search_option = st.selectbox('Search By:', ['Unique ID', 'Case Name'])
    
    # function to output search results
    def search_results(search_out):
        # throw error if zero or more than one case match criteria
        if len(search_out) > 1:
            st.error('There is more than one case matching your search criteria.' \
                     ' Please be more specific in your search. You may try using' \
                     ' the "Filter Data" button above to search the data.', 
                     icon="🚨")
        elif len(search_out) == 0:
            st.error('No cases match this search criteria.', 
                     icon="🚨")
        else:
            # transpose dataframe and print
            return st.dataframe(search_out.T, height=(1000), width=(1000))
        
    
    # search function depends on choice in search_option
    # search by UniqueID
    if search_option == 'Unique ID':
        # accept user input for case number
        case_search = st.text_input('Search by uniqueID')
        # ignore empty search results
        if case_search == '':
            pass
        # if user input text, try to match and output case
        else:
            # match uniqueID column to given case number
            search_out = df[df['uniqueID'].astype(str) == case_search]
            search_results(search_out)
    
    # or search by caseName
    else:
        # accept text input from user
        case_search = st.text_input('Case Name')
        # ignore empty search results
        if case_search == '':
            pass
        # if user input text, try to match and output case
        else:
            # match partial string to caseName in df
            search_out = df[df['caseName'].astype(str).str.contains(case_search, case = False)]
            # output results
            search_results(search_out)