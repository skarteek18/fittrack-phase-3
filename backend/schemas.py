

class Meal(Base):

    __tablename__ = "meals"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    meal_type = Column(
        String(50),
        nullable=False
    )

    food_name = Column(
        String(200),
        nullable=False
    )

    calories = Column(
        Float,
        nullable=False,
        default=0
    )

    protein = Column(
        Float,
        nullable=False,
        default=0
    )

    carbs = Column(
        Float,
        nullable=False,
        default=0
    )

    fats = Column(
        Float,
        nullable=False,
        default=0
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    __table_args__ = (
        CheckConstraint(
            "meal_type IN ('Breakfast', 'Lunch', 'Dinner', 'Snacks')",
            name="check_meal_type"
        ),
        CheckConstraint(
            "calories >= 0 AND protein >= 0 AND carbs >= 0 AND fats >= 0",
            name="check_meal_nutrition"
        ),
    )

    user = relationship(
        "User",
        back_populates="meals"
    )
