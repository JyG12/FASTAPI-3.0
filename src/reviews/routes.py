#for api endpoints
from fastapi import APIRouter, Depends
from src.db.models import User
from .schemas import ReviewCreateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.auth.dependencies import get_current_user
from .service import ReviewService

#now need to create review router
review_router = APIRouter()
review_service = ReviewService()

@review_router.post('/book/{book_uid}')
async def add_review_to_books(
    book_uid: str,
    #data that will be used to add this review
    review_data: ReviewCreateModel,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)#session need import line 6
):
    new_review = await review_service.add_review_to_book(
        user_email = current_user.email,
        review_data = review_data,
        book_uid = book_uid,
        session = session
    )
    return new_review