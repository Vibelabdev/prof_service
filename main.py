import uvicorn
from fastapi import FastAPI, UploadFile, File, Form, Query
from fastapi.middleware.cors import CORSMiddleware

from service_methods import check_profile, get_recommends


app = FastAPI(title='server')


origins = [
    "http://localhost:3000"  # для тестирования
]

#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "OPTIONS", 'DELETE', 'PUT', 'PATCH'],
#     allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
#                    "Authorization"],
# )



@app.get('/check_profile/')
def check_profile_endpoint(link: str = Query(..., alias="link")):
    try:
        class_percents = check_profile(link)  # получаем информацию о пользователе через ссылку на профиль

        return {'activity_percents': class_percents, 'success': True}

    except Exception as ex:
        print("EXCEPTION: ", ex)
        return {'success': False}


@app.post('/get_recommended_professions/')
def check_profile_endpoint(link: str = Query(..., alias="link"),
                           activity_level: str = Query(None, enum=["спокойный", "активный"]),
                           team: str = Query(None, enum=["командный", "одиночный", "командный/одиночный", "с животными"])):
    try:
        recommends = get_recommends(link, activity_level, team)
        return {'recommends': recommends, 'success': True}

    except Exception as ex:
        print("EXCEPTION: ", ex)
        return {'success': False}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=4000)
