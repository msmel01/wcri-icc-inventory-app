import streamlit as st
from sqlalchemy.sql import text
from datetime import datetime, timezone
import hmac


def add_items_ui():
    with st.form("Add Items", enter_to_submit=False, clear_on_submit=True):
        name = st.text_input("Item Name*", value=None)

        category = st.selectbox (
            "Item Category*",
            ("QLI", "Socials", "Member Initiatives", "Member Education", "ICC Meetings", "Judicial"),
            placeholder="Select Budget Category", index=None
        )

        count = st.number_input (
            "Insert Item Count", value=1
        )

        condition = st.selectbox (
            "Item Condition*",
            ("New", "Good", "Fair", "Damaged"), placeholder="Select condition", index=None
        )

        cost = st.number_input (
            "Insert Cost Per Unit", placeholder="Type a number"
        )

        dateBought = st.date_input(
            "Select Date Bought",
            format="DD.MM.YYYY", value=None
        )

        canBorrow = st.toggle("Item Is Loanable") # Potentially which user group can loan it

        notes = st.text_input("Additional Notes", value=None)
        
        submitted = st.form_submit_button("Add")

        if submitted and name and category and condition:
            with conn.session as session:
                session.begin()
            try:
                timestamp = datetime.now(timezone.utc)
                session.execute(
                    text(f"INSERT INTO items (name, category, count, condition, cost, bought, added, updated, canBorrow, notes) VALUES ('{name}', '{category}', '{count}', '{condition}', '{cost}', '{dateBought}', '{timestamp}', '{timestamp}', '{canBorrow}', '{notes}');")
                )

            except:
                session.rollback()
                raise

            else:
                session.commit()
                st.success('Added Successfully!')


def login():
    def check_password():
        if st.session_state["username"] in st.secrets["passwords"] and hmac.compare_digest(st.session_state["password"], st.secrets.passwords[st.session_state["username"]]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    if st.session_state.get("password_correct", False):
        return True

    with st.form("Credentials"):
        st.text_input("Username", key="username")
        st.text_input("Password", type="password", key="password")
        st.form_submit_button("Log in", on_click=check_password)

    if "password_correct" in st.session_state:
        st.error("Incorrect Username or Password")

    return False
    

if not login():
     st.stop()

# Setup connection
conn = st.connection("icc_db", type="sql")

add_items_ui()
