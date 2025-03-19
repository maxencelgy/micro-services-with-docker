from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
import httpx
import models, schemas, database
from circuitbreaker import circuit

app = FastAPI(title="Reservation Service")

# Création des tables en base si elles n'existent pas
models.Base.metadata.create_all(bind=database.engine)

# Définition d'une fonction d'appel avec circuit breaker pour simplifier
@circuit(failure_threshold=3, recovery_timeout=30)
async def call_service(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()

@app.post("/reservations/", response_model=schemas.Reservation)
async def create_reservation(
    reservation: schemas.ReservationCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(database.get_db)
):
    # Vérifier la disponibilité du livre via books-service
    try:
        book = await call_service(f"http://books-service/books/{reservation.book_id}")
        # Ici, on suppose qu'une clé 'available' indique la disponibilité du livre
        if not book.get("available", True):
            raise HTTPException(status_code=400, detail="Book is not available")
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Books service unavailable: {e}")

    # Vérifier l'existence du membre via members-service
    try:
        member = await call_service(f"http://members-service/members/{reservation.member_id}")
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Members service unavailable: {e}")

    # Créer la réservation
    db_reservation = models.Reservation(**reservation.dict())
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)

    # Publier un événement en arrière-plan (code à implémenter selon le message broker choisi)
    background_tasks.add_task(publish_reservation_event, "reservation.created", db_reservation.id)

    return db_reservation

async def publish_reservation_event(event_type: str, reservation_id: int):
    # Code pour publier l'événement vers un message broker (ex. RabbitMQ ou Kafka)
    pass
