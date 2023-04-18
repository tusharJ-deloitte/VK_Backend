from django.http import HttpResponse
import io
from rest_framework.parsers import JSONParser
from .models import MRUserAnswer, MysteryRoom, MysteryRoomCollection, MysteryRoomOption, MysteryRoomQuestion, Timer
import json
from app1.models import Event, Team, Player, Activity, Registration
import datetime
from GrapheneTest.settings import CLOUDFRONT_DOMAIN as imgBaseUrl
from GrapheneTest.settings import AWS_STORAGE_BUCKET_NAME
from django.contrib.auth.models import User
import boto3
import pytz


def service_check(request):
    return HttpResponse("Mystery Room Service up and running...", content_type="application/json", status=200)

def invalidate_cloudfront_cache(object_key):
    distribution_id = "E1W1M825N8JK1G"
    cf_client = boto3.client('cloudfront')
    print("client")
    paths = {
        'Quantity': 1,
        'Items': ['/'+object_key]
    }
    print("paths")
    cf_client.create_invalidation(
        DistributionId=distribution_id,
        InvalidationBatch={
            'Paths': paths,
            'CallerReference': 'my-invalidation'
        }
    )
    print("done")


def create_collection(request):
    if request.method != "POST":
        return HttpResponse(json.dumps({"message": "wrong request method", "status": 400}), content_type="appication/json", status=400)
    try:
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        print(python_data)
        collection = MysteryRoomCollection.objects.filter(
            title=python_data['title'])
        if len(collection) != 0:
            raise Exception(json.dumps(
                {"message": "mystery room collection does not exist", "status": 400}))
        print("creating collection")
        collection = MysteryRoomCollection(
            title=python_data['title'],    
            number_of_mystery_rooms=python_data['number_of_mystery_rooms'],
            theme=python_data['theme'],
            created_on=python_data['created_on'],
            last_modified = python_data['created_on']
        )
        collection.save()
        if python_data["is_image"]:
            collection.banner_image = "collection___"+str(collection.pk)
            collection.save()
        print("collection created")
        result={
            "id":collection.pk
        }
        return HttpResponse(json.dumps(result), content_type='application/json')
    except Exception as err:
        return HttpResponse(err, content_type="application/json")


def edit_collection(request):
    if request.method != "PUT":
        return HttpResponse(json.dumps({"message": "wrong request method", "status": 400}), content_type="appication/json", status=400)
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
        print("inside edit collection")
        if collection.banner_image:
            print("inside banner image")
            key = "virtualkunakidza/"+collection.banner_image+".png"
            print(key)
            invalidate_cloudfront_cache(key)
            s3_client = boto3.client('s3')
            print("---",s3_client)
            response = s3_client.delete_object(
                    Bucket=AWS_STORAGE_BUCKET_NAME, Key=key)
            print("###",response)
        collection.title = python_data['title']
        collection.theme = python_data['theme']
        collection.last_modified = python_data["last_modified"]
        if python_data["is_image"]:
            collection.banner_image = "collection___"+str(collection.pk)
        collection.save()
        result={
            "id":collection.pk
        }
        return HttpResponse(json.dumps(result), content_type='application/json')
    except Exception as err:
        return HttpResponse(err, content_type="application/json")


def delete_collection(request, collection_id):
    if request.method != "DELETE":
        return HttpResponse(json.dumps({"message": "wrong request method", "status": 400}), content_type="appication/json", status=400)
    try:
        collection = MysteryRoomCollection.objects.filter(id=collection_id)
        if len(collection) == 0:
            raise Exception(json.dumps(
                {"message": "mystery room collection does not exist", "status": 400}))
        collection = collection[0]
        if collection.banner_image:
            key = collection.banner_image+".png"
            s3_client = boto3.client('s3')
            response = s3_client.delete_object(
                    Bucket=AWS_STORAGE_BUCKET_NAME, Key=key)
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
    if request.method != "GET":
        return HttpResponse(json.dumps({"message": "wrong request method", "status": 400}), content_type="appication/json", status=400)
    try:
        collection = MysteryRoomCollection.objects.filter(id=collection_id)
        if len(collection) == 0:
            raise Exception(json.dumps(
                {"message": "mystery room collection does not exist", "status": 400}))
        collection = collection[0]

        room = MysteryRoom.objects.filter(mystery_room = collection)
        flag=0
        if len(room)!=collection.number_of_mystery_rooms:
            flag=1
        for r in room:
            questions = MysteryRoomQuestion.objects.filter(room=r, mystery_room_collection=collection)
            if r.number_of_questions-len(questions) != 0:
                flag=1
        
        result = {
            "collection_id": collection.pk,
            "event_id": collection.event_id,
            "event_name": "Not published yet" if collection.event_id == 0 else Event.objects.get(id=collection.event_id).name,
            "event_date": "Not published yet" if collection.event_id == 0 else str(Event.objects.get(id=collection.event_id).start_date),
            "title": collection.title,
            "banner_image": imgBaseUrl+collection.banner_image+".png" if collection.banner_image else "",
            "number_of_mystery_rooms": collection.number_of_mystery_rooms,
            "theme": collection.theme,
            "created_on": collection.created_on,
            "updated_on":collection.last_modified.split('=')[0],
            "updated_time":collection.last_modified.split('=')[1],
            "last_modified": collection.last_modified,
            "status":"Complete" if flag==0 else "Incomplete"

        }
        json_post = json.dumps(result)
        return HttpResponse(json_post, content_type="application/json")
    except Exception as err:
        return HttpResponse(err, content_type="application/json")


