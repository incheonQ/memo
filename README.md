## 프로젝트 설명
<p>
  이 프로젝트는 AI IDE cursor 의 도움을 받아 웹 서비스에 대한 지식이 전무한 사람이 어디까지 가능한가?를 알아보기 위해 시작되었습니다.

  2시간 30분 동안 메모 애플리케이션 웹 서비스를 만드는 데 성공했습니다.

  flask 라이브러리를 비롯해 html, css, javascript에 대한 지식이 전무한 사람도 cursor에게 질답하며 상당히 빠른 시간 내로 웹 서비스를 구현하는 것이 가능합니다. 
</p>

## Cursor란?
[cursor](https://www.cursor.com/)

### Bash에서 실행
```python
from app import db
  db.create_all()
```

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
