# bluecoconut_website



## **⦁ 설명 영상 (9분)**

    - 


## **⦁ PDF 보고서 (p24)**

    - https://github.com/shindong96/bluecoconut_data_web/blob/main/bluecoconut_website%20%EB%B3%B4%EA%B3%A0%EC%84%9C.pdf

## **⦁ 개요**

    -자체 해양 관측 기기를 개발 중인 스타트업 블루코코넛의 실시간 해양 데이터 제공을 위한 웹사이트 제작 (4개월) (2021.3 ~ 2021.6)

    -총 3명이 진행한 프로젝트

    -**공동 업무**: 서비스 기획, UI/UX 설계, 데이터베이스 설계

    -**분담 업무**: 해양 데이터 지도 형태/테이블 형태/시각화로 분업 개발

    -**맡은 역할**: 
    - 구글 맵 API 사용한 지도 형태 해양 데이터 제공 서비스 개발(map/templates/map.html, static/js/map/map.js) 
    - AWS EC2, RDS 베포 및 연동, AWS 람다 함수를 통한 AWS S3와 RDS 연동


## **⦁ 구현 영상 (1분30초)**

    - https://www.youtube.com/watch?v=9VHgKp-l6G0

    - GIF (1분)

    ![bluecoconut_website 시연 영상](https://user-images.githubusercontent.com/58173061/125639419-38925724-a2d9-4d8c-8685-d5a702bb9f05.gif)



## **⦁ 기술 스택**

    -**웹 프론트**: html, css, javascript를 통해 개발했으며 공개 탬플릿을 사용하여 웹 사이트 틀을 구성했습니다.

    -**웹 백엔드**: 데이터 시각화에 적합한 언어는 python이라고 판단해 python 프레임워크인 django 프레임워크로 개발했으며, django ORM을 통해 DB와 연동했습니다. MVT 디자인 패턴을 사용했고 지도/테이블로 모듈화하여 분업 개발하였습니다.

    -**데이터베이스**: 해당 기능에 적합한 데이터만 불러오기 위해 SQL 언어를 선택하였으며 그 중 팀원 모두 경험이 있는 MYSQL로 DB를 개발하였습니다.

    -**클라우드**: 개발 중인 해양 관측기기와 위성 통신을 위해 AWS 위성 통신 서비스(SES)가 필요하여 클라우드는 AWS로 선정하였고, 프로젝트는 AWS EC2, DB는 AWS RDS에 각각 베포 및 연동하였습니다. 추후 위성 통신을 통한 해양 데이터가 S3에 업로드 되면 자동으로 개발한 알고리즘에 따라 RDS에 INSERT/UPDATE 되도록 람다 함수를 구현하여 연동하였습니다. 

    -**협업 툴**: gitlab과 souretree로 분업 개발과 지속적인 통합하며 협업하였습니다.


## **⦁ 블루코코넛 소개**

    - http://oceanbluecoconut.com/
