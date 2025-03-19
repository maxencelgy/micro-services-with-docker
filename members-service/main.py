from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import models, schemas, database

app = FastAPI(title="Members Service")

# Création des tables en base si elles n'existent pas
models.Base.metadata.create_all(bind=database.engine)

@app.get("/members/", response_model=List[schemas.Member])
def get_members(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    members = db.query(models.Member).offset(skip).limit(limit).all()
    return members

@app.get("/members/{member_id}", response_model=schemas.Member)
def get_member(member_id: int, db: Session = Depends(database.get_db)):
    member = db.query(models.Member).filter(models.Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member

@app.post("/members/", response_model=schemas.Member)
def create_member(member: schemas.MemberCreate, db: Session = Depends(database.get_db)):
    db_member = models.Member(**member.dict())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

@app.put("/members/{member_id}", response_model=schemas.Member)
def update_member(member_id: int, member: schemas.MemberUpdate, db: Session = Depends(database.get_db)):
    db_member = db.query(models.Member).filter(models.Member.id == member_id).first()
    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found")
    for key, value in member.dict(exclude_unset=True).items():
        setattr(db_member, key, value)
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member
