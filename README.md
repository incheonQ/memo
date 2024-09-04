### Bash에서 실행
  from app import db
   db.create_all()

### PythonAnywhere의 WSGI 설정 파일
```python
import sys
import os

# 프로젝트 디렉토리 경로 설정
# 데이터베이스 경로 설정
basedir = os.path.abspath(os.path.dirname(__file__))
project_folder = os.path.expanduser('~/mysite')  # 여기서 'mysite'는 여러분의 프로젝트 폴더명으로 변경해야 합니다.

# 프로젝트 디렉토리를 파이썬 경로에 추가
sys.path.insert(0, project_folder)

# Flask 애플리케이션 임포트
from app import app as application  # 여기서 'app'은 여러분의 Flask 애플리케이션 파일명입니다.
```
