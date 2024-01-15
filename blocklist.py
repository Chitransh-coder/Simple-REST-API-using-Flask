from db import db

class Blocklist(db.Model):
    __tablename__ = 'blocklist'

    token = db.Column(db.String(512), primary_key=True)
