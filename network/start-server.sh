echo [SERVER] Installing dependencies…
pip3 install flask
pip3 install pillow
pip3 install PyCryptodome
pip3 install sqlite3
echo [SERVER] Done installing dependencies…
echo [SERVER] Starting server...
python3 cards_api.py 127.0.0.1 5000 sql://database.db > /dev/null 2>&1 &
sleep 5
echo [SERVER] Server running!