def get_all_collections(request):
    if request.method != "GET":
        return HttpResponse(json.dumps({"message": "wrong request method", "status": 400}), content_type="appication/json", status=400)
    try:
        result = []
        collections = MysteryRoomCollection.objects.all()

        for collection in collections:
            room = MysteryRoom.objects.filter(mystery_room = collection)
            flag=0
            if len(room)!=collection.number_of_mystery_rooms:
                flag=1
            for r in room:
                questions = MysteryRoomQuestion.objects.filter(room=r, mystery_room_collection=collection)
                if r.number_of_questions-len(questions) != 0:
                    flag=1
            result.append({
                "collection_id": collection.pk,
                "event_id": collection.event_id,
                "event_name": "Not published yet" if collection.event_id == 0 else Event.objects.get(id=collection.event_id).name,
                "event_date": "Not published yet" if collection.event_id == 0 else str(Event.objects.get(id=collection.event_id).start_date),
                "title": collection.title,
                "banner_image": imgBaseUrl+collection.banner_image+".png" if collection.banner_image else "",
                "number_of_mystery_rooms": collection.number_of_mystery_rooms,
                "theme": collection.theme,
                "created_on": collection.created_on,
                "updated_on":collection.last_modified.split('=')[0],
                "updated_time":collection.last_modified.split('=')[1],
                "last_modified": collection.last_modified,
                "status":"Complete" if flag==0 else "Incomplete"

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
        return HttpResponse(json.dumps({"message": "wrong request method", "status": 400}), content_type="appication/json", status=400)

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
        return HttpResponse(json.dumps({"message": "wrong request method", "status": 400}), content_type="appication/json", status=400)
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
            room_number=python_data['room_number'],
            title=python_data['title'],
            difficulty_level=python_data['difficulty_level'],
            number_of_questions=python_data['number_of_questions'],
            description=python_data['description'],
            created_on=python_data['created_on'],
            last_modified = python_data['created_on']
        )
        if python_data['room_number'] == 1:
            room.is_locked = False
        room.save()
        if python_data['is_image']:
            room.banner_image = "room___"+str(room.pk)
            room.save()
        result={
            "id":room.pk
        }
        print("saving room")
        return HttpResponse(json.dumps(result), content_type='application/json')
    except Exception as err:
        return HttpResponse(err, content_type="application/json")


def edit_room(request):
    if request.method != "PUT":
        return HttpResponse(json.dumps({"message": "wrong request method", "status": 400}), content_type="appication/json", status=400)
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
        if room.banner_image:
            key = room.banner_image+".png"
            s3_client = boto3.client('s3')
            response = s3_client.delete_object(
                    Bucket=AWS_STORAGE_BUCKET_NAME, Key=key)
        room.room_number = python_data['room_number']
        room.title = python_data['title']
        room.difficulty_level = python_data['difficulty_level']
        room.description = python_data['description']
        room.last_modified = python_data['last_modified']
        if python_data['is_image']:
            room.banner_image = "room___"+str(room.pk)
        room.save()
        print("saving room")
        result={
            "id":room.pk
        }
        return HttpResponse(json.dumps(result), content_type='application/json')
    except Exception as err:
        return HttpResponse(err, content_type="application/json")


def delete_room(request, room_id):
    if request.method != "DELETE":
        return HttpResponse(json.dumps({"message": "wrong request method", "status": 400}), content_type="appication/json", status=400)
    try:
        room = MysteryRoom.objects.filter(id=room_id)
        if len(room) == 0:
            raise Exception(json.dumps(
                {"message": "mystery room with given name not found", "status": 400}))
        room=room[0]
        if room.banner_image:
            key =room.banner_image+".png"
            s3_client = boto3.client('s3')
            response = s3_client.delete_object(
                Bucket=AWS_STORAGE_BUCKET_NAME, Key=key)
        room.delete()
        return HttpResponse("deleted mystery room", content_type='application/json')
    except Exception as err:
        return HttpResponse(err, content_type="application/json")


def get_all_rooms(request, collection_id):
    if request.method != "GET":
        return HttpResponse(json.dumps({"message": "wrong request method", "status": 400}), content_type="appication/json", status=400)
    try:
        collection = MysteryRoomCollection.objects.filter(id=collection_id)
        if len(collection) == 0:
            raise Exception(json.dumps(
                {"message": "mystery room collection not found", "status": 400}))
        collection = collection[0]
        rooms = MysteryRoom.objects.filter(mystery_room=collection).order_by('room_number')
        result = []
        print(rooms)
        r=[]
        for room in rooms:
            questions = MysteryRoomQuestion.objects.filter(
                room=room, mystery_room_collection=collection)
            print(questions)
            r.append({
                "room_id": room.pk,
                "room_number": room.room_number,
                "is_locked": room.is_locked,
                "banner_image": imgBaseUrl+room.banner_image+".png" if room.banner_image else "",
                "title": room.title,
                "difficulty_level": room.difficulty_level,
                "number_of_questions": room.number_of_questions,
                "number_of_questions_left": room.number_of_questions-len(questions),
                "description": room.description,
                "created_on": room.created_on,
                "updated_on":room.last_modified.split('=')[0],
                "updated_time":room.last_modified.split('=')[1],
                "last_modified": room.last_modified
            })
        result.append({
            "collection_id":collection_id,
            "collection_name":collection.title,
            "completed_rooms":len(r),
            "incompleted_rooms":collection.number_of_mystery_rooms-len(r),
            "number_of_mystery_rooms":collection.number_of_mystery_rooms,
            "rooms":r,
        })
        json_post = json.dumps(result)
        return HttpResponse(json_post, content_type="application/json")
    except Exception as err:
        return HttpResponse(err, content_type="application/json")


def get_room(request, collection_id, room_id):
    if request.method != "GET":
        return HttpResponse(json.dumps({"message": "wrong request method", "status": 400}), content_type="appication/json", status=400)
    try:
        room = MysteryRoom.objects.filter(id=room_id)
        if len(room) == 0:
            raise Exception(json.dumps(
                {"message": "mystery room  not found", "status": 400}))
        room = room[0]
        collection = MysteryRoomCollection.objects.filter(id=collection_id)
        if len(collection) == 0:
            raise Exception(json.dumps(
                {"message": "mystery room collection not found", "status": 400}))
        collection = collection[0]
        ques_info = []
        questions = MysteryRoomQuestion.objects.filter(
            room=room, mystery_room_collection=collection).order_by('question_number')
        for question in questions:
            all_options_for_question = MysteryRoomOption.objects.filter(
                room=room, question=question)
            options = []
            for option in all_options_for_question:
                options.append({
                    "option_text": option.option_text,
                    "is_correct": option.is_correct
                })
            ques_info.append({
                "question_id": question.pk,
                "question_text": question.question_text,
                "question_image": imgBaseUrl+question.question_image+".png" if question.question_image else "",
                "note": question.note,
                "hint_text": question.hint_text,
                "hint_image": imgBaseUrl+question.hint_image+".png" if question.hint_image else "",
                "question_type": question.question_type,
                "question_number": question.question_number,
                "options": options,
            })
        result = {
            "room_id": room.pk,
            "room_number": room.room_number,
            "is_locked": room.is_locked,
            "banner_image": imgBaseUrl+room.banner_image+".png" if room.banner_image else "",
            "questions": ques_info,
            "title": room.title,
            "difficulty_level": room.difficulty_level,
            "number_of_questions": room.number_of_questions,
            "number_of_questions_left": room.number_of_questions-len(ques_info),
            "description": room.description,
            "created_on": room.created_on,
            "updated_on":room.last_modified.split('=')[0],
            "updated_time":room.last_modified.split('=')[1],
            "last_modified": room.last_modified
        }
        json_post = json.dumps(result)
        return HttpResponse(json_post, content_type="application/json")
    except Exception as err:
        return HttpResponse(err, content_type="application/json")


def add_question(request):
    if request.method != "POST":
        return HttpResponse(json.dumps({"message": "wrong request method", "status": 400}), content_type="appication/json", status=400)
    try:
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        print(python_data)
        room = MysteryRoom.objects.filter(id=python_data['room_id'])
        if len(room) == 0:
            raise Exception(json.dumps(
                {"message": "mystery room  not found", "status": 400}))
        room = room[0]
        collection = MysteryRoomCollection.objects.filter(
            id=python_data['collection_id'])
        if len(collection) == 0:
            raise Exception(json.dumps(
                {"message": "mystery room collection not found", "status": 400}))
        collection = collection[0]
        question = MysteryRoomQuestion.objects.filter(
            room=room, mystery_room_collection=collection, question_number=python_data['question_number'])
        if len(question) != 0:
            raise Exception(json.dumps(
                {"message": "question already exists", "status": 400}))
        question = MysteryRoomQuestion(
            room=room,
            mystery_room_collection=collection,
            question_number=python_data['question_number'],
            question_text=python_data['question_text'],
            note=python_data['note'],
            hint_text=python_data['hint_text'],
            question_type=python_data['question_type']
        )
        question.save()
        if python_data['is_question_image']:
            question.question_image = str(collection.pk)+"___"+str(room.pk)+"___question___"+str(question.pk)
        if python_data['is_hint_image']:
            question.hint_image = str(collection.pk)+"___"+str(room.pk)+"___hint___"+str(question.pk)
        question.save()    
        options_list = python_data["options"]
        for item in options_list:
            option_instance = MysteryRoomOption(
                room=room,
                question=question,
                option_text=item[0],
                is_correct=item[1]
            )
            option_instance.save()
        result={"id":question.pk}
        return HttpResponse(json.dumps(result), content_type='application/json')
    except Exception as err:
        return HttpResponse(err, content_type="application/json")


def add_new_question(request):
    if request.method != "POST":
        return HttpResponse(json.dumps({"message": "wrong request method", "status": 400}), content_type="appication/json", status=400)
    try:
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        print(python_data)
        room = MysteryRoom.objects.filter(id=python_data['room_id'])
        if len(room) == 0:
            raise Exception(json.dumps(
                {"message": "mystery room  not found", "status": 400}))
        room = room[0]
        collection = MysteryRoomCollection.objects.filter(
            id=python_data['collection_id'])
        if len(collection) == 0:
            raise Exception(json.dumps(
                {"message": "mystery room collection not found", "status": 400}))
        collection = collection[0]
        # question = MysteryRoomQuestion.objects.filter(
        #     room=room, mystery_room_collection=collection, question_number=python_data['question_number'])
        # if len(question) != 0:
        #     raise Exception(json.dumps(
        #         {"message": "question already exists", "status": 400}))
        # question = MysteryRoomQuestion(
        #     room=room,
        #     mystery_room_collection=collection,
        #     question_number=python_data['question_number'],
        #     question_text=python_data['question_text'],
        #     question_image=collection.title+"___"+room.title +
        #     "___question___"+str(python_data['question_number']),
        #     note=python_data['note'],
        #     hint_text=python_data['hint_text'],
        #     hint_image=collection.title+"___"+room.title +
        #     "___hint___"+str(python_data['question_number']),
        #     question_type=python_data['question_type']
        # )
        # question.save()
        # options_list = python_data["options"]
        # for item in options_list:
        #     option_instance = MysteryRoomOption(
        #         room=room,
        #         question=question,
        #         option_text=item[0],
        #         is_correct=item[1]
        #     )
        #     option_instance.save()
        room.number_of_questions += 1
        room.save()
        return HttpResponse("added question", content_type='application/json')
    except Exception as err:
        return HttpResponse(err, content_type="application/json")


def edit_question(request):
    if request.method != "PUT":
        return HttpResponse(json.dumps({"message": "wrong request method", "status": 400}), content_type="appication/json", status=400)
    try:
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        print(python_data)
        room = MysteryRoom.objects.filter(id=python_data['room_id'])
        if len(room) == 0:
            raise Exception(json.dumps(
                {"message": "mystery room  not found", "status": 400}))
        room = room[0]
        collection = MysteryRoomCollection.objects.filter(
            id=python_data['collection_id'])
        if len(collection) == 0:
            raise Exception(json.dumps(
                {"message": "mystery room collection not found", "status": 400}))
        collection = collection[0]
        question = MysteryRoomQuestion.objects.filter(
            room=room, mystery_room_collection=collection, question_number=python_data['question_number'])
        if len(question) == 0:
            raise Exception(json.dumps(
                {"message": "question does not exist", "status": 400}))
        question = question[0]
        if question.question_image:
            key = question.question_image+".png"
            s3_client = boto3.client('s3')
            response = s3_client.delete_object(
                    Bucket=AWS_STORAGE_BUCKET_NAME, Key=key)
        if question.hint_image:
            key = question.hint_image+".png"
            s3_client = boto3.client('s3')
            response = s3_client.delete_object(
                    Bucket=AWS_STORAGE_BUCKET_NAME, Key=key)
        question.question_text = python_data['question_text']
        question.note = python_data['note']
        question.hint_text = python_data['hint_text']
        question.question_type = python_data['question_type']
        if python_data['is_question_image']:
            question.question_image = str(collection.pk)+"___"+str(room.pk)+"___question___"+str(question.pk)
        if python_data['is_hint_image']:
            question.hint_image = str(collection.pk)+"___"+str(room.pk)+"___question___"+str(question.pk)
        question.save()

        options_list = python_data["options"]
        options = MysteryRoomOption.objects.filter(
            room=room, question=question)
        for item in options:
            item.delete()
        for item in options_list:
            option_instance = MysteryRoomOption(
                room=room,
                question=question,
                option_text=item[0],
                is_correct=item[1]
            )
            option_instance.save()
        result={"id":question.pk}
        return HttpResponse(json.dumps(result), content_type='application/json')
    except Exception as err:
        return HttpResponse(err, content_type="application/json")


def delete_question(request, collection_id, room_id, question_number):
    if request.method != 'DELETE':
        return HttpResponse(json.dumps({"message": "wrong request method", "status": 400}), content_type="appication/json", status=400)
    try:
        room = MysteryRoom.objects.filter(id=room_id)
        if len(room) == 0:
            raise Exception(json.dumps(
                {"message": "mystery room  not found", "status": 400}))
        room = room[0]
        collection = MysteryRoomCollection.objects.filter(id=collection_id)
        if len(collection) == 0:
            raise Exception(json.dumps(
                {"message": "mystery room collection not found", "status": 400}))
        collection = collection[0]
        question = MysteryRoomQuestion.objects.filter(
            room=room, mystery_room_collection=collection, question_number=question_number)
        if len(question) != 0:
            question = question[0]
            if question.question_image:
                key = question.question_image+".png"
                s3_client = boto3.client('s3')
                response = s3_client.delete_object(
                        Bucket=AWS_STORAGE_BUCKET_NAME, Key=key)
            if question.hint_image:
                key = question.hint_image+".png"
                s3_client = boto3.client('s3')
                response = s3_client.delete_object(
                        Bucket=AWS_STORAGE_BUCKET_NAME, Key=key)
            question.delete()
            questions = MysteryRoomQuestion.objects.filter(
                mystery_room_collection=collection, room=room)
            for item in questions:
                if item.question_number > question_number:
                    item.question_number = item.question_number-1
                    item.save()
        room.number_of_questions = room.number_of_questions - 1
        room.save()

        return HttpResponse("deleted question", content_type='application/json')
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")


def get_particular_question(request, collection_id, room_id, question_number):
    if request.method != 'GET':
        return HttpResponse(json.dumps({"message": "wrong request method", "status": 400}))
    try:
        room = MysteryRoom.objects.filter(id=room_id)
        if len(room) == 0:
            raise Exception(json.dumps(
                {"message": "mystery room  not found", "status": 400}))
        room = room[0]
        collection = MysteryRoomCollection.objects.filter(id=collection_id)
        if len(collection) == 0:
            raise Exception(json.dumps(
                {"message": "mystery room collection not found", "status": 400}))
        collection = collection[0]
        question = MysteryRoomQuestion.objects.filter(
            room=room, mystery_room_collection=collection, question_number=question_number)
        if len(question) == 0:
            raise Exception(json.dumps(
                {"message": "question not found", "status": 400}))
        question = question[0]
        all_options_for_question = MysteryRoomOption.objects.filter(
            room=room, question=question)
        options = []
        for option in all_options_for_question:
            options.append({
                "option_text": option.option_text,
                "is_correct": option.is_correct
            })
        result = {
            "question_id": question.pk,
            "question_text": question.question_text,
            "question_image": imgBaseUrl+question.question_image+".png" if question.question_image else "",
            "note": question.note,
            "hint_text": question.hint_text,
            "hint_image": imgBaseUrl+question.hint_image+".png" if question.hint_image else "",
            "question_type": question.question_type,
            "options": options
        }
        return HttpResponse(json.dumps(result), content_type='application/json')
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")


def add_user_answer(request):
    if request.method != 'POST':
        return HttpResponse(json.dumps({"message": "wrong request method", "status": 400}))
    try:
        body = request.body
        stream = io.BytesIO(body)
        python_data = JSONParser().parse(stream)
        print(python_data)
        # check user exists or not
        user = User.objects.filter(email=python_data['user_email'])
        if len(user) == 0:
            raise Exception(json.dumps(
                {"message": "user not found", "status": 400}))
        user = user[0]
        # check room exists or not
        room = MysteryRoom.objects.filter(id=python_data['room_id'])
        if len(room) == 0:
            raise Exception(json.dumps(
                {"message": "mystery room  not found", "status": 400}))
        room = room[0]
        # check team exists or not
        teams = Team.objects.filter(
            team_lead=user.first_name, activity=Activity.objects.get(name="Mystery Room"))
        if len(teams) == 0:
            raise Exception(json.dumps(
                {"message": "team not found or user is not a team lead", "status": 400}))
        team = None
        for t in teams:
            reg = Registration.objects.filter(
                event=Event.objects.get(id=room.mystery_room.event_id), team=t)
            if len(reg) != 0:
                team = t
                break
        if team is None:
            raise Exception(json.dumps(
                {"message": "team not registered", "status": 400}))

        # check question exists or not
        question = MysteryRoomQuestion.objects.filter(
            room=room, mystery_room_collection=room.mystery_room, question_number=python_data['question_number'])
        if len(question) == 0:
            raise Exception(json.dumps(
                {"message": "question not found", "status": 400}))
        question = question[0]
        # check user answer already added or not
        user_answer = MRUserAnswer.objects.filter(
            mr_collection=room.mystery_room, mr_room=room, mr_question=question, team_id=team.pk)
        if len(user_answer) != 0:
            raise Exception(json.dumps(
                {"message": "user answer already exists", "status": 400}))

        user_answer = MRUserAnswer(
            team_id=team.pk,
            mr_collection=room.mystery_room,
            mr_room=room,
            mr_question=question,
            submitted_answer=python_data['answer']
        )
        user_answer.save()
        options = MysteryRoomOption.objects.filter(
            question=question, room=room, is_correct=True)
        print("options for the question ::", options)
        q_type = user_answer.mr_question.question_type
        if q_type == MysteryRoomQuestion.MCQ or q_type == MysteryRoomQuestion.TEXTFIELD:
            option = options[0]
            if option.option_text != user_answer.submitted_answer:
                return HttpResponse("user answer added but incorrect", content_type="application/json")
        else:
            option_list = [item.option_text for item in options]
            answer_list = user_answer.submitted_answer.split(',')
            print("user answer list :: ", answer_list)
            if len(option_list) != len(answer_list):
                return HttpResponse("user answer added but incorrect", content_type="application/json")
            for item in answer_list:
                if item not in option_list:
                    return HttpResponse("user answer added but incorrect", content_type="application/json")

        user_answer.is_correct = True
        user_answer.score = 10
        user_answer.save()

        return HttpResponse(json.dumps("user answer added, and correct"), content_type='application/json')
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json")


# check user can participate in event or not -> only registered team's team lead will participate
def check_team_lead(request, event_id, user_email):
    if request.method != 'GET':
        return HttpResponse(json.dumps({"message": "wrong request method", "status": 400}))

    try:
        # check user exists or not
        user = User.objects.filter(email=user_email)
        if len(user) == 0:
            raise Exception(json.dumps(
                {"message": "user not found", "status": 400}))
        user = user[0]
        # check team exists or not
        teams = Team.objects.filter(
            team_lead=user.first_name, activity=Activity.objects.get(name="Mystery Room"))
        if len(teams) == 0:
            raise Exception(json.dumps(
                {"message": "user is not a team lead", "status": 400}))
        team = None
        for t in teams:
            reg = Registration.objects.filter(
                event=Event.objects.get(id=event_id), team=t)
            if len(reg) != 0:
                team = t
                break
        if team is None:
            raise Exception(json.dumps(
                {"message": "team not registered", "status": 400}))

        return HttpResponse("user is a team lead and registered for the event", content_type="application/json")
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json", status=400)

# get user result room wise
def user_result(request, collection_id,user_email):
    if request.method != 'GET':
        return HttpResponse(json.dumps({"message": "wrong request method", "status": 400}))

    try:
        user = User.objects.filter(email=user_email)
        if len(user) == 0:
            raise Exception(json.dumps(
                {"message": "user not found", "status": 400}))
        user = user[0]
        collection = MysteryRoomCollection.objects.filter(id=collection_id)
        if len(collection) == 0:
            raise Exception(json.dumps(
                {"message": "mystery room collection not found", "status": 400}))
        collection = collection[0]
        room_list = MysteryRoom.objects.filter(mystery_room = collection)
        result=[]
        for room in room_list:
            if room.is_locked :
                raise Exception(json.dumps(
                    {"message": "all rooms are not played", "status": 400}))

            event = Event.objects.get(id=room.mystery_room.event_id)
            timer = []
            if event.event_type == "Group":
                # for group registration
                teams = Team.objects.filter(
                    team_lead=user.first_name, activity=Activity.objects.get(name="Mystery Room"))
                if len(teams) == 0:
                    raise Exception(json.dumps(
                        {"message": "team not found or user is not a team lead", "status": 400}))
                team = None
                for t in teams:
                    reg = Registration.objects.filter(
                        event=Event.objects.get(id=room.mystery_room.event_id), team=t)
                    if len(reg) != 0:
                        team = t
                        break
                if team is None:
                    raise Exception(json.dumps(
                        {"message": "team not registered", "status": 400}))
                timer = Timer.objects.filter(team_id=team.pk, room=room)
            else:
                # for individual registration
                ind_registration = Player.objects.filter(
                    user=user, event_id=event.pk)
                if len(ind_registration) == 0:
                    raise Exception(json.dumps(
                        {"message": "user not registered for the event", "status": 400}))
                timer = Timer.objects.filter(user_email=user.email, room=room)

            if len(timer) == 0:
                raise Exception(json.dumps(
                    {"message": "room not started yet", "status": 400}))
            timer = timer[0]

            time_diff = timer.end_time - timer.start_time #returns timedelta object
            diff = time_diff.seconds
            res = diff + timer.penalty*60

            result.append({
                "room_number":room.room_number,
                "room_id":room.pk,
                "room_title":room.title,
                "total_time":res
            })

        return HttpResponse(json.dumps(result), content_type="application/json")


    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json", status=400)

def start_collection(request,event_id,user_email):
    if request.method != 'POST':
        return HttpResponse(json.dumps({"message": "wrong request method", "status": 400}))
    try:
        user = User.objects.filter(email=user_email)
        if len(user) == 0:
            raise Exception(json.dumps(
                {"message": "user not found", "status": 400}))
        user = user[0] 
        print("user :: ",user)
        event = Event.objects.get(id=event_id)
        print("event ::",event)
        if event.task_id == 0:
            raise Exception(json.dumps({"message": "event not published", "status": 400}))
        collection = MysteryRoomCollection.objects.get(id=event.task_id)
        rooms = MysteryRoom.objects.filter(mystery_room = collection)
        print("collection ::",collection,",rooms ::",rooms)
        if event.event_type == "Group":
            print("Group event, finding team!")
            teams = Team.objects.filter(
                team_lead=user.first_name, activity=Activity.objects.get(name="Mystery Room"))
            if len(teams) == 0:
                raise Exception(json.dumps(
                    {"message": "team not found or user is not a team lead", "status": 400}))
            team = None
            for t in teams:
                reg = Registration.objects.filter(
                    event=event, team=t)
                if len(reg) != 0:
                    team = t
                    break
            if team is None:
                raise Exception(json.dumps(
                    {"message": "team not registered", "status": 400}))
            print("team found! ",team)
            for room in rooms:
                timer = Timer.objects.filter(team_id=team.pk, room=room)
                if len(timer) != 0: #timer already exists
                    continue
                timer = Timer(team_id=team.pk, room=room)
                print(timer)
                if room.room_number==1:
                    timer.is_locked = False
                timer.save()
                print("timer for room :",room," created")
        else:
            ind_registration = Player.objects.filter(user=user,event_id=event.pk)
            if len(ind_registration) == 0:
                raise Exception(json.dumps({"message": "user not registered for the event", "status": 400}))
            for room in rooms:
                timer = Timer.objects.filter(user_email=user.email, room=room)
                if len(timer) != 0: #timer already exists
                    continue
                timer = Timer(user_email=user.email, room=room)
                print(timer)
                if room.room_number==1:
                    timer.is_locked = False
                timer.save()
                print("timer for room :",room," created")
        return HttpResponse(json.dumps({"message":"timer details added","status":200}), content_type="application/json")
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json", status=400)

def get_timer_collection(request,event_id,user_email):
    if request.method != 'GET':
        return HttpResponse(json.dumps({"message": "wrong request method", "status": 400}))
    try:
        user = User.objects.filter(email=user_email)
        if len(user) == 0:
            raise Exception(json.dumps(
                {"message": "user not found", "status": 400}))
        user = user[0]
        event = Event.objects.get(id=event_id)
        collection = MysteryRoomCollection.objects.filter(event_id=event_id)
        if len(collection) == 0:
            raise Exception(json.dumps(
            {"message": "collection not found or event not published", "status": 400}))
        collection = collection[0]
        rooms = MysteryRoom.objects.filter(mystery_room = collection)
        res=[]
        if event.event_type == "Group":
            teams = Team.objects.filter(
                team_lead=user.first_name, activity=Activity.objects.get(name="Mystery Room"))
            if len(teams) == 0:
                raise Exception(json.dumps(
                    {"message": "team not found or user is not a team lead", "status": 400}))
            team = None
            for t in teams:
                reg = Registration.objects.filter(
                    event=event, team=t)
                if len(reg) != 0:
                    team = t
                    break
            if team is None:
                raise Exception(json.dumps(
                    {"message": "team not registered", "status": 400}))
            for room in rooms:
                timer = Timer.objects.filter(team_id=team.pk, room=room)
                if len(timer) == 0:
                    return HttpResponse("timer not added for the room.", content_type="application/json")
                timer=timer[0]
                res.append({
                    "room_id":room.pk,
                    "room_title":room.title,
                    "start_time":str(timer.start_time),
                    "is_complete":timer.is_complete,
                    "is_locked":timer.is_locked,
                    "end_time":str(timer.end_time),
                    "room_id": room.pk,
                    "room_number": room.room_number,
                    "banner_image": imgBaseUrl+room.banner_image+".png" if room.banner_image else "",
                    "difficulty_level": room.difficulty_level,
                    "number_of_questions": room.number_of_questions, 
                    "description": room.description,
                    "created_on": room.created_on,
                    "updated_on":room.last_modified.split('=')[0],
                    "updated_time":room.last_modified.split('=')[1],
                    "last_modified": room.last_modified
                })              
                
        else:
            ind_registration = Player.objects.filter(user=user,event_id=event.pk)
            if len(ind_registration) == 0:
                raise Exception(json.dumps({"message": "user not registered for the event", "status": 400}))
            for room in rooms:
                timer = Timer.objects.filter(user_email=user.email, room=room)
                if len(timer) == 0:
                    return HttpResponse("timer not added for the room.", content_type="application/json")
                timer=timer[0]
                res.append({
                    "room_id":room.pk,
                    "room_title":room.title,
                    "start_time":str(timer.start_time),
                    "is_complete":timer.is_complete,
                    "is_locked":timer.is_locked,
                    "end_time":str(timer.end_time),
                    "room_id": room.pk,
                    "room_number": room.room_number,
                    "banner_image": imgBaseUrl+room.banner_image+".png" if room.banner_image else "",
                    "difficulty_level": room.difficulty_level,
                    "number_of_questions": room.number_of_questions,
                    "description": room.description,
                    "created_on": room.created_on,
                    "updated_on":room.last_modified.split('=')[0],
                    "updated_time":room.last_modified.split('=')[1],
                    "last_modified": room.last_modified
                })  
        result=[{
            "collection_id":collection.pk,
            "collection_name":collection.title,
            "number_of_mystery_rooms":collection.number_of_mystery_rooms,
            "rooms":res,
        }]
                    
        return HttpResponse(json.dumps(result), content_type="application/json")
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json", status=400)


def start_room(request):
    if request.method != 'POST':
        return HttpResponse(json.dumps({"message": "wrong request method", "status": 400}))
    try:
        body = request.body
        stream = io.BytesIO(body)
        python_data = JSONParser().parse(stream)
        print(python_data)
        user = User.objects.filter(email=python_data['user_email'])
        if len(user) == 0:
            raise Exception(json.dumps(
                {"message": "user not found", "status": 400}))
        user = user[0]
        room = MysteryRoom.objects.filter(id=python_data['room_id'])
        if len(room) == 0:
            raise Exception(json.dumps(
                {"message": "mystery room  not found", "status": 400}))
        room = room[0]
        if room.mystery_room.event_id == 0:
            raise Exception(json.dumps({"message": "collection not published yet", "status": 400}))

        event = Event.objects.get(id=room.mystery_room.event_id)
        if event.event_type == "Group":
            teams = Team.objects.filter(
                team_lead=user.first_name, activity=Activity.objects.get(name="Mystery Room"))
            if len(teams) == 0:
                raise Exception(json.dumps(
                    {"message": "team not found or user is not a team lead", "status": 400}))
            team = None
            for t in teams:
                reg = Registration.objects.filter(
                    event=event, team=t)
                if len(reg) != 0:
                    team = t
                    break
            if team is None:
                raise Exception(json.dumps(
                    {"message": "team not registered", "status": 400}))
            timer = Timer.objects.filter(team_id=team.pk, room=room)
            if len(timer) == 0:
                return HttpResponse("timer not added", content_type="application/json")
            timer = timer[0]
            if timer.start_time:
                return HttpResponse(f"room already started at {timer.start_time} for team {team.name}", content_type="application/json")
            timer.start_time = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
            timer.save()
        else:
            ind_registration = Player.objects.filter(user=user,event_id=event.pk)
            if len(ind_registration) == 0:
                raise Exception(json.dumps({"message": "user not registered for the event", "status": 400}))
            timer = Timer.objects.filter(user_email=user.email, room=room)
            if len(timer) == 0:
                return HttpResponse("timer not added", content_type="application/json")
            timer = timer[0]
            if timer.start_time:
                return HttpResponse(f"room already started at {timer.start_time} for user {user.first_name}", content_type="application/json")
            timer.start_time = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
            timer.save()

        return HttpResponse(json.dumps({"message":"start time details added","status":200}), content_type="application/json")
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json", status=400)


def is_penalty(request):
    if request.method != 'POST':
        return HttpResponse(json.dumps({"message": "wrong request method", "status": 400}))
    try:
        body = request.body
        stream = io.BytesIO(body)
        python_data = JSONParser().parse(stream)
        print(python_data)
        user = User.objects.filter(email=python_data['user_email'])
        if len(user) == 0:
            raise Exception(json.dumps(
                {"message": "user not found", "status": 400}))
        user = user[0]
        room = MysteryRoom.objects.filter(id=python_data['room_id'])
        if len(room) == 0:
            raise Exception(json.dumps(
                {"message": "mystery room  not found", "status": 400}))
        room = room[0]

        event = Event.objects.get(id=room.mystery_room.event_id)
        timer=[]
        next_room = MysteryRoom.objects.filter(mystery_room = room.mystery_room,room_number = room.room_number+1)
        next_timer=[]
        if event.event_type == "Group":
            #for group registration
            teams = Team.objects.filter(
                team_lead=user.first_name, activity=Activity.objects.get(name="Mystery Room"))
            if len(teams) == 0:
                raise Exception(json.dumps(
                    {"message": "team not found or user is not a team lead", "status": 400}))
            team = None
            for t in teams:
                reg = Registration.objects.filter(event=event, team=t)
                if len(reg) != 0:
                    team = t
                    break
            if team is None:
                raise Exception(json.dumps(
                    {"message": "team not registered", "status": 400}))

            timer = Timer.objects.filter(team_id=team.pk, room=room)
            
            if len(next_room) !=0:
                next_timer = Timer.objects.filter(team_id=team.pk, room=next_room)

        else:
            #for individual registration
            ind_registration = Player.objects.filter(user=user, event_id=event.pk)
            if len(ind_registration) == 0:
                raise Exception(json.dumps({"message": "user not registered for the event", "status": 400}))
            timer = Timer.objects.filter(user_email=user.email, room=room)
            if len(next_room) !=0:
                next_timer = Timer.objects.filter(user_email=user.email, room=next_room)

        if len(timer) == 0:
            raise Exception(json.dumps({"message": "timer not added", "status": 400}))
        timer = timer[0]
        timer.penalty += python_data['is_penalty']
        if python_data['is_last_question'] and python_data['is_penalty'] == 0:
            timer.end_time = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
            timer.is_complete=True
            if len(next_timer)!=0:
                next_timer = next_timer[0]
                next_timer.is_locked = False
                next_timer.save()            
        else:
            timer.latest_question += 1
        timer.save()

        return HttpResponse(json.dumps({"message":"timer updated","status":200}), content_type="application/json")
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json", status=400)


def get_result(request, user_email, room_id):
    if request.method != 'GET':
        return HttpResponse(json.dumps({"message": "wrong request method", "status": 400}))
    try:
        user = User.objects.filter(email=user_email)
        if len(user) == 0:
            raise Exception(json.dumps(
                {"message": "user not found", "status": 400}))
        user = user[0]
        room = MysteryRoom.objects.filter(id=room_id)
        if len(room) == 0:
            raise Exception(json.dumps(
                {"message": "mystery room  not found", "status": 400}))
        room = room[0]
        
        event = Event.objects.get(id=room.mystery_room.event_id)
        timer = []
        if event.event_type == "Group":
            # for group registration
            teams = Team.objects.filter(
                team_lead=user.first_name, activity=Activity.objects.get(name="Mystery Room"))
            if len(teams) == 0:
                raise Exception(json.dumps(
                    {"message": "team not found or user is not a team lead", "status": 400}))
            team = None
            for t in teams:
                reg = Registration.objects.filter(
                    event=Event.objects.get(id=room.mystery_room.event_id), team=t)
                if len(reg) != 0:
                    team = t
                    break
            if team is None:
                raise Exception(json.dumps(
                    {"message": "team not registered", "status": 400}))
            timer = Timer.objects.filter(team_id=team.pk, room=room)
        else:
            # for individual registration
            ind_registration = Player.objects.filter(
                user=user, event_id=event.pk)
            if len(ind_registration) == 0:
                raise Exception(json.dumps(
                    {"message": "user not registered for the event", "status": 400}))
            timer = Timer.objects.filter(user_email=user.email, room=room)

        if len(timer) == 0:
            return HttpResponse(json.dumps({"message": "room not started yet", "status": 200}), content_type="application/json")
        timer = timer[0]
        current_time=0
        if timer.end_time:
            current_time=timer.end_time
        else:
            current_time = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
        time_diff = current_time - timer.start_time #returns timedelta object
        diff = time_diff.seconds
        res = diff + timer.penalty*60

        result = {
            "start_time": str(timer.start_time),
            "end_time":str(timer.end_time) if timer.end_time else "",
            "current_time":str(current_time),
            "timer": diff,
            "result":res,
            "latest_question": timer.latest_question,
            "is_complete":timer.is_complete
        }
        return HttpResponse(json.dumps(result), content_type="application/json")
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json", status=400)
