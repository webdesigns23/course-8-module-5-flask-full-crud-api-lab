from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# Read events
@app.route("/events/<int:event_id>", methods=["GET"])
def get_event(event_id):
    event = next((event for event in events if event.id == event_id), None)
    if event:
        return jsonify(event.to_dict())
    else:
        return ("Event not found", 404)
    
# Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()
    new_id = max([event.id for event in events]) + 1 if events else 1
    new_event = Event(id=new_id, title=data["title"])
    events.append(new_event)
    return jsonify(new_event.to_dict()), 201

# Update the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    data = request.get_json()
    event = next((event for event in events if event.id == event_id), None)
    if not event:
        return ("Event not found", 404)
    if "title" in data:
        event.title = data["title"]
    return jsonify(event.to_dict())

# Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    global events
    event = next((event for event in events if event.id == event_id), None)
    if not event:
        return ("Event not found", 404)
    events = [event for event in events if event.id != event_id]
    return ("Event deleted", 204)

if __name__ == "__main__":
    app.run(debug=True)
