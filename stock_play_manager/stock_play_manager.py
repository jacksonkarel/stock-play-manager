import streamlit as st
import pandas as pd
import os

# Title of the app
st.title('Stock Portfolio Adjuster')

st.write('Use this app to build and adjust your stock portfolio by adding stocks, inputting their prices, and specifying the number of shares you want to buy.')

# Initialize session state for storing portfolio data
if 'portfolio' not in st.session_state:
    st.session_state['portfolio'] = []
    # Check if a saved portfolio exists and load it
    if os.path.exists('portfolio.csv'):
        df_saved = pd.read_csv('portfolio.csv')
        st.session_state['portfolio'] = df_saved.to_dict('records')

# Function to save portfolio to CSV
def save_portfolio():
    df_portfolio = pd.DataFrame(st.session_state['portfolio'])
    df_portfolio.to_csv('portfolio.csv', index=False)
    st.success('Portfolio has been saved to portfolio.csv.')

# Section to add new stocks
st.header('Add a Stock to Your Portfolio')

with st.form(key='add_stock_form'):
    col1, col2, col3 = st.columns(3)
    with col1:
        # No max_chars argument, so no character limit
        stock_symbol = st.text_input('Stock Symbol', value='')
    with col2:
        stock_price = st.number_input('Price per Share ($)', min_value=0.0, format="%.2f")
    with col3:
        num_shares = st.number_input('Number of Shares', min_value=0, value=0, step=1)
    add_stock = st.form_submit_button(label='Add Stock')

if add_stock:
    if stock_symbol.strip() == '':
        st.error('Please enter a valid stock symbol.')
    elif stock_price <= 0:
        st.error('Price per share must be greater than zero.')
    elif num_shares <= 0:
        st.error('Number of shares must be greater than zero.')
    else:
        # Add the stock to the portfolio
        st.session_state['portfolio'].append({
            'Stock Symbol': stock_symbol.upper(),
            'Price per Share ($)': stock_price,
            'Number of Shares': num_shares,
            'Total Cost ($)': stock_price * num_shares
        })
        st.success(f"Added {num_shares} shares of {stock_symbol.upper()} at ${stock_price:.2f} per share.")
        # Save the updated portfolio
        save_portfolio()

# Display the portfolio summary
if st.session_state['portfolio']:
    st.header('Portfolio Summary')
    df_portfolio = pd.DataFrame(st.session_state['portfolio'])

    # Format the currency columns for display
    df_display = df_portfolio.copy()
    df_display['Price per Share ($)'] = df_display['Price per Share ($)'].map('${:,.2f}'.format)
    df_display['Total Cost ($)'] = df_display['Total Cost ($)'].map('${:,.2f}'.format)
    st.table(df_display[['Stock Symbol', 'Price per Share ($)', 'Number of Shares', 'Total Cost ($)']])

    # Calculate and display the total portfolio cost
    total_portfolio_cost = df_portfolio['Total Cost ($)'].sum()
    st.write(f'**Total Cost of Portfolio:** ${total_portfolio_cost:,.2f}')

    # Section to remove stocks
    st.header('Remove Stocks from Your Portfolio')
    # Get a list of stock symbols in the portfolio
    stock_symbols = [item['Stock Symbol'] for item in st.session_state['portfolio']]
    if stock_symbols:
        stock_to_remove = st.multiselect('Select stock(s) to remove:', options=stock_symbols)
        if st.button('Remove Selected Stocks'):
            if stock_to_remove:
                # Remove the selected stocks from the portfolio
                st.session_state['portfolio'] = [item for item in st.session_state['portfolio'] if item['Stock Symbol'] not in stock_to_remove]
                st.success(f"Removed stock(s): {', '.join(stock_to_remove)}")
                # Save the updated portfolio
                save_portfolio()
            else:
                st.error('Please select at least one stock to remove.')
    else:
        st.info('No stocks available to remove.')

    # Option to reset the entire portfolio
    if st.button('Reset Portfolio'):
        st.session_state['portfolio'] = []
        # Remove the CSV file if it exists
        if os.path.exists('portfolio.csv'):
            os.remove('portfolio.csv')
        st.success('Portfolio has been reset.')
else:
    st.info('Your portfolio is currently empty. Add stocks using the form above.')
