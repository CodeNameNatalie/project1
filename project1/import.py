import csv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

#check for environment var
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

#set up database
    #database engine object from SQLAlchemy to manage connections to database
engine = create_engine(os.getenv("DATABASE_URL"))
    #ensure session maker is scoped to keep different users actions separate
db = scoped_session(sessionmaker(bind=engine))

def main():
    db.execute("INSERT INTO books (isbn varchar(50), title var char(900), author varchar(400), year(integer)")
    #import, open, and read books.csv
    file = open("books.csv")
    reader = csv.reader(file)

	#organize books.csv into categories by isbn, title, author, year
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
        {"isbn": isbn, "title": title, "author": author, "year": year})
    #print book added
        print(f"Added book {isbn} ISBN {title} titled by {author} from {year} year")
    #commit
    db.commit()

#only runs when this is program is run
if __name__ == "__main__":
    main()