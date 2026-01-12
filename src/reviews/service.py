# for crud stuff
from src.db.models import Review
from src.auth.service import UserService
from src.books.service import BookService
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import status
from fastapi.exceptions import HTTPException
from .schemas import ReviewCreateModel
import logging

book_service = BookService()
user_service = UserService()

class ReviewService:
    async def add_review_to_book(
        self,
        user_email: str,
        book_uid: str,
        review_data: ReviewCreateModel,
        session: AsyncSession,
    ):
    
        try:
            book = await book_service.get_book(
                book_uid = book_uid,
                session = session
            )
    
        #now get the user who is making this request
            user = await user_service.get_user_by_email(
                email = user_email,
                session = session
        )
        
            review_data_dict = review_data.model_dump()
        
            new_review = Review(**review_data_dict)
        
            if not book:
                raise HTTPException(
                    status_code = status.HTTP_404_NOT_FOUND,
                    detail = "Book not found"
                )
        
            if not user:
                raise HTTPException(
                    status_code = status.HTTP_404_NOT_FOUND,
                    detail = "User not found"
                )
            
        #now need to make sure that this review has both the user and the book associated with it
       #only when both user and book exist then u continue below steps, skipping the both if 
            new_review.user = user
            new_review.book = book
        
        #use our session to commit this to our database
        
            session.add(new_review)
        
            await session.commit()
        
            return new_review
            
            
        except Exception as e:
            logging.exception(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Oops...Something went wrong!"
            )
