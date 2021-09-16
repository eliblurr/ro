from sqlalchemy import Column, String, Integer, ForeignKey, CheckConstraint, event
from sqlalchemy.orm import relationship
from mixins import BaseMixin
from database import Base

class Image(BaseMixin, Base):
    '''Image Model'''
    __tablename__ = "images"
    __table_args__ = (
        CheckConstraint(
            """
                (
                    (ad_id IS NOT NULL AND COALESCE(meal_id, menu_id, category_id, restaurant_id) IS NULL)
                OR  (meal_id IS NOT NULL AND COALESCE(ad_id, menu_id, category_id, restaurant_id) IS NULL) 
                OR  (menu_id IS NOT NULL AND COALESCE(meal_id, ad_id, category_id, restaurant_id) IS NULL) 
                OR  (category_id IS NOT NULL AND COALESCE(meal_id, menu_id, ad_id, restaurant_id) IS NULL) 
                OR  (restaurant_id IS NOT NULL AND COALESCE(meal_id, menu_id, category_id, ad_id) IS NULL) 
                ) 
                AND COALESCE(ad_id, meal_id, menu_id, category_id, restaurant_id) IS NOT NULL
            """
        , name="ck_img_assoc_single_fk_allowed"),
    )

    small = Column(String, nullable=True)
    detail = Column(String, nullable=True)
    listquad = Column(String, nullable=True)
    thumbnail = Column(String, nullable=True)

    ad_id = Column(Integer, ForeignKey('ads.id'))
    meal_id = Column(Integer, ForeignKey('meals.id'))
    menu_id = Column(Integer, ForeignKey('menus.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    
# Remove from File System after_delete
@event.listens_for(Image, 'after_delete')
def remove_file(mapper, connection, target):
    pass