import streamlit as st
import requests

st.title("Money Transfer App")

# Get User Details
st.header("Get User Details")
user_id = st.text_input("Enter User ID")
if st.button("Get User Details"):
    if not user_id:
        st.error("Please enter a User ID.")
    else:
        response = requests.get(f"http://localhost:8000/users/{user_id}")
        if response.status_code == 200:
            user_info = response.json()
            st.success("User details fetched successfully!")
            st.json(user_info)  
        else:
            st.error(f"Failed to fetch user details: {response.text}")

# Update username or phone_number
st.header("Update User Details")
update_user_id = st.text_input("User ID to Update")
new_username = st.text_input("New Username (leave blank if no change)")
new_phone_number = st.text_input("New Phone Number (leave blank if no change)")
if st.button("Update User"):
    if not update_user_id:
        st.error("Please enter a User ID.")
    else:
        payload = {}
        if new_username:
            payload["username"] = new_username
        if new_phone_number:
            payload["phone_number"] = new_phone_number
        if not payload:
            st.error("Please provide at least one field to update.")
        else:
            response = requests.put(f"http://localhost:8000/users/{update_user_id}", params=payload)
            if response.status_code == 200:
                st.success("User details updated successfully!")
                st.json(response.json())
            else:
                st.error(f"Failed to update user details: {response.text}")

# User balance check
st.header("Check Wallet Balance")
check_user_id = st.text_input("User ID to Check Balance")
if st.button("Check Balance"):
    if not check_user_id:
        st.error("Please enter a User ID.")
    else:
        response = requests.get(f"http://localhost:8000/wallet/{check_user_id}/balance")
        if response.status_code == 200:
            balance_info = response.json()
            st.success(f"Wallet Balance: {balance_info['balance']}")
        else:
            st.error(f"Failed to fetch balance: {response.text}")

# Add money to wallet
st.header("Add Money to Wallet")
add_user_id = st.text_input("User ID to Add Money")
add_amount = st.number_input("Amount to Add", min_value=0.01, step=0.01)
if st.button("Add Money"):
    if not add_user_id or add_amount <= 0:
        st.error("Please provide valid inputs.")
    else:
        payload = {
            "amount": add_amount,
            "description": "Added money to wallet"
        }
        response = requests.post("http://localhost:8000/wallet/{add_user_id}/add-money", params=payload)
        if response.status_code == 200:
            st.success("Money added successfully!")
            st.json(response.json())
        else:
            st.error(f"Failed to add money: {response.text}")

# Withdraw money from wallet
st.header("Withdraw Money from Wallet")
withdraw_user_id = st.text_input("User ID to Withdraw Money")
withdraw_amount = st.number_input("Amount to Withdraw", min_value=0.01, step=0.01)
if st.button("Withdraw Money"):
    if not withdraw_user_id or withdraw_amount <= 0:
        st.error("Please provide valid inputs.")
    else:
        payload = {
            "amount": withdraw_amount,
            "description": "Withdrew money from wallet"
        }
        response = requests.post("http://localhost:8000/wallet/{withdraw_user_id}/withdraw", params=payload)
        if response.status_code == 200:
            st.success("Money withdrawn successfully!")
            st.json(response.json())
        else:
            st.error(f"Failed to withdraw money: {response.text}")

# Transfer money to another user
st.header("Transfer Money to Another User")
sender_user_id = st.text_input("Sender User ID")
recipient_user_id = st.text_input("Recipient User ID")
amount = st.number_input("Amount", min_value=0.01, step=0.01)
description = st.text_input("Description")
if st.button("Transfer Money"):
    if not sender_user_id or not recipient_user_id or amount <= 0:
        st.error("Please provide valid inputs.")
    else:
        payload = {
            "sender_user_id": sender_user_id,
            "recipient_user_id": recipient_user_id,
            "amount": amount,
            "description": description
        }
        response = requests.post("http://localhost:8000/transfer", params=payload)
        if response.status_code == 200:
            st.success("Transfer successful!")
            st.json(response.json())
        else:
            st.error(f"Transfer failed: {response.text}")

# View transaction history
st.header("View Transaction History")
history_user_id = st.text_input("User ID to View Transactions")
page = st.number_input("Page Number", min_value=1, step=1, value=1)
limit = st.number_input("Transactions per Page", min_value=1, step=1, value=10) 
if st.button("View Transactions"):
    if not history_user_id:
        st.error("Please enter a User ID.") 
    else:
        response = requests.get(f"http://localhost:8000/transactions/{history_user_id}/page={page}&limit={limit}")
        if response.status_code == 200:
            transactions = response.json()
            st.success("Transaction history fetched successfully!")
            st.json(transactions)   
        else:
            st.error(f"Failed to fetch transactions: {response.text}")

# View specific transaction detail
st.header("View Transaction Detail")
transaction_id = st.text_input("Transaction ID to View Detail") 
if st.button("View Transaction Detail"):
    if not transaction_id:
        st.error("Please enter a Transaction ID.")  
    else:
        response = requests.get(f"http://localhost:8000/transactions/detail/{transaction_id}")
        if response.status_code == 200:
            transaction_detail = response.json()
            st.success("Transaction detail fetched successfully!")
            st.json(transaction_detail)
        else:
            st.error(f"Failed to fetch transaction detail: {response.text}")


