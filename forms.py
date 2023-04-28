from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField

from wtforms.validators import AnyOf, URL, Optional

"""Forms for adopt app."""


class AddPetForm(FlaskForm):
    """Form for adding a pet."""

    name = StringField("Pet Name")
    species = StringField(
        "Pet Species",
        validators=[
            AnyOf(
                ["cat", "dog", "porcupine"],
                "The pet species must be cat, dog, or porcupine",
            )
        ],
    )
    photo_url = StringField(
        "Pet Photo URL",
        validators=[
            Optional(),
            URL(require_tld=False, message="Please enter a valid URL"),
        ],
    )
    age = SelectField(
        "Choose a pet age",
        choices=[
            ("baby", "baby"),
            ("young", "young"),
            ("adult", "adult"),
            ("senior", "senior"),
        ],
        validators=[
            AnyOf(
                ["baby", "young", "adult", "senior"],
                "The pet age must be baby, young, adult, or senior",
            )
        ],
    )
    notes = StringField("Other Pet Notes")


class EditPetForm(FlaskForm):
    """Form for editing the pet information."""

    photo_url = StringField(
        "Pet Photo URL",
        validators=[
            Optional(),
            URL(require_tld=False, message="Please enter a valid URL"),
        ],
    )
    notes = StringField("Other Pet Notes")
    available = BooleanField("Pet available for adoption?")
