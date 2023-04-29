"""Flask app for adopt app."""

import os
import requests

from flask import Flask, render_template, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Pets, Pet_Finder_Pets

from forms import AddPetForm, EditPetForm

app = Flask(__name__)

app.config["SECRET_KEY"] = "secret"

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///adopt"
)

PETFINDER_API_KEY = os.environ['PET_FINDER_API_SECRET_KEY']
PETFINDER_SECRET_KEY = os.environ['SECRET_KEY']
PETFINDER_ACCESS_TOKEN = os.environ['ACCESS_TOKEN']

connect_db(app)

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)


@app.get("/")
def get_homepage():
    """Displays a list of all pets."""

    pets = Pets.query.all()
    pet_finder_pet = Pet_Finder_Pets.query.all()

    return render_template("list_pets.html", pets=pets, pet_finder_pet=Pet_Finder)


@app.route("/add", methods=["GET", "POST"])
def add_pet_form():
    """Displays a form to add a pet for adoption; handle adding."""

    form = AddPetForm()

    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data

        new_pet = Pets(
            name=name, species=species, photo_url=photo_url, age=age, notes=notes
        )

        db.session.add(new_pet)
        db.session.commit()

        flash(f"Added pet {name} to adoption list!")
        return redirect("/")

    else:
        return render_template("pet_add_form.html", form=form)


@app.route("/<pet_id>", methods=["GET", "POST"])
def display_edit_pet_form(pet_id):
    """Displays a page with information about the pet and a form to edit the
    pet information."""

    pet = Pets.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data

        db.session.commit()

        flash(f"Pet {pet.name} information updated!")
        return redirect("/")

    else:
        return render_template("pet_display_edit.html", form=form, pet=pet)

@app.get("/random/pet")
def get_random_pet():

    resp = requests.get("https://api.petfinder.com/v2/animals", 
                        params={"limit": "100"},
                        headers={f"Authorization: Bearer {PETFINDER_ACCESS_TOKEN}"})
    
    random_pet_data = resp.json()

    name = random_pet_data.animals[0].name
    photo_url = random_pet_data.animals[0].photos[0].small
    age = random_pet_data.animals[0].age

    new_pet = Pet_Finder_Pets(name=name, photo_url=photo_url, age=age)

    db.session.add(new_pet)
    db.session.commit()

    return render_template("list_pets.html", pet_finder_pet=new_pet)
    