import os
import cv2

import db
import settings
from logger import get_logger
from utils import rotate_image


def test_grouping_result():
    conn = db.get_connection()
    try:
        sql = ("select id, name from tbl_person where id != -1")
        with conn.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
            persons = [{"id": row[0], "name": row[1]} for row in rows]

            for person in persons:
                test_photos_in_person(cursor, person['id'])
                conn.commit()
    finally:
        db.put_connection(conn)


def test_photos_in_person(cursor, personId):
    sql = ("select photo.id, photo.path"
           " from tbl_photo photo"
           " inner join tbl_face face on photo.id = face.photo_id"
           " where face.person_id = %s"
           " group by photo.id")
    cursor.execute(sql, (personId, ))
    rows = cursor.fetchall()
    photos = [{"id": row[0], "path": row[1]} for row in rows]
    if len(photos) == 0:
        return

    # 得到照片的来源人物
    for photo in photos:
        path = photo['path']
        photo['fileName'] = path.split('\\')[-1]
        photo['personName'] = path.split('\\')[-2]

    # 统计每个人物的照片数量
    personCountDict = {}
    for photo in photos:
        personName = photo['personName']
        if personName in personCountDict:
            personCountDict[personName] += 1
        else:
            personCountDict[personName] = 1

    # 照片最多的人物
    maxCount = 0
    currentPersonName = None
    for personName, count in personCountDict.items():
        if count > maxCount:
            maxCount = count
            currentPersonName = personName

    realCount = real_photo_count[currentPersonName]
    # print(
    #     f"current person: {currentPersonName}, total photo count: {realCount}, found photo count: {maxCount}"
    # )
    # peronId,当前人物，真正的照片数量，检出的照片总数，检出的正确照片数
    print(f"{personId} {currentPersonName} {realCount} {len(photos)} {maxCount}")


real_photo_count = {
    "Adam_Sandler": 81,
    "Alan_Rickman": 109,
    "Alice_Krige": 37,
    "Alyssa_Milano": 105,
    "Amanda_Bearse": 22,
    "Arnold_Schwarzenegger": 44,
    "Benicio_Del_Toro": 95,
    "Bernard_Hill": 43,
    "Bernie_Mac": 56,
    "Bobbie_Eakes": 74,
    "Bradley_Cooper": 109,
    "Brianna_Brown": 63,
    "Carla_Gallo": 60,
    "Charlie_Sheen": 108,
    "Chris_Kattan": 87,
    "Chris_Klein": 81,
    "Daniel_Craig": 98,
    "Danny_Masterson": 96,
    "Dan_Lauria": 88,
    "David_Duchovny": 86,
    "Dean_Cain": 102,
    "Debra_Messing": 132,
    "Denzel_Washington": 74,
    "Dina_Meyer": 77,
    "Ed_Harris": 58,
    "Eileen_Davidson": 84,
    "Ethan_Hawke": 118,
    "Ewan_McGregor": 104,
    "Gillian_Anderson": 106,
    "Glenn_Close": 123,
    "Hugh_Grant": 114,
    "Ilene_Kristen": 46,
    "Jackie_Chan": 82,
    "James_Brolin": 62,
    "James_Marsden": 108,
    "Jane_Curtin": 43,
    "Jane_Krakowski": 91,
    "Jane_Leeves": 83,
    "Jared_Padalecki": 100,
    "Jason_Bateman": 116,
    "Jason_Behr": 83,
    "Jennette_McCurdy": 105,
    "Jensen_Ackles": 69,
    "Jeremy_Irons": 110,
    "Jessica_Capshaw": 118,
    "Jet_Li": 79,
    "Jill_Eikenberry": 27,
    "Jill_Hennessy": 67,
    "Jimmy_Fallon": 77,
    "Johnny_Depp": 111,
    "John_Cusack": 97,
    "John_Travolta": 89,
    "Joshua_Jackson": 112,
    "Jude_Law": 111,
    "Julie_Benz": 130,
    "Justine_Bateman": 83,
    "Kate_Linder": 74,
    "Kathy_Baker": 45,
    "Kathy_Griffin": 68,
    "Kellan_Lutz": 94,
    "Ken_Watanabe": 57,
    "Kristen_Johnston": 90,
    "Kristy_McNichol": 44,
    "Laurie_Metcalf": 80,
    "Linda_Evans": 84,
    "Lorraine_Bracco": 99,
    "Mackenzie_Aladjem": 53,
    "Margaret_Cho": 80,
    "Mark_Ruffalo": 105,
    "Mary_Crosby": 47,
    "Melissa_Benoist": 95,
    "Melissa_Claire_Egan": 76,
    "Melissa_Gilbert": 61,
    "Michael_Douglas": 119,
    "Mila_Kunis": 75,
    "Morena_Baccarin": 91,
    "Nicole_Eggert": 76,
    "Oliver_Platt": 76,
    "Omid_Djalili": 70,
    "Pamela_Sue_Martin": 71,
    "Patricia_Kalember": 36,
    "Peggy_McCay": 40,
    "Peter_Sarsgaard": 105,
    "Philip_Seymour_Hoffman": 65,
    "Pierce_Brosnan": 108,
    "Portia_Doubleday": 63,
    "Rebecca_Budig": 84,
    "Richard_E._Grant": 68,
    "Roma_Downey": 108,
    "Russell_Crowe": 101,
    "Ryan_Phillippe": 91,
    "Ryan_Reynolds": 93,
    "Sally_Field": 85,
    "Scott_Patterson": 62,
    "Sharon_Case": 77,
    "Simon_Pegg": 119,
    "Susan_Dey": 57,
    "Tamara_Braun": 68,
    "Tatyana_M._Ali": 65,
    "Yasmine_Bleeth": 71,
}

if __name__ == "__main__":
    test_grouping_result()
