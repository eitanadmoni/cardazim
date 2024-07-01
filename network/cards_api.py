from flask import Flask, request, jsonify, send_file
from saver import Saver
from PIL import Image
import sys
import sqlite3



def create_app(database_url):
    app = Flask(__name__)
    app.db = Saver(database_url)

    @app.route('/')       
    def hello(): 
        return 'Welcome to Cardazim'

    @app.route('/creators')
    def get_creators():
        return jsonify(app.db.driver.get_creators())


    @app.route('/creators/<creator>/cards/solved')
    def get_solved_from_creator(creator):
        solved_cards = []
        cards = app.db.driver.get_creator_cards(creator)
        for card in cards:
            if card['solution'] != None:
                card.pop('key_hash')
                solved_cards.append(card)
        return jsonify(solved_cards)


    @app.route('/creators/<creator>/cards/unsolved')
    def get_unsolved_from_creator(creator):
        unsolved_cards = []
        cards = app.db.driver.get_creator_cards(creator)
        for card in cards:
            print(card)
            if card['solution'] == None:
                card.pop('key_hash')
                unsolved_cards.append(card)
        return jsonify(unsolved_cards)


    @app.route('/creators/<creator>/cards/<card_name>')
    def get_specific_card(card_name, creator):
        cards = app.db.driver.get_creator_cards(creator)
        for card in cards:
            if card['name'] == card_name:
                return jsonify(card)


    @app.route('/creators/<creator>/cards/<card_name>/image.jpg')
    def get_card_image(card_name, creator):
        cards = app.db.driver.get_creator_cards(creator)
        for card in cards:
            print(card)
            if card['name'] == card_name:
                return send_file(card['image_path'], mimetype='image/jpeg')
    

    @app.route('/cards/find')
    def find_by_parameters():
        creator = request.args.get('creator')
        name = request.args.get('name')
        riddle = request.args.get('riddle')
        cards = app.db.find_by_parameters(name, creator, riddle)
        return jsonify(cards)        


            
    
    @app.route('/cards/<card_id>/solve', methods=['POST'])
    def check_solution(card_id):
        req_data = request.get_json()
        if 'solution' not in req_data:
            return jsonify({
                'status': 'failure',
                'message': 'Solution not provided'
            }), 400
        card = app.db.load(card_id)
        image_path = app.db.driver.load_card(card_id)['image_path']
        decryption = card.image.decrypt(req_data['solution'])
        card.image.image.show()
        if not decryption:
            return jsonify({
                'status': 'failure',
                'message': 'Incorrect solution'
            }), 200
        else:
            card.solution = req_data['solution']
            app.db.save(card)
            update_image(card.image.image, image_path)
            return jsonify({
                'status': 'success',
                'message': 'Solution is correct. Card marked as solved.'
            }), 200

    
    
    
    return app

def run_api_server(host, port, database_url):
    app = create_app(database_url)
    app.run(host=host, port=port, debug=True)


def update_image(image, image_path):
    image.save(image_path, "JPEG")




if __name__=='__main__': 
    argv = sys.argv
    run_api_server(argv[1], argv[2], argv[3]) 