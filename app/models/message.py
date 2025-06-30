from datetime import datetime
from app import db

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    autor = db.Column(db.Integer, db.ForeignKey('users.id'))

    def to_dict(self):
        return {
            "id": self.id,
            "autor":self.autor,
            "content": self.content,
            "created_at": self.created_at.isoformat()
        }