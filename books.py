import os
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)


class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    author = db.relationship('Author', backref=db.backref('written', lazy=True))

    def __repr__(self):
        return "<Title: {}>".format(self.title)


class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return "<Author: {}>".format(self.name)


@app.route('/', methods=["GET", "POST"])
def home():
    books = None
    if request.form:
        try:
            book = Book(title=request.form.get("title"), author_id=request.form.get("author"))
            db.session.add(book)
            db.session.commit()
        except Exception as e:
            print("Failed to add book")
            print(e)
    # books = db.session.query(Book, Author.name).join(Author)
    books = Book.query.all()
    authors = Author.query.all()
    return render_template("home.html", books=books, authors=authors)


@app.route('/author', methods=["GET", "POST"])
def author():
    authors = None
    if request.form:
        try:
            author = Author(name=request.form.get("surname"))
            db.session.add(author)
            db.session.commit()
        except Exception as e:
            print("Failed to add author")
            print(e)
    # books = db.session.query(Book, Author.name).join(Author)
    books = Book.query.all()
    authors = Author.query.all()
    return render_template("home.html", books=books, authors=authors)


@app.route("/update", methods=["POST"])
def update():
    try:
        newtitle = request.form.get("newtitle")
        oldtitle = request.form.get("oldtitle")
        book = Book.query.filter_by(title=oldtitle).first()
        book.title = newtitle
        db.session.commit()
    except Exception as e:
        print("Can't update book")
        print(e)
    return redirect("/")


@app.route("/updateauthor", methods=["POST"])
def update_author():
    try:
        oldID = request.form.get("oldID")
        newauthorid = request.form.get("newauthorid")
        # oldauthorid = request.form.get("oldauthorid")
        book = Book.query.filter_by(id=oldID).first()
        book.author_id = newauthorid
        db.session.commit()
    except Exception as e:
        print("Can't update author")
        print(e)
    return redirect("/")

@app.route("/updatename", methods=["POST"])
def update_name():
    try:
        oldid = request.form.get("oldaid")
        newaname = request.form.get("newaname")
        oldaname = request.form.get("oldaname")
        author = Author.query.filter_by(id=oldid).first()
        author.name = newaname
        db.session.commit()
    except Exception as e:
        print("Can't update author")
        print(e)
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    book = Book.query.filter_by(title=title).first()
    db.session.delete(book)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
