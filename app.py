from flask import Flask, request, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import inspect, or_, case
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
from PIL import Image
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # 실제 운영 시 변경 필요
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///memos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/uploads')


db = SQLAlchemy(app)

# 뷰어 계정 생성 함수
def create_viewer_account():
    viewer = User.query.filter_by(username='viewer').first()
    if not viewer:
        viewer = User(username='viewer', is_viewer=True)
        viewer.set_password('viewerpassword')  # 실제 운영 시 더 복잡한 비밀번호 사용
        db.session.add(viewer)
        db.session.commit()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    is_viewer = db.Column(db.Boolean, default=False)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# 둘러보기 라우트
@app.route('/browse')
def browse():
    viewer = User.query.filter_by(username='viewer').first()
    if viewer:
        session['user_id'] = viewer.id
        flash('둘러보기 모드로 로그인되었습니다.', 'info')
    return redirect(url_for('index'))


class Memo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    details = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image_filename = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('memos', lazy=True))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # 사용자 이름 중복 확인
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('이미 존재하는 사용자 이름입니다.', 'error')
            return redirect(url_for('register'))

        # 비밀번호 확인
        if password != confirm_password:
            flash('비밀번호가 일치하지 않습니다.', 'error')
            return redirect(url_for('register'))

        # 새 사용자 생성
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('회원가입이 완료되었습니다. 로그인해주세요.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = authenticate(username, password)
        if user:
            session['user_id'] = user.id
            flash('로그인되었습니다.', 'success')
            return redirect(url_for('index'))
        else:
            flash('잘못된 사용자 이름 또는 비밀번호입니다.', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('로그아웃되었습니다.', 'success')
    return redirect(url_for('index'))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('로그인이 필요합니다.', 'error')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# 메모 수정/삭제 권한 확인 함수 수정
def check_memo_permission(memo, user):
    return user and (user.id == memo.user_id or user.is_admin) and not user.is_viewer


@app.route('/', methods=['GET', 'POST'])
def index():
    user = get_current_user()
    if request.method == 'POST':

        if not user or user.is_viewer:
            flash('메모를 작성하려면 로그인이 필요합니다.', 'error')
            return redirect(url_for('login'))

        memo_content = request.form['content']
        memo_category = request.form.get('category', '')
        memo_details = request.form.get('details', '')
        image = request.files.get('image')
        
        new_memo = Memo(content=memo_content, category=memo_category, details=memo_details, user_id=session['user_id'])
        
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            resize_image(image_path)
            new_memo.image_filename = filename
        
        try:
            db.session.add(new_memo)
            db.session.commit()
            flash('메모가 추가되었습니다.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'오류가 발생했습니다: {str(e)}', 'error')
        return redirect(url_for('index'))
    
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', '')
    search = request.args.get('search', '')
    
    query = Memo.query

    if category:
        query = query.filter_by(category=category)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(or_(Memo.content.like(search_term), 
                                 Memo.category.like(search_term), 
                                 Memo.details.like(search_term)))

    query = query.order_by(
        case((Memo.category == '중요', 0), else_=1),
        Memo.created_at.desc()
    )
    
    
    pagination = query.order_by(Memo.created_at.desc()).paginate(page=page, per_page=10, error_out=False)
    
    categories = db.session.query(Memo.category).distinct().all()

    current_user = get_current_user()

    return render_template('index.html', pagination=pagination, categories=categories, 
                           current_category=category, search=search, current_user=current_user,
                           check_memo_permission=check_memo_permission)


def get_current_user():
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

def resize_image(image_path, max_size=(800, 800)):
    with Image.open(image_path) as img:
        img.thumbnail(max_size, Image.LANCZOS)
        img.save(image_path, optimize=True, quality=85)

def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user
    return None

def check_memo_permission(memo, user):
    return user and (user.id == memo.user_id or user.is_admin) and not user.is_viewer

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    memo = Memo.query.get_or_404(id)
    user = get_current_user()
    if not check_memo_permission(memo, user):
        flash('수정 권한이 없습니다.', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        print("POST 요청 받음")
        print("폼 데이터:", request.form)
        print("파일:", request.files)
        
        content = request.form.get('content')
        print("Content:", content)
        
        if not content:
            flash('메모 내용을 입력해주세요.', 'error')
            return render_template('edit.html', memo=memo)

        memo.content = content
        memo.category = request.form.get('category', '')
        memo.details = request.form.get('details', '')
        
        try:
            db.session.commit()
            flash('메모가 수정되었습니다.', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'수정 중 오류가 발생했습니다: {str(e)}', 'error')

    return render_template('edit.html', memo=memo)

@app.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    memo = Memo.query.get_or_404(id)
    user = get_current_user()
    if not check_memo_permission(memo, user):
        flash('삭제 권한이 없습니다.', 'error')
        return redirect(url_for('index'))

    try:
        db.session.delete(memo)
        db.session.commit()
        flash('메모가 삭제되었습니다.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'삭제 중 오류가 발생했습니다: {str(e)}', 'error')
    return redirect(url_for('index'))

@app.route('/category/<category>')
def filter_by_category(category):
    page = request.args.get('page', 1, type=int)
    pagination = Memo.query.filter_by(category=category).order_by(Memo.created_at.desc()).paginate(page=page, per_page=10, error_out=False)
    categories = db.session.query(Memo.category).distinct().all()
    return render_template('index.html', pagination=pagination, categories=categories, current_category=category)

@app.route('/memo/<int:id>')
def memo_detail(id):
    memo = Memo.query.get_or_404(id)
    return render_template('memo_detail.html', memo=memo)

def init_db():
    with app.app_context():
        inspector = inspect(db.engine)
        if not inspector.has_table("user"):  # 'user' 테이블이 없는 경우에만
            db.create_all()  # 새로운 테이블 생성
            create_admin()  # 관리자 계정 생성
            create_viewer_account()  # 뷰어 계정 생성
            print("데이터베이스가 초기화되었습니다.")
        else:
            print("데이터베이스가 이미 존재합니다.")
            create_admin()  # 관리자 계정이 없는 경우 생성
            create_viewer_account()  # 뷰어 계정이 없는 경우 생성


def create_admin():
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', is_admin=True)
        admin.set_password('smpeople')  # 실제 운영 시 강력한 비밀번호로 변경 필요
        db.session.add(admin)
        db.session.commit()
        print("관리자 계정이 생성되었습니다.")
    else:
        print("관리자 계정이 이미 존재합니다.")

if __name__ == '__main__':
    init_db()  # 데이터베이스 초기화 및 관리자 계정 생성
    app.run(debug=True)