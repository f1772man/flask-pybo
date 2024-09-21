from flask import Blueprint, render_template, jsonify, request
import csv
import re
import os

# Blueprint 객체 생성
cctv_bp = Blueprint('cctv', __name__)

# 현재 파일의 디렉토리 경로를 기반으로 CSV 파일 경로를 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 현재 파일의 절대 경로
CSV_PATH = os.path.join(BASE_DIR, './data/Sejong_CCTV_20240531.csv')  # CSV 파일 경로


# CSV 파일에서 CCTV 위치 데이터 읽어오기
def read_cctv_locations():
    cctv_locations = []
    with open(CSV_PATH, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            address_parts = extract_address_parts(row['소재지주소'])
            cctv_locations.append({
                "id": row['소재지주소'],
                "name": row['설치목적구분'],
                "latitude": float(row['위도']),
                "longitude": float(row['경도']),
                "agency": row['관리기관명'],
                "address": row['소재지주소'],
                "dong": address_parts['dong'],
                "gil": address_parts['gil'],
                "ro": address_parts['ro'],
                "ri": address_parts['ri'],
                "cameras": int(row['카메라대수'])  # 카메라대수 컬럼을 정수로 변환
            })
    return cctv_locations


# 주소에서 '동', '길', '로', '리' 등을 추출하는 함수
def extract_address_parts(address):
    parts = {'dong': None, 'gil': None, 'ro': None, 'ri': None}
    dong_match = re.search(r'([가-힣]+동)', address)
    gil_match = re.search(r'([가-힣]+길)', address)
    ro_match = re.search(r'([가-힣]+로)', address)
    ri_match = re.search(r'([가-힣]+리)', address)

    if dong_match:
        parts['dong'] = dong_match.group(1)
    if gil_match:
        parts['gil'] = gil_match.group(1)
    if ro_match:
        parts['ro'] = ro_match.group(1)
    if ri_match:
        parts['ri'] = ri_match.group(1)

    return parts


# CCTV 데이터를 동별로 분류
def get_dongs_and_locations():
    cctv_locations = read_cctv_locations()
    dongs = set([cctv['dong'] for cctv in cctv_locations])
    return list(dongs), cctv_locations


# 관리기관명과 지역별로 CCTV 데이터 필터링 및 수량 합산
@cctv_bp.route('/api/cctv_locations', methods=['GET'])
def get_cctv_locations():
    agency = request.args.get('agency')
    area = request.args.get('area')
    locations = read_cctv_locations()

    filtered_locations = []
    area_cameras = 0
    total_cameras = 0  # 관리기관 필터만 적용한 총 카메라 수
    for cctv in locations:
        # 관리기관 필터 적용
        if agency and agency != "" and cctv['agency'] != agency:
            continue

        # 관리기관에 대한 카메라 수량 추가
        total_cameras += cctv['cameras']

        # 동/길/로/리 필터 적용
        if area and area != "" and area not in (cctv['dong'], cctv['gil'], cctv['ro'], cctv['ri']):
            continue

        filtered_locations.append(cctv)
        area_cameras += cctv['cameras']

    # 콘솔에 total_cameras 값 출력
    print(f"Total cameras: {area_cameras}")
    print(f"Agency cameras: {total_cameras}")

    return jsonify({
        "locations": filtered_locations,
        "area_cameras": area_cameras,
        "total_cameras": total_cameras,  # 해당 관리기관의 전체 카메라 수
    })


# 관리기관명별로 CCTV 데이터 분류
def get_agency_data():
    cctv_locations = read_cctv_locations()
    agencies = {}
    for cctv in cctv_locations:
        if cctv['agency'] not in agencies:
            agencies[cctv['agency']] = []
        agencies[cctv['agency']].append(cctv)
    return agencies


@cctv_bp.route('/cctv')
def index():
    agencies = get_agency_data()  # 관리기관 목록을 반환
    dongs, _ = get_dongs_and_locations()  # 동 목록을 반환
    return render_template('/cctv/cctv_view.html', agencies=agencies, dongs=dongs)
