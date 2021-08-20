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
                (
                    (meal_id IS NOT NULL AND COALESCE(menu_id, category_id, restaurant_id) IS NULL) 
                OR  (menu_id IS NOT NULL AND COALESCE(meal_id, category_id, restaurant_id) IS NULL) 
                OR  (category_id IS NOT NULL AND COALESCE(menu_id, meal_id, restaurant_id) IS NULL) 
                OR  (restaurant_id IS NOT NULL AND COALESCE(menu_id, meal_id, category_id) IS NULL) 
                ) 
                AND COALESCE(meal_id, menu_id, category_id, restaurant_id) IS NOT NULL
            """
        , name="ck_img_assoc_single_fk_allowed"),
    )

    meal_id = Column(Integer, ForeignKey('meals.id'))
    menu_id = Column(Integer, ForeignKey('menus.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    
# after delete to remove from file system
# @event.listens_for(Image.__table__, 'before_delete')
# def remove_file(mapper, connection, target):
#     pass