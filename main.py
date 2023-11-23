import requests
# В этом задании мы будем выгружать из API персонажей Start Wars и загружать в базу данных.
def get_person(person_id):
    return requests.get(f'https://swapi.dev/api/people//{person_id}/').json() #получаем инфо
# https://swapi.dev/api/people/1/

def main():
    person_1 = get_person(1) #отправили запрос получили ответ и тд.
    person_2 = get_person(2)
    person_3 = get_person(3)
    person_4 = get_person(4)

    print(person_1, person_2, person_3, person_4)

if __name__ == '__main__':
    main()