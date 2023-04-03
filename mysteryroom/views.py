from django.http import HttpResponse
import io
from rest_framework.parsers import JSONParser
from .models import MRUserAnswer, MysteryRoom, MysteryRoomCollection, MysteryRoomOption, MysteryRoomQuestion
import json
from app1.models import Event
import datetime


def service_check(request):
    return HttpResponse("Mystery Room Service up and running...", content_type="application/json", status=200)


def create_collection(request):
    if request.method != "POST":
        raise Exception(json.dumps(
            {"message": "wrong request method", "status": 400}))
    try:
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        print(python_data)
        collection = MysteryRoomCollection.objects.filter(
            title=python_data['title'])
        if len(collection) != 0:
            raise Exception(json.dumps(
                {"message": "mystery room collection with given name already exists", "status": 400}))
        print("creating collection")
        collection = MysteryRoomCollection(
            banner_image="collection___"+python_data['title'],
            title=python_data['title'],
            number_of_team_members=python_data['number_of_team_members'],
            number_of_mystery_rooms=python_data['number_of_mystery_rooms'],
            theme=python_data['theme'],
            created_on=python_data['created_on']
        )
        collection.save()
        print("collection created")
        return HttpResponse("created mystery room collection ", content_type='application/json')
    except Exception as err:
        return HttpResponse(err, content_type="application/json")


def edit_collection(request):
    if request.method != "POST":
        raise Exception(json.dumps(
            {"message": "wrong request method", "status": 400}))
    try:
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        print(python_data)
        collection = MysteryRoomCollection.objects.filter(
            id=python_data['collection_id'])
        if len(collection) == 0:
            raise Exception(json.dumps(
                {"message": "mystery room collection does not exist", "status": 400}))
        collection = collection[0]
        collection.banner_image = "collection___"+python_data['title']
        collection.title = python_data['title']
        # collection.number_of_team_members = python_data["number_of_team_members"]
        collection.theme = python_data['theme']
        collection.last_modified = python_data["last_modified"]
        collection.save()
        return HttpResponse("edited mystery room collection ", content_type='application/json')
    except Exception as err:
        return HttpResponse(err, content_type="application/json")


def delete_collection(request, collection_id):
    if request.method != "DELETE":
        raise Exception(json.dumps(
            {"message": "wrong request method", "status": 400}))
    try:
        collection = MysteryRoomCollection.objects.filter(id=collection_id)
        if len(collection) == 0:
            raise Exception(json.dumps(
                {"message": "mystery room collection does not exist", "status": 400}))
        collection = collection[0]
        event_id = collection.event_id
        collection.delete()
        if event_id != 0:
            ev = Event.objects.filter(id=event_id)
            if len(ev) == 0:
                raise Exception(json.dumps(
                    {"message": "event not found", "status": 400}))
            ev = ev[0]
            ev.task_id = 0
            ev.save()
        return HttpResponse("deleted mystery room collection ", content_type='application/json')
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")


def get_collection(request, collection_id):
    if request.method != "DELETE":
        raise Exception(json.dumps(
            {"message": "wrong request method", "status": 400}))
    try:
        collection = MysteryRoomCollection.objects.filter(id=collection_id)
        if len(collection) == 0:
            raise Exception(json.dumps(
                {"message": "mystery room collection does not exist", "status": 400}))
        collection = collection[0]

        result = {
            "collection_id": collection.pk,
            "event_id": collection.event_id,
            "event_name": "Mystery Room Collection not published" if collection.event_id == 0 else Event.objects.get(id=collection.event_id).name,
            "event_date": "Mystery Room Collection not published" if collection.event_id == 0 else Event.objects.get(id=collection.event_id).start_date,
            "title": collection.title,
            "banner_image": collection.banner_image,
            "number_of_team_members": collection.number_of_team_members,
            "number_of_mystery_rooms": collection.number_of_mystery_rooms,
            "theme": collection.theme,
            "created_on": collection.created_on,
            "last_modified": collection.last_modified

        }
        json_post = json.dumps(result)
        return HttpResponse(json_post, content_type="application/json")
    except Exception as err:
        return HttpResponse(err, content_type="application/json")


def get_all_collections(request):
    if request.method != "GET":
        raise Exception(json.dumps(
            {"message": "wrong request method", "status": 400}))
    try:
        result = []
        collections = MysteryRoomCollection.objects.all()
        for collection in collections:
            result.append({
                "collection_id": collection.pk,
                "event_id": collection.event_id,
                "event_name": "Mystery Room Collection not published" if collection.event_id == 0 else Event.objects.get(id=collection.event_id).name,
                "event_date": "Mystery Room Collection not published" if collection.event_id == 0 else Event.objects.get(id=collection.event_id).start_date,
                "title": collection.title,
                "banner_image": collection.banner_image,
                "number_of_team_members": collection.number_of_team_members,
                "number_of_mystery_rooms": collection.number_of_mystery_rooms,
                "theme": collection.theme,
                "created_on": collection.created_on,
                "last_modified": collection.last_modified

            })
        active = []
        elapsed = []
        for i, item in enumerate(result):
            curr = datetime.date.today()
            curt = datetime.datetime.now().time()
            print(item)
            if item['event_id'] != 0:
                event = Event.objects.get(name=item['event_name'])
                if event.end_date < curr:
                    elapsed.append(result[i])
                elif event.end_time < curt and event.end_date == curr:
                    elapsed.append(result[i])
                else:
                    active.append(result[i])
            else:
                active.append(result[i])

        json_post = json.dumps({"active": active, "elapsed": elapsed})
        return HttpResponse(json_post, content_type="application/json")
    except Exception as err:
        return HttpResponse(err, content_type="application/json")


