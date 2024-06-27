from abc import ABC, abstractmethod
import os
import json
import sqlite3

class CardDriver(ABC):
    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    def save_card(self, metadata):
        ...
    
    @abstractmethod
    def load_card(self, identifier):
        ...

    def get_creators(self):
        ...

    def get_creator_cards(self, creator):
        ...


class FilesystemDriver(CardDriver):
    def __init__(self, db_path):
        self.creators = []
        self.dir_path = dir_path

    def save_card(self, metadata):
        idendifier = metadata["idendifier"]
        new_dir_path = f"{self.dir_path}/{idendifier}"
        os.makedirs(new_dir_path)
        json_object = json.dumps(metadata, indent=4)
        json_path = os.path.join(new_dir_path, "metadata.json")
        with open(json_path, "w") as json_file:
            json_file.write(json_object)
        self.creators.append(metadata["creator"])


    def load_card(self, identifier: str):
        f = open(f"{self.dir_path}/{identifier}/metadata.json")
        data = json.load(f)
        return data

    def get_creators(self):
        return self.creators
    '''
    alternative implementation
    
    def get_creator_cards(self, creator):
        creator_cards = []
        for root, dirs, files in os.walk(self.dir_path):
            for dir_name in dirs:
                f = open(f"{self.dir_path}/{identifier}/metadata.json")
                data = json.load(f)
                if data["creator"] == creator:
                    creator_cards.append(data)
    '''

    def get_creator_cards(self, creator):
        creator_cards = []
        for root, dirs, files in os.walk(self.dir_path):
            for dir_name in dirs:
                id_creator = dir_name.split("_")[1]
                if id_creator == creator:
                    creator_cards.append(self.load_card(dir_name))
        return creator_cards



class SQLDriver(CardDriver):
    def __init__(self, db_path):
        self.db_path = db_path
    
    def save_card(self, metadata):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS cards (
                id INTEGER PRIMARY KEY,
                identifier TEXT NOT NULL,
                name TEXT NOT NULL,
                creator TEXT NOT NULL,
                riddle TEXT,
                solution TEXT,
                image_path TEXT
            )
        ''')
        cur.execute('''
            INSERT INTO cards (identifier, name, creator, riddle, solution, image_path)
            VALUES (:identifier, :name, :creator, :riddle, :solution, :image_path)
        ''', metadata)

        conn.commit()
        conn.close()




    def load_card(self, identifier):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute('SELECT * FROM cards')
        rows = cur.fetchall()
        cur.execute('SELECT * FROM cards WHERE identifier = ?', (identifier,))
        rows = cur.fetchall()
        for row in rows:
            conn.close()
            return row_to_dict(row)
            
    
    def get_creators(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute('SELECT DISTINCT creator FROM cards')
        rows = cur.fetchall()
        creators_list = [row[0] for row in rows]
        conn.close()
        return creators_list

    
    def get_creator_cards(self, creator):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute('SELECT * FROM cards WHERE creator = ?', (creator,))
        rows = cur.fetchall()
        creator_cards_medata = [row_to_dict(row) for row in rows]
        conn.close()
        return creator_cards_medata

def row_to_dict(row):
    return {
        'identifier': row[1],
        'name': row[2],
        'creator': row[3],
        'riddle': row[4],
        'solution': row[5],
        'image_path': row[6]
    }