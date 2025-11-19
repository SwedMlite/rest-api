from datetime import date
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import Comment, Post, User
from .schemas import (
    CommentCreate,
    CommentOut,
    CommentUpdate,
    PostCreate,
    PostOut,
    PostUpdate,
    UserCreate,
    UserOut,
    UserRole,
    UserUpdate,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="REST Lab6 Python API",
    version="1.0.0",
    description="REST API for managing users, posts and comments using MySQL storage.",
)


def get_user_or_404(db: Session, user_id: int) -> User:
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


def get_post_or_404(db: Session, post_id: int) -> Post:
    post = db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


def get_comment_or_404(db: Session, comment_id: int) -> Comment:
    comment = db.get(Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return comment


@app.get("/health")
def healthcheck():
    return {"status": "ok"}


@app.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    user = User(
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        birth_date=user_in.birth_date,
        email=user_in.email,
        active=user_in.active,
        role=user_in.role.value,
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")
    db.refresh(user)
    return user


@app.get("/users", response_model=List[UserOut])
def list_users(
    name: Optional[str] = Query(None, description="Partial first name match"),
    surname: Optional[str] = Query(None, description="Partial last name match"),
    birth_from: Optional[date] = Query(None, alias="birthFrom"),
    birth_to: Optional[date] = Query(None, alias="birthTo"),
    role: Optional[UserRole] = Query(None),
    active: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(User)
    if name:
        query = query.filter(User.first_name.ilike(f"%{name}%"))
    if surname:
        query = query.filter(User.last_name.ilike(f"%{surname}%"))
    if birth_from:
        query = query.filter(User.birth_date >= birth_from)
    if birth_to:
        query = query.filter(User.birth_date <= birth_to)
    if role:
        query = query.filter(User.role == role.value)
    if active is not None:
        query = query.filter(User.active == active)
    return query.order_by(User.id).all()


@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return get_user_or_404(db, user_id)


@app.put("/users/{user_id}", response_model=UserOut)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = get_user_or_404(db, user_id)
    update_data = user_update.dict(exclude_unset=True)
    if "role" in update_data and isinstance(update_data["role"], UserRole):
        update_data["role"] = update_data["role"].value
    for field, value in update_data.items():
        setattr(user, field, value)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")
    db.refresh(user)
    return user


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_or_404(db, user_id)
    db.delete(user)
    db.commit()
    return None


@app.post("/posts", response_model=PostOut, status_code=status.HTTP_201_CREATED)
def create_post(post_in: PostCreate, db: Session = Depends(get_db)):
    get_user_or_404(db, post_in.user_id)
    post = Post(title=post_in.title, body=post_in.body, link=post_in.link, user_id=post_in.user_id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@app.get("/posts", response_model=List[PostOut])
def list_posts(
    title: Optional[str] = Query(None, description="Partial title match"),
    user_id: Optional[int] = Query(None, alias="userId"),
    db: Session = Depends(get_db),
):
    query = db.query(Post)
    if title:
        query = query.filter(Post.title.ilike(f"%{title}%"))
    if user_id is not None:
        query = query.filter(Post.user_id == user_id)
    return query.order_by(Post.id).all()


@app.get("/posts/{post_id}", response_model=PostOut)
def get_post(post_id: int, db: Session = Depends(get_db)):
    return get_post_or_404(db, post_id)


@app.put("/posts/{post_id}", response_model=PostOut)
def update_post(post_id: int, post_update: PostUpdate, db: Session = Depends(get_db)):
    post = get_post_or_404(db, post_id)
    update_data = post_update.dict(exclude_unset=True)
    if "user_id" in update_data:
        get_user_or_404(db, update_data["user_id"])
    for field, value in update_data.items():
        setattr(post, field, value)
    db.commit()
    db.refresh(post)
    return post


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = get_post_or_404(db, post_id)
    db.delete(post)
    db.commit()
    return None


@app.post("/comments", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
def create_comment(comment_in: CommentCreate, db: Session = Depends(get_db)):
    get_user_or_404(db, comment_in.user_id)
    get_post_or_404(db, comment_in.post_id)
    comment = Comment(body=comment_in.body, user_id=comment_in.user_id, post_id=comment_in.post_id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


@app.get("/comments", response_model=List[CommentOut])
def list_comments(
    user_id: Optional[int] = Query(None, alias="userId"),
    post_id: Optional[int] = Query(None, alias="postId"),
    db: Session = Depends(get_db),
):
    query = db.query(Comment)
    if user_id is not None:
        query = query.filter(Comment.user_id == user_id)
    if post_id is not None:
        query = query.filter(Comment.post_id == post_id)
    return query.order_by(Comment.id).all()


@app.get("/comments/{comment_id}", response_model=CommentOut)
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    return get_comment_or_404(db, comment_id)


@app.get("/posts/{post_id}/comments", response_model=List[CommentOut])
def get_comments_for_post(
    post_id: int,
    user_id: Optional[int] = Query(None, alias="userId"),
    db: Session = Depends(get_db),
):
    get_post_or_404(db, post_id)
    query = db.query(Comment).filter(Comment.post_id == post_id)
    if user_id is not None:
        query = query.filter(Comment.user_id == user_id)
    return query.order_by(Comment.id).all()


@app.put("/comments/{comment_id}", response_model=CommentOut)
def update_comment(comment_id: int, comment_update: CommentUpdate, db: Session = Depends(get_db)):
    comment = get_comment_or_404(db, comment_id)
    update_data = comment_update.dict(exclude_unset=True)
    if "user_id" in update_data:
        get_user_or_404(db, update_data["user_id"])
    if "post_id" in update_data:
        get_post_or_404(db, update_data["post_id"])
    for field, value in update_data.items():
        setattr(comment, field, value)
    db.commit()
    db.refresh(comment)
    return comment


@app.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = get_comment_or_404(db, comment_id)
    db.delete(comment)
    db.commit()
    return None
