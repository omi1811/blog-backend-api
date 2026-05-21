# src/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from src import models, database
from src.schemas import CommentCreate, UserCreate, UserResponse, PostCreate, PostResponse # We'll create this next

app = FastAPI(title="Blog API", description="PostgreSQL + FastAPI")

# 🗄️ Create tables on startup (only for9dev! Use Alembic in prod)
@app.on_event("startup")
def startup():
    models.Base.metadata.create_all(bind=database.engine)

# 🔌 Health check
@app.get("/health")
def health():
    return {"status": "ok", "database": "connected"}

# 👤 Create a user (first CRUD endpoint!)
@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user_data: UserCreate, db: Session = Depends(database.get_db)):
    # Check if email already exists
    existing = db.query(models.User).filter(models.User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash password (we'll import from auth.py later)
    from src.auth import hash_password
    hashed = hash_password(user_data.password)
    
    # Create & save new user
    new_user = models.User(email=user_data.email, hashed_password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # ← Loads the auto-generated ID
    
    return new_user
 

@app.post("/users/{user_id}/posts", response_model=PostResponse, status_code=201)
def create_post(
    user_id: int, 
    post_data: PostCreate, 
    db: Session = Depends(database.get_db)
):
    
    # Verify user exists
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Create & save new post
    new_post = models.Post(
        title=post_data.title, 
        content=post_data.content, 
        author_id=user_id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

@app.get("/users/{user_id}/posts", response_model=list[PostResponse])
def get_user_posts(user_id: int, db: Session = Depends(database.get_db)):
    # Verify user exists
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user.posts

@app.get("/debug/users/{user_id}", response_model=list[UserResponse])
def debug_user(user_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        user.id: {
            "username": user.username,
            "email": user.email,
            "posts": [
                {"id": p.id, "title": p.title} for p in user.posts
            ]
        }
    }

@app.post("users/{user_id}/posts/{post_id}/comments", status_code=201)
def create_comment(
    user_id: int, 
    post_id: int, 
    comment_data: CommentCreate, 
    db: Session = Depends(database.get_db)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:    
        raise HTTPException(status_code=404, detail="User not found")
    
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    new_comment = models.Comment(
        body=comment_data.body,
        post_id=post_id,
        author_id=user_id
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment

@app.get("/users/{user_id}/posts/{post_id}/comments", status_code=200)
def get_comments(user_id: int, post_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:    
        raise HTTPException(status_code=404, detail="User not found")
    
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return post.comments

@app.delete("/users/{user_id}/posts/{post_id}", status_code=204)
def delete_post(user_id: int, post_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.author_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")

    db.delete(post)
    db.commit()
    return {"detail": "Post deleted"}