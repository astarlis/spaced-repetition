from app import app
from app.models import user
from app.__init__ import db

if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True)
