import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Blog API Frontend", page_icon="📝")
st.title("Blog API Frontend")

try:
    users = requests.get(f"{API_URL}/users").json()
    user_emails = {user['email'] for user in users}
except Exception as e:   
    st.error(f"Error fetching users: {e}")
    users = []
    
st.subheader("Create a New User") # New section for user creation
with st.form("user_form"):
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submit_user = st.form_submit_button("Create User")
    
    if submit_user:
        if not username or not email or not password:
            st.warning("Please fill in all fields.")
        elif email in user_emails:
            st.warning("Email already exists. Please use a different email.")
        else:
            try:
                response = requests.post(f"{API_URL}/users", json={
                    "username": username,
                    "email": email,
                    "password": password
                })
                if response.status_code == 201:
                    st.success("User created successfully!")
                    user_emails.add(email)  # Update local set to prevent duplicates
                else:
                    st.error(f"Error creating user: {response.text}")
            except Exception as e:
                st.error(f"Error connecting to API: {e}")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Users")
    selected_user_id = st.selectbox("Select a user to view their posts", options=[f"{user['id']}: {user['username']}" for user in users])

if selected_user_id:
    with col2:
        st.subheader("Posts")
        user_id = int(selected_user_id.split(":")[0])
        try:
            posts = requests.get(f"{API_URL}/users/{user_id}/posts").json()
            post_titles = [post['title'] for post in posts]
            selected_post_id = st.selectbox("Select a post to view details", options=[f"{post['id']}: {post['title']}" for post in posts])
        except Exception as e:
            st.info("No posts found for this user.")
            st.error(f"Error fetching posts: {e}")

    if selected_post_id:
        with col3:
            st.subheader("Post Details")
            post_id = int(selected_post_id.split(":")[0])
            try:
                post_details = requests.get(f"{API_URL}/posts/{post_id}").json()
                st.write(f"**Title:** {post_details['title']}")
                st.write(f"**Content:** {post_details['content']}")
                st.write(f"**Created At:** {post_details['created_at']}")
            except Exception as e:
                st.error(f"Error fetching post details: {e}")

st.divider()
c1, c2 = st.columns(2)
with c1:
    st.subheader("Create a New Post")
    post_user_id = st.number_input("User ID", min_value=1, step=1)
    post_title = st.text_input("Post Title")
    post_content = st.text_area("Post Content")
    submit_post = st.button("Create Post")
    
    if submit_post:
        if not post_title or not post_content:
            st.warning("Please fill in all fields.")
        else:
            try:
                response = requests.post(f"{API_URL}/users/{post_user_id}/posts", json={
                    "title": post_title,
                    "content": post_content
                })
                if response.status_code == 201:
                    st.success("Post created successfully!")
                else:
                    st.error(f"Error creating post: {response.text}")
            except Exception as e:
                st.error(f"Error connecting to API: {e}")

with c2:
    st.subheader("Create a New Comment")
    comment_post_id = st.number_input("Post ID", min_value=1, step=1)
    comment_user_id = st.number_input("User ID", min_value=1, step=1, key="comment_user_id")
    comment_body = st.text_area("Comment Body", key="comment_body")
    submit_comment = st.button("Create Comment")
    
    if submit_comment:
        if not comment_body:
            st.warning("Please fill in the comment body.")
        else:
            try:
                response = requests.post(f"{API_URL}/posts/{comment_post_id}/comments", json={
                    "body": comment_body,
                    "author_id": comment_user_id
                })
                if response.status_code == 201:
                    st.success("Comment created successfully!")
                else:
                    st.error(f"Error creating comment: {response.text}")
            except Exception as e:
                st.error(f"Error connecting to API: {e}")
    