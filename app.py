from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import inspect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # 실제 운영 시 변경 필요
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///memos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Memo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    details = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        memo_content = request.form['content']
        memo_category = request.form.get('category', '')
        new_memo = Memo(content=memo_content, category=memo_category)
        try:
            db.session.add(new_memo)
            db.session.commit()
            flash('메모가 추가되었습니다.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'오류가 발생했습니다: {str(e)}', 'error')
        return redirect(url_for('index'))
    
    page = request.args.get('page', 1, type=int)
    pagination = Memo.query.order_by(Memo.created_at.desc()).paginate(page=page, per_page=10, error_out=False)
    categories = db.session.query(Memo.category).distinct().all() 
    return render_template('index.html', pagination=pagination, categories=categories)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    memo = Memo.query.get_or_404(id)
    if request.method == 'POST':
        memo.content = request.form['content']
        memo.details = request.form['details']
        memo.category = request.form.get('category', '')
        try:
            db.session.commit()
            flash('메모가 수정되었습니다.', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'수정 중 오류가 발생했습니다: {str(e)}', 'error')
    return render_template('edit.html', memo=memo)

@app.route('/delete/<int:id>')
def delete(id):
    memo = Memo.query.get_or_404(id)
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
        if not inspector.has_table("memo"):  # 'memo' 테이블이 없는 경우에만
            db.create_all()  # 새로운 테이블 생성
            print("데이터베이스가 초기화되었습니다.")
        
if __name__ == '__main__':
    init_db()  # 애플리케이션 실행 전에 데이터베이스 확인 및 초기화
    app.run(debug=True)