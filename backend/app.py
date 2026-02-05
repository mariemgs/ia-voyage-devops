from flask import Flask, request, jsonify, url_for, send_from_directory
from flask_cors import CORS
from experta import *
import os

app = Flask(__name__)
CORS(app)

app.config["UPLOAD_FOLDER"] = os.path.join(os.getcwd(), "backend", "image")

@app.route('/images/<path:filename>')
def serve_image(filename):
    """Serve image files from the image folder."""
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


class TravelAdvisor(KnowledgeEngine): 
    DESTINATIONS = [
        # Low Budget - Beach
        {"name": "Algarve", "budget": "low", "period": "summer", "type": "beach", "image_path": "algarve.jpg"},
        {"name": "Barcelona", "budget": "low", "period": "summer", "type": "beach", "image_path": "barcelona.jpg"},
        {"name": "Bali", "budget": "low", "period": "summer", "type": "beach", "image_path": "bali.jpg"},
        {"name": "Goa", "budget": "low", "period": "winter", "type": "beach", "image_path": "goa.jpg"},
        {"name": "Phuket", "budget": "low", "period": "autumn", "type": "beach", "image_path": "phuket.jpg"},

        # Medium Budget - Beach
        {"name": "Cancun", "budget": "medium", "period": "spring", "type": "beach", "image_path": "cancun.jpg"},
        {"name": "Maldives", "budget": "medium", "period": "summer", "type": "beach", "image_path": "maldives.jpg"},
        {"name": "Hawaii", "budget": "medium", "period": "winter", "type": "beach", "image_path": "hawaii.jpg"},
        {"name": "Maui", "budget": "medium", "period": "autumn", "type": "beach", "image_path": "maui.jpg"},

        # High Budget - Beach
        {"name": "Fiji", "budget": "high", "period": "spring", "type": "beach", "image_path": "fiji.jpg"},
        {"name": "Seychelles", "budget": "high", "period": "summer", "type": "beach", "image_path": "seychelles.jpg"},
        {"name": "Bora Bora", "budget": "high", "period": "winter", "type": "beach", "image_path": "borabora.jpg"},

        # Low Budget - Mountain
        {"name": "Himalayas", "budget": "low", "period": "autumn", "type": "mountain", "image_path": "himalayas.jpeg"},
        {"name": "Rocky Mountains", "budget": "low", "period": "winter", "type": "mountain", "image_path": "rockymountains.jpg"},
        {"name": "Atlas Mountains", "budget": "low", "period": "spring", "type": "mountain", "image_path": "atlasmountains.jpg"},

        # Medium Budget - Mountain
        {"name": "Swiss Alps", "budget": "medium", "period": "winter", "type": "mountain", "image_path": "swissalps.jpg"},
        {"name": "Andes", "budget": "medium", "period": "summer", "type": "mountain", "image_path": "andes.jpg"},
        {"name": "Dolomites", "budget": "medium", "period": "spring", "type": "mountain", "image_path": "dolomites.jpg"},

        # High Budget - Mountain
        {"name": "Kilimanjaro", "budget": "high", "period": "autumn", "type": "mountain", "image_path": "kilimanjaro.jpg"},
        {"name": "Patagonian Andes", "budget": "high", "period": "spring", "type": "mountain", "image_path": "patagonian_andes.jpg"},
        {"name": "Hokkaido Mountains", "budget": "high", "period": "winter", "type": "mountain", "image_path": "hokkaido_mountains.jpg"},

        # Low Budget - City
        {"name": "Bangkok", "budget": "low", "period": "summer", "type": "city", "image_path": "bangkok.jpg"},
        {"name": "Prague", "budget": "low", "period": "autumn", "type": "city", "image_path": "prague.jpg"},
        {"name": "Budapest", "budget": "low", "period": "winter", "type": "city", "image_path": "budapest.jpg"},

        # Medium Budget - City
        {"name": "Barcelona", "budget": "medium", "period": "spring", "type": "city", "image_path": "barcelona.jpg"},
        {"name": "New York", "budget": "medium", "period": "autumn", "type": "city", "image_path": "New York.jpg"},
        {"name": "Tokyo", "budget": "medium", "period": "summer", "type": "city", "image_path": "Tokyo.jpg"},

        # High Budget - City
        {"name": "Paris", "budget": "high", "period": "spring", "type": "city", "image_path": "Paris.jpg"},
        {"name": "Kyoto", "budget": "high", "period": "autumn", "type": "city", "image_path": "Kyoto.jpg"},
        {"name": "Dubai", "budget": "high", "period": "winter", "type": "city", "image_path": "dubai.jpg"},

        # Low Budget - Nature
        {"name": "Kerala", "budget": "low", "period": "autumn", "type": "nature", "image_path": "kerala.jpg"},
        {"name": "Plitvice Lakes", "budget": "low", "period": "spring", "type": "nature", "image_path": "plitvice_lakes.jpg"},
        {"name": "Lake District", "budget": "low", "period": "summer", "type": "nature", "image_path": "lake_district.jpeg"},

        # Medium Budget - Nature
        {"name": "Banff National Park", "budget": "medium", "period": "winter", "type": "nature", "image_path": "banff_national_park.jpeg"},
        {"name": "Kruger National Park", "budget": "medium", "period": "spring", "type": "nature", "image_path": "kruger_national_park.jpeg"},
        {"name": "Galapagos Islands", "budget": "medium", "period": "autumn", "type": "nature", "image_path": "galapagos_islands.jpeg"},

        # High Budget - Nature
        {"name": "Amazon Rainforest", "budget": "high", "period": "summer", "type": "nature", "image_path": "Amazon Rainforest.jpeg"},
        {"name": "Serengeti", "budget": "high", "period": "autumn", "type": "nature", "image_path": "serengeti.jpeg"},
        {"name": "Antarctica", "budget": "high", "period": "winter", "type": "nature", "image_path": "Antarctica.jpeg"},
    ]

    @DefFacts()
    def _initial_action(self):
        yield Fact(action="find_destination")

    @Rule(Fact(action='find_destination'), 
          Fact(budget=MATCH.budget), 
          Fact(period=MATCH.period), 
          Fact(type=MATCH.type))
    def find_destinations(self, budget, period, type):
        matches = [
            d for d in self.DESTINATIONS
            if d["budget"] == budget and d["period"] == period and d["type"] == type
        ]
        for destination in matches:
            self.declare(Fact(destination=destination))


@app.route('/', methods=['GET', 'POST'])
def index():
    destinations = []
    if request.method == 'POST':
        data = request.json
        budget = data['budget']
        period = data['period']
        travel_type = data['type']

        advisor = TravelAdvisor()
        advisor.reset()
        advisor.declare(Fact(budget=budget))
        advisor.declare(Fact(period=period))
        advisor.declare(Fact(type=travel_type))
        advisor.run()

        for fact in advisor.facts.values():
            if isinstance(fact, Fact) and 'destination' in fact:
                destination = fact['destination']
                image_url = url_for('serve_image', filename=destination["image_path"], _external=True)
                destinations.append({
                    "name": destination["name"],
                    "image_url": image_url
                })

    return jsonify(destinations if destinations else {"message": "No destinations found."})


if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
