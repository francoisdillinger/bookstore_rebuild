from flask import request, Blueprint, jsonify, session
from ..models import User, Book, db

books = Blueprint('books', __name__)

@books.route('/books', methods=['GET'])
def get_books():
    book_results = Book.query.all()
    book_list = []
    for book in book_results:
        book_list.append({
             "isbn": book.isbn,
            "author": book.author,
            "title": book.title,
            "price": book.price,
            "stock_quantity": book.stock_quantity,
            "description": book.description,
            "category": book.category,
            "image_file": book.image_file,
        })
    return jsonify({'books': book_list}), 200


@books.route('/books', methods=['POST'])
def create_book():
    user_id = session.get('user_id')
    if user_id:
        user_is_admin = check_admin_status(user_id)
        if user_is_admin:
            book_exists = Book.query.filter_by(isbn=int(request.json['isbn'])).first()

            if not book_exists:   
                # image = request.files['image_file']
                # new_image_name = check_image_file_and_save(image, 'book_images')
                # book_image = 'stock.jpg'
                # if new_image_name:
                #     book_image = new_image_name
                book = Book(
                    isbn = int(request.json['isbn']), 
                    author = request.json['author'],  
                    title = request.json['title'], 
                    price = float(request.json['price']),
                    stock_quantity = int(request.json['stock_quantity']), 
                    description = request.json['description'], 
                    category = request.json['category'], 
                    image_file = 'stock.jpg')

                db.session.add(book)
                db.session.commit()

                return jsonify({
                    "isbn" : int(request.json['isbn']),
                    "author": request.json['author'],
                    "title" : request.json['title'],
                    "price" : float(request.json['price']),
                    "stock_quantity" : int(request.json['stock_quantity']),
                    "description" : request.json['description'],
                    "category" : request.json['category'],
                    "book_image": "stock.jpg",
                    }), 201
            else:
                return {"error":"This book already exists."}, 409
        else:
            return {"error":"User is not Authorized"}, 401    
    else:
        return {"error": "User not logged in."}

def check_admin_status(user_id):
    user = User.query.filter_by(id=user_id).first()
    return (user.admin_status == True)

# def check_image_file_and_save(image, img_folder):
#     image_name = image.filename
#     _, ext = os.path.splitext(image_name)
#     if image_name:
#         if ext != '.jpg' and ext != '.png':
#             flash('Not proper file format. Must be .jpg or .png, default image selected.', category='error')
#         else:
#             file_hex = secrets.token_hex(8)
#             path_hex = file_hex + ext
#             full_img_path = os.path.join(os.path.realpath("bookstore"), f'static/{img_folder}', path_hex)
#             new_size = (300, 300)
#             resized_image = Image.open(image)
#             resized_image.thumbnail(new_size)
#             resized_image.save(full_img_path)
#             return path_hex