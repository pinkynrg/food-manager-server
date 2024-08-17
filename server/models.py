from server import db

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    expiration_date = db.Column(db.Date, nullable=False)
    opened_date = db.Column(db.Date)
    expiration_days_after_open = db.Column(db.Integer, default=7)
    user_id = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Item {self.name}>'
