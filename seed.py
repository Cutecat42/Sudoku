from werkzeug.security import generate_password_hash

from models import db, User, PersonalBest
from app import app

db.drop_all()
db.create_all()

# Create users
ss = User(name="SS",username="SallySam",password=generate_password_hash("shdgfyr123", method='sha256'),total_played=91)
may = User(name="May",username="Applexd0",password=generate_password_hash("shdgfyr123", method='sha256'),total_played=10)
sandy = User(name="Sandy Meza",username="hot_ones_35",password=generate_password_hash("shdgfyr123", method='sha256'),total_played=39)
annie = User(name="annie",username="annie1990",password=generate_password_hash("shdgfyr123", method='sha256'),total_played=32)
sean = User(name="sean rhett",username="gm_BrownShu",password=generate_password_hash("shdgfyr123", method='sha256'),total_played=45)
ss1 = User(name="G",username="g_major",password=generate_password_hash("shdgfyr123", method='sha256'),total_played=11)
may1 = User(name="s mantel",username="SantaPop",password=generate_password_hash("shdgfyr123", method='sha256'),total_played=10)
sandy1 = User(name="G Harmon",username="gooeyZz",password=generate_password_hash("shdgfyr123", method='sha256'),total_played=42)
annie1 = User(name="Lilly",username="lillypuff08",password=generate_password_hash("shdgfyr123", method='sha256'),total_played=32)
sean1 = User(name="mm",username="mandymantha",password=generate_password_hash("shdgfyr123", method='sha256'),total_played=48)

db.session.add(ss)
db.session.add(may)
db.session.add(sandy)
db.session.add(annie)
db.session.add(sean)
db.session.add(ss1)
db.session.add(may1)
db.session.add(sandy1)
db.session.add(annie1)
db.session.add(sean1)
db.session.commit()

# Create personal bests

easy1 = PersonalBest(level="Easy",time="06:01",user_id=1)
easy2 = PersonalBest(level="Easy",time="03:52",user_id=8)
easy3 = PersonalBest(level="Easy",time="05:21",user_id=3)
easy4 = PersonalBest(level="Easy",time="12:22",user_id=7)
easy5 = PersonalBest(level="Easy",time="10:56",user_id=5)
medium1 = PersonalBest(level="Medium",time="07:45",user_id=6)
medium2= PersonalBest(level="Medium",time="08:31",user_id=7)
medium3 = PersonalBest(level="Medium",time="05:32",user_id=2)
medium4 = PersonalBest(level="Medium",time="06:37",user_id=4)
medium5 = PersonalBest(level="Medium",time="05:59",user_id=5)
hard1 = PersonalBest(level="Hard",time="13:56",user_id=1)
hard2 = PersonalBest(level="Hard",time="15:42",user_id=2)
hard3 = PersonalBest(level="Hard",time="12:12",user_id=5)
hard4 = PersonalBest(level="Hard",time="13:59",user_id=4)
hard5 = PersonalBest(level="Hard",time="10:29",user_id=7)

db.session.add(easy1)
db.session.add(easy2)
db.session.add(easy3)
db.session.add(easy4)
db.session.add(easy5)
db.session.add(medium1)
db.session.add(medium2)
db.session.add(medium3)
db.session.add(medium4)
db.session.add(medium5)
db.session.add(hard1)
db.session.add(hard2)
db.session.add(hard3)
db.session.add(hard4)
db.session.add(hard5)
db.session.commit()