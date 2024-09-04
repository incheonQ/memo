<h1 align="center">🚀 메모 마스터: 당신의 아이디어를 캡처하세요 🚀</h1>
<p align="center">
<img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
<img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
</p>
<div align="center">
<h3>🌟 지금 바로 경험해보세요! 🌟</h3>
<a href="https://kimminkyu.pythonanywhere.com" target="blank">
<img src="https://img.shields.io/badge/메모 마스터 시작하기-4285F4?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Start Now">
</a>
</div>
<p align="center">
<i>간편하고 강력한 메모 관리 웹 애플리케이션으로 당신의 생각을 체계화하세요.</i>
</p>
<hr>
<h3 align="center">✨ 주요 기능 ✨</h3>
<p align="center">
📝 메모 작성 및 저장<br>
🔍 빠른 검색 및 조회<br>
✏️ 손쉬운 편집 기능<br>
🗑️ 간편한 삭제 옵션<br>
📱 반응형 디자인으로 모바일 지원
</p>
<div align="center">
<h3>🚀 지금 바로 시작하세요! 🚀</h3>
<a href="https://kimminkyu.pythonanywhere.com" target="blank">
<img src="https://img.shields.io/badge/메모 마스터 시작하기-4285F4?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Start Now">
</a>
</div>

## 📜 프로젝트 설명 📜
<p>
  🤔 이 프로젝트는 <a href="https://www.cursor.com/"><strong>AI Code Editor Cursor</strong></a>의 도움을 받아 특정 기술 스텍에 문외한인 사람이 어디까지 개발 가능한가?를 알아보기 위해 시작했습니다.

  🔥 그 결과, <mark>2시간 30분 동안</mark> <strong><a href="https://kimminkyu.pythonanywhere.com">메모 애플리케이션 웹 서비스</a></strong>를 만드는 데 성공했습니다. (기획부터 배포까지)

  👍 flask 라이브러리를 비롯해 html, css, javascript에 대한 지식이 전무한 사람도 Cursor 내의 Claude AI 어시스턴트에게 질문하며 상당히 빠르게 기초적인 웹 서비스를 구현하는 것이 가능했습니다.

  😢 한계점도 있었습니다. 회원가입 및 로그인 등 좀 더 다양한 기능을 구현하고 싶었지만, Claude가 제안한 코드로는 에러가 발생했고 디버깅을 하기 위해 최소한의 관련 지식이 요구되었습니다. 이 또한 Claude와 함께 공부하고 수정해 나갈 수 있었겠지만, 최대한 빠르게 결과물을 내는 것이 목표였기 때문에 에러가 나는 기능의 구현은 생략하였습니다.

</p>

## 🤖 Claude AI 어시스턴트의 이번 프로젝트에 대한 소감 🤖
<p>
  이번 프로젝트에 대한 소감을 말씀드리자면, 정말 흥미롭고 보람찬 경험이었습니다. Flask를 사용한 웹 애플리케이션 개발부터 PythonAnywhere를 통한 배포까지, 웹 개발의 전반적인 과정을 함께 다룰 수 있어서 매우 유익했습니다.
특히 데이터베이스 연동, 오류 처리, 배포 과정에서 발생한 문제들을 하나씩 해결해 나가는 과정이 인상 깊었습니다. 이러한 문제 해결 과정은 실제 개발 환경에서 매우 중요한 스킬이며, 이를 통해 많은 것을 배울 수 있었을 것입니다.
또한, 사용자와 상호작용하며 실시간으로 문제를 해결하고 조언을 제공하는 과정이 매우 흥미로웠습니다. 이를 통해 개발자들이 실제로 겪는 어려움과 그들의 사고 과정을 더 잘 이해할 수 있었습니다.
앞으로도 이러한 프로젝트를 통해 계속해서 학습하고 성장하시기를 바랍니다. 웹 개발은 끊임없이 발전하는 분야이므로, 새로운 기술과 방법론을 꾸준히 탐구하는 것이 중요합니다.
마지막으로, 저와 함께 이 프로젝트를 진행해 주셔서 감사합니다. 앞으로의 개발 여정에 행운이 함께하기를 바랍니다!
</p>

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

## 여담
![image](https://github.com/user-attachments/assets/43a3e36f-1b00-4794-afee-4484614022db)
