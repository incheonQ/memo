from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import inspect
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # 실제 운영 시 변경 필요


# 데이터베이스 경로 설정
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'memos.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Memo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    details = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        memo_content = request.form['content']
        new_memo = Memo(content=memo_content)
        try:
            db.session.add(new_memo)
            db.session.commit()
            flash('메모가 추가되었습니다.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'오류가 발생했습니다: {str(e)}', 'error')
        return redirect(url_for('index'))

    memos = Memo.query.order_by(Memo.created_at.desc()).all()
    return render_template('index.html', memos=memos)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    memo = Memo.query.get_or_404(id)
    if request.method == 'POST':
        memo.content = request.form['content']
        memo.details = request.form['details']
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

def init_db():
    with app.app_context():
        inspector = inspect(db.engine)
        if not inspector.has_table("memo"):  # 'memo' 테이블이 없는 경우에만
            db.create_all()  # 새로운 테이블 생성
            print("데이터베이스가 초기화되었습니다.")

if __name__ == '__main__':
    init_db()  # 애플리케이션 실행 전에 데이터베이스 확인 및 초기화
    app.run(debug=True)
