from django.http import HttpResponse
import io
from rest_framework.parsers import JSONParser
from .models import MRUserAnswer, MysteryRoom, MysteryRoomCollection, MysteryRoomOption, MysteryRoomQuestion
import json
from app1.models import Event, Team, Player, Activity, Registration
import datetime
from GrapheneTest.settings import CLOUDFRONT_DOMAIN as imgBaseUrl
from django.contrib.auth.models import User


def service_check(request):
    return HttpResponse("Mystery Room Service up and running...", content_type="application/json", status=200)


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
        return HttpResponse(json.dumps({"message": "wrong request method", "status": 400}), content_type="appication/json", status=400)
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
    if request.method != "GET":
        return HttpResponse(json.dumps({"message": "wrong request method", "status": 400}), content_type="appication/json", status=400)
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
            "event_date": "Mystery Room Collection not published" if collection.event_id == 0 else str(Event.objects.get(id=collection.event_id).start_date),
            "title": collection.title,
            "banner_image": imgBaseUrl+"/"+collection.banner_image,
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
        return HttpResponse(json.dumps({"message": "wrong request method", "status": 400}), content_type="appication/json", status=400)
    try:
        result = []
        collections = MysteryRoomCollection.objects.all()
        for collection in collections:
            result.append({
                "collection_id": collection.pk,
                "event_id": collection.event_id,
                "event_name": "Mystery Room Collection not published" if collection.event_id == 0 else Event.objects.get(id=collection.event_id).name,
                "event_date": "Mystery Room Collection not published" if collection.event_id == 0 else str(Event.objects.get(id=collection.event_id).start_date),
                "title": collection.title,
                "banner_image": imgBaseUrl+"/"+collection.banner_image,
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
            banner_image="room___"+python_data['title'],
            title=python_data['title'],
            difficulty_level=python_data['difficulty_level'],
            number_of_questions=python_data['number_of_questions'],
            description=python_data['description'],
            created_on=python_data['created_on'],
            total_time=python_data['total_time']
        )
        room.save()
        print("saving room")
        return HttpResponse("created mystery room", content_type='application/json')
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
        room.banner_image = "room___"+python_data['title']
        room.title = python_data['title']
        room.difficulty_level = python_data['difficulty_level']
        room.description = python_data['description']
        room.last_modified = python_data['last_modified']
        room.total_time = python_data['total_time']
        room.save()
        print("saving room")
        return HttpResponse("edited mystery room", content_type='application/json')
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
        rooms = MysteryRoom.objects.filter(mystery_room=collection)
        result = []
        print(rooms)
        for room in rooms:
            questions = MysteryRoomQuestion.objects.filter(
                room=room, mystery_room_collection=collection)
            print(questions)
            result.append({
                "room_id": room.pk,
                "banner_image": imgBaseUrl+"/"+room.banner_image,
                "title": room.title,
                "difficulty_level": room.difficulty_level,
                "number_of_questions": room.number_of_questions,
                "number_of_questions_left": room.number_of_questions-len(questions),
                "description": room.description,
                "created_on": room.created_on,
                "last_modified": room.last_modified,
                "total_time": room.total_time
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
            room=room, mystery_room_collection=collection)
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
                "question_image": question.question_image,
                "note": question.note,
                "hint_text": question.hint_text,
                "hint_image": question.hint_image,
                "question_type": question.question_type,
                "question_number": question.question_number,
                "options": options,
            })
        result = {
            "room_id": room.pk,
            "banner_image": imgBaseUrl+"/"+room.banner_image,
            "questions": ques_info,
            "title": room.title,
            "difficulty_level": room.difficulty_level,
            "number_of_questions": room.number_of_questions,
            "number_of_questions_left": room.number_of_questions-len(ques_info),
            "description": room.description,
            "created_on": room.created_on,
            "last_modified": room.last_modified,
            "total_time": room.total_time
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
            question_image=collection.title+"___"+room.title +
            "___question___"+str(python_data['question_number']),
            note=python_data['note'],
            hint_text=python_data['hint_text'],
            hint_image=collection.title+"___"+room.title +
            "___hint___"+str(python_data['question_number']),
            question_type=python_data['question_type']
        )
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

        return HttpResponse("added question", content_type='application/json')
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
            question_image=collection.title+"___"+room.title +
            "___question___"+str(python_data['question_number']),
            note=python_data['note'],
            hint_text=python_data['hint_text'],
            hint_image=collection.title+"___"+room.title +
            "___hint___"+str(python_data['question_number']),
            question_type=python_data['question_type']
        )
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
        question.question_text = python_data['question_text']
        question.question_image = collection.title+"___"+room.title + \
            "___question___"+str(python_data['question_number'])
        question.note = python_data['note']
        question.hint_text = python_data['hint_text']
        question.hint_image = collection.title+"___"+room.title + \
            "___hint___"+str(python_data['question_number'])
        question.question_type = python_data['question_type']
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

        return HttpResponse("edited question", content_type='application/json')
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
        if len(question) == 0:
            raise Exception(json.dumps(
                {"message": "question not found", "status": 400}))
        question = question[0]
        question.delete()
        room.number_of_questions = room.number_of_questions - 1
        room.save()
        questions = MysteryRoomQuestion.objects.filter(
            mystery_room_collection=collection, room=room)
        for item in questions:
            if item.question_number > question_number:
                item.question_number = item.question_number-1
                item.save()
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
            "question_image": question.question_image,
            "note": question.note,
            "hint_text": question.hint_text,
            "hint_image": question.hint_image,
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
        #check user exists or not
        user = User.objects.filter(email=python_data['user_email'])
        if len(user) == 0:
            raise Exception(json.dumps(
                {"message": "user not found", "status": 400}))
        user = user[0]
        #check room exists or not
        room = MysteryRoom.objects.filter(id=python_data['room_id'])
        if len(room) == 0:
            raise Exception(json.dumps({"message": "mystery room  not found", "status": 400}))
        room = room[0]
        # check team exists or not
        teams = Team.objects.filter(
            team_lead=user.first_name, activity=Activity.objects.get(name="Mystery Room"))
        if len(teams) == 0:
            raise Exception(json.dumps({"message": "team not found or user is not a team lead", "status": 400}))
        team=None
        for t in teams:
            reg = Registration.objects.filter(event=Event.objects.get(id=room.mystery_room.event_id),team=t)
            if len(reg) != 0:
                team=t
                break
        if team is None:
            raise Exception(json.dumps({"message": "team not registered", "status": 400}))
        
        #check question exists or not
        question = MysteryRoomQuestion.objects.filter(
            room=room, mystery_room_collection=room.mystery_room, question_number=python_data['question_number'])
        if len(question) == 0:
            raise Exception(json.dumps({"message": "question not found", "status": 400}))
        question = question[0]
        #check user answer already added or not
        user_answer = MRUserAnswer.objects.filter(
            mr_collection=room.mystery_room, mr_room=room, mr_question=question, team_id=team.pk)
        if len(user_answer) != 0:
            raise Exception(json.dumps({"message": "user answer already exists", "status": 400}))

        user_answer = MRUserAnswer(
            team_id=team.pk,
            mr_collection=room.mystery_room,
            mr_room=room,
            mr_question=question,
            submitted_answer=python_data['answer']
        )
        user_answer.save()
        options = MysteryRoomOption.objects.filter(question=question, room=room, is_correct=True)
        print("options for the question ::",options)
        q_type = user_answer.mr_question.question_type
        if q_type == MysteryRoomQuestion.MCQ or q_type == MysteryRoomQuestion.TEXTFIELD:
            option=options[0]
            if option.option_text != user_answer.submitted_answer:
                return HttpResponse("user answer added but incorrect", content_type="application/json")           
        else:
            option_list = [item.option_text for item in options]
            answer_list = user_answer.submitted_answer.split(',')
            print("user answer list :: ",answer_list)
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


#check user can participate in event or not -> only registered team's team lead will participate
def check_user_participation(request,event_id,user_email):
    if request.method != 'GET':
        return HttpResponse(json.dumps({"message": "wrong request method", "status": 400}))

    try:
        #check user exists or not
        user = User.objects.filter(email=user_email)
        if len(user) == 0:
            raise Exception(json.dumps({"message": "user not found", "status": 400}))
        user = user[0]
        # check team exists or not
        teams = Team.objects.filter(team_lead=user.first_name, activity=Activity.objects.get(name="Mystery Room"))
        if len(teams) == 0:
            raise Exception(json.dumps({"message": "user is not a team lead", "status": 400}))
        team = None
        for t in teams:
            reg = Registration.objects.filter(event=Event.objects.get(id=event_id), team=t)
            if len(reg) != 0:
                team = t
                break
        if team is None:
            raise Exception(json.dumps({"message": "team not registered", "status": 400}))

        return HttpResponse("user is a team lead and registered for the event", content_type="application/json")
    except Exception as err:
        print(err)
        return HttpResponse(err, content_type="application/json",status=400)

#get user result room wise
def user_result(request,collection_id):
    if request.method != 'GET':
        return HttpResponse(json.dumps({"message": "wrong request method", "status": 400}))
