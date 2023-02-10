from flask import Flask, request, jsonify
from pymongo import MongoClient
import requests
import json

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["events_db"]
events_collection = db["events"]

count = 0
SendUrlTTE = "http://localhost:5000/events"

@app.route("/events", methods=["GET", "POST"])
def events():
    global count
    if request.method == "POST":
        event = request.get_json()
        result = events_collection.insert_one(event)
        return "Event added successfully"
    elif request.method == "GET":
        events = events_collection.find()
        events = [event for event in events]
        return jsonify(events)

@app.route("/")
def index():
    return """
        <html>
          <head>
            <title>Events List</title>
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
            <script>
              function refreshEvents() {
                $.ajax({
                  url: "/events",
                  type: "GET",
                  success: function(events) {
                    $("#events-table tbody").empty();
                    events.forEach(function(event) {
                      $("#events-table tbody").append(
                        "<tr>" +
                        "<td>" + event["ControlRoomId"] + "</td>" +
                        "<td>" + event["ObjectId"] + "</td>" +
                        "<td>" + event["VehicleClass"] + "</td>" +
                        "<td>" + event["LaneId"] + "</td>" +
                        "<td>" + event["VehicleSpeed"] + "</td>" +
                        "<td>" + event["EventDateTime"] + "</td>" +
                        "</tr>"
                      );
                    });
                  }
                });
              }
              $(document).ready(function() {
                refreshEvents();
                setInterval(refreshEvents, 5000);
              });
            </script>
          </head>
          <body>
            <h1>Events List</h1>
            <table id="events-table">
              <thead>
                <tr>
                  <th>Control Room Id</th>
                  <th>Object Id</th>
                  <th>Vehicle Class</th>
                  <th>Lane Id</th>
                  <th>Vehicle Speed</th>
                  <th>Event Date Time</th>
                </tr>
              </thead>
              <tbody>
              </tbody>
            </table>
          </body>
        </html>
    """

if __name__ == "__main__":
    app.run(debug=True)
