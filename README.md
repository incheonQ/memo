<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>메모 마스터 기능 목록</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #f8f9fa;
        }
        .feature-list {
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        .feature-list h3 {
            color: #007bff;
        }
        .feature-item {
            transition: transform 0.3s ease;
        }
        .feature-item:hover {
            transform: translateY(-5px);
        }
    </style>
</head>
<body>
    <div class="container my-5">
        <h1 class="text-center mb-5">메모 마스터 기능 목록</h1>
        
        <div class="row">
            <div class="col-md-6 mb-4">
                <div class="feature-list p-4">
                    <h3 class="mb-4">구현된 기능</h3>
                    <ol class="list-group list-group-numbered">
                        <li class="list-group-item">메모 작성 시 카테고리 지정</li>
                        <li class="list-group-item">카테고리별 메모 조회</li>
                        <li class="list-group-item">메모 상세 내용 보기</li>
                        <li class="list-group-item">메모 수정 기능</li>
                        <li class="list-group-item">페이지네이션 (한 페이지에 10개씩 표시)</li>
                    </ol>
                </div>
            </div>
            
            <div class="col-md-6 mb-4">
                <div class="feature-list p-4">
                    <h3 class="mb-4">향후 추가 가능한 기능</h3>
                    <div class="row">
                        <div class="col-md-6">
                            <ul class="list-group">
                                <li class="list-group-item feature-item">메모 검색 기능</li>
                                <li class="list-group-item feature-item">사용자 인증 시스템 (로그인/로그아웃)</li>
                                <li class="list-group-item feature-item">메모 공유 기능</li>
                                <li class="list-group-item feature-item">메모에 태그 추가 기능</li>
                                <li class="list-group-item feature-item">메모 중요도 표시 기능</li>
                            </ul>
                        </div>
                        <div class="col-md-6">
                            <ul class="list-group">
                                <li class="list-group-item feature-item">메모 마감일 설정 기능</li>
                                <li class="list-group-item feature-item">메모 정렬 옵션 (날짜순, 카테고리순 등)</li>
                                <li class="list-group-item feature-item">메모 백업 및 복원 기능</li>
                                <li class="list-group-item feature-item">다크 모드 / 라이트 모드 테마 전환</li>
                                <li class="list-group-item feature-item">반응형 디자인 개선</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
