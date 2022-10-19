from api import create_app
from flask import session
app = create_app()

@app.route('/', methods=['GET'])
def hello():
    return {'message': 'Hello, world!'}

if __name__ == '__main__':
    app.run(debug=True)