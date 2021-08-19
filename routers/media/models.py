from sqlalchemy import Column, Integer, ForeignKey, CheckConstraint, event
from sqlalchemy.orm import relationship
from mixins import ImageMixin
from database import Base

class Image(ImageMixin, Base):
    '''Image Model'''
    __tablename__ = "images"
    __table_args__ = (
        CheckConstraint(
            """
                ((meal_id IS NOT NULL AND COALESCE(col1, col2, col3, col4) IS NULL) 
                OR (col1 IS NOT NULL AND COALESCE(col2, col3, col4) IS NULL) 
                OR (col2 IS NOT NULL AND COALESCE(col1, col3, col4) IS NULL) 
                OR (col3 IS NOT NULL AND COALESCE(col1, col2, col4) IS NULL) 
                OR (col4 IS NOT NULL AND COALESCE(col1, col2, col3) IS NULL) ) AND
                COALESCE(meal_id, col1, col2, col3, col4) IS NOT NULL
            """
        , name="ck_im_assoc_single_fk_allowed"),
    )

    meal_id = Column(Integer, ForeignKey('meals.id'))
    menu_id = Column(Integer, ForeignKey('menus.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    
    col1 = Column(Integer)
    col2 = Column(Integer)
    col3 = Column(Integer)
    col4 = Column(Integer)

# after delete to remove from file system
# @event.listens_for(Image.__table__, 'after_delete')
# def remove_file(mapper, connection, target):
#     pass