def publish_collection(request):
    if request.method != 'POST':
        raise Exception(json.dumps(
            {"message": "wrong request method", "status": 400}))

    try:
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        print(python_data)

        event = Event.objects.filter(id=python_data['event_id'])
        if len(event) == 0:
            raise Exception(json.dumps(
                {"message": "event not exists", "status": 400}))
        event = event[0]
        print(event)

        collection = MysteryRoomCollection.objects.filter(
            id=python_data['collection_id'])
        if len(collection) == 0:
            raise Exception(json.dumps(
                {"message": "Mystery Room collection does not exist", "status": 400}))
        collection = collection[0]

        if collection.event_id != 0:
            raise Exception(json.dumps(
                {"message": "collection already published", "status": 400}))

        event.task_id = collection.pk
        event.save()

        collection.event_id = event.pk
        collection.save()

        return HttpResponse(json.dumps({"message": f"collection {collection} published for the event {event}", "status": 200}), content_type="application/json")
    except Exception as err:
        return HttpResponse(err, content_type="application/json")


def create_room(request):
    if request.method != "POST":
        raise Exception(json.dumps(
            {"message": "wrong request method", "status": 400}))
    try:
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        print(python_data)
        room = MysteryRoom.objects.filter(title=python_data['title'])
        if len(room) != 0:
            raise Exception(json.dumps(
                {"message": "mystery room with given name already exists", "status": 400}))
        print("creating room")
        room = MysteryRoom(
            mystery_room=MysteryRoomCollection.objects.get(
                id=python_data['collection_id']),
            banner_image="room___"+python_data['title'],
            title=python_data['title'],
            difficulty_level=python_data['difficulty_level'],
            number_of_questions=python_data['number_of_questions'],
            description=python_data['description'],
            created_on=python_data['created_on']
        )
        room.save()
        print("saving room")
        return HttpResponse("created mystery room", content_type='application/json')
    except Exception as err:
        return HttpResponse(err, content_type="application/json")


def edit_room(request):
    if request.method != "POST":
        raise Exception(json.dumps(
            {"message": "wrong request method", "status": 400}))
    try:
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        print(python_data)
        room = MysteryRoom.objects.filter(id=python_data['room_id'])
        if len(room) == 0:
            raise Exception(json.dumps(
                {"message": "mystery room with given name not found", "status": 400}))
        room = room[0]
        room.banner_image = "room___"+python_data['title']
        room.title = python_data['title']
        room.difficulty_level = python_data['difficulty_level']
        room.description = python_data['description']
        room.last_modified = python_data['last_modified']
        room.save()
        print("saving room")
        return HttpResponse("edited mystery room", content_type='application/json')
    except Exception as err:
        return HttpResponse(err, content_type="application/json")


def delete_room(request, room_id):
    if request.method != "DELETE":
        raise Exception(json.dumps(
            {"message": "wrong request method", "status": 400}))
    try:
        room = MysteryRoom.objects.filter(id=room_id)
        if len(room) == 0:
            raise Exception(json.dumps(
                {"message": "mystery room with given name not found", "status": 400}))
        room.delete()
        return HttpResponse("deleted mystery room", content_type='application/json')
    except Exception as err:
        return HttpResponse(err, content_type="application/json")


def get_all_rooms(request, collection_id):
    if request.method != "GET":
        raise Exception(json.dumps(
            {"message": "wrong request method", "status": 400}))
    try:
        collection = MysteryRoomCollection.objects.filter(id=collection_id)
        if len(collection) == 0:
            raise Exception(json.dumps(
                {"message": "mystery room collection not found", "status": 400}))
        collection = collection[0]
        rooms = MysteryRoom.objects.filter(mystery_room=collection)
        result = []
        for room in rooms:
            result.append({
                "room_id": room.pk,
                "banner_image": room.banner_image,
                "title": room.title,
                "difficulty_level": room.difficulty_level,
                "number_of_questions": room.number_of_questions,
                "description": room.description,
                "created_on": room.created_on,
                "last_modified": room.last_modified
            })
        json_post = json.dumps(result)
        return HttpResponse(json_post, content_type="application/json")
    except Exception as err:
        return HttpResponse(err, content_type="application/json")


def get_room(request, room_id):
    if request.method != "GET":
        raise Exception(json.dumps(
            {"message": "wrong request method", "status": 400}))
    try:
        room = MysteryRoom.objects.filter(id=room_id)
        if len(room) == 0:
            raise Exception(json.dumps(
                {"message": "mystery room  not found", "status": 400}))
        room = room[0]
        result = {
            "room_id": room.pk,
            "banner_image": room.banner_image,
            "title": room.title,
            "difficulty_level": room.difficulty_level,
            "number_of_questions": room.number_of_questions,
            "description": room.description,
            "created_on": room.created_on,
            "last_modified": room.last_modified
        }
        json_post = json.dumps(result)
        return HttpResponse(json_post, content_type="application/json")
    except Exception as err:
        return HttpResponse(err, content_type="application/json")
