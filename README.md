# Description

## 프로젝트 개요
이미지와 식품 영양 정보 DB를 구축하고 이미지 데이터를 학습한 머신러닝 API와 DB를 웹에 연결하여 사진이나 키워드로 영양정보를 손쉽게 검색하는 웹서비스 ‘알고먹조’ 개발

## 프로젝트 기간
2021.05.31~2021.6.4

## 프로젝트 팀 인원 : 총 5명
### 팀내 역할
- 역할 1 프로젝트 전체 관리 및 최종 발표

- 역할 2 데이터 실시간 플랫폼 구성(Spark, Kafka, MariaDB)
  - Python에서 제품 이미지 데이터를 스크레이핑하여 Kafka를 통해 Spark로 전송, Spark에서 structured streaming을 사용하여 데이터 전처리 후 MariaDB에 적재

  - MariaDB에 적재한 데이터를 Python에서 Azure Custom Vision AP

- 역할 3 웹개발(서버, 클라이언트)

  - 웹에 식품 사진을 업로드하면 Azure Custom Vision API를 사용하여 해당 사진 분석 후 예측된 식품명을 기반으로 MariaDB에 적재된 식품 영양 정보를 불러오는 서비스 개발
  
  - 제품명, 제조사 등 키워드로 식품을 검색하는 기능 개발, 영양 성분 범위를 지정하여 식품을 검색하는 기능 개발, 검색된 식품 명을 클릭하면 상세페이지로 이동하여 MariaDB에 적재된 식품 영양 정보 확인 가능


<br>

# Environment

|분류|이름|버전|
|:---|:---|:---|
|운영체제|CentOS|7|
|개발언어|Java|1.8|
||Python|3.9.5|
||Scala|2.12|
|DB|MriaDB|10.5|
|파이프라인|Kafka|0.10|
||Zookeeper|3.7.0|
||Spark|3.1.1|
||Hadoop|3.2|
||Logstash|7.12.0|
||Elasticsearch|7.12.0|
||Grafana|7.1.0|
|ML|Custom Vision|3.3|
|Web|Flask|2.0.1|

<br>

# Directories

|디렉토리명|소개|
|:---|:---|
|Web|Flask 기반 웹 개발 코드|
|Custom_vision.ipynb|커스텀 비전 학습 코드|
|scraping.ipynb|이미지 스크레이핑 코드|
|StreamingSpark.scala|Spark shell에서 사용한 spark streaming용 scala 코드|