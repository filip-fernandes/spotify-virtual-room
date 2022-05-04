import code
from os import stat
from tkinter import N
from django.http import JsonResponse
from itsdangerous import Serializer
from rest_framework import generics, status
from .models import Room
from .serializers import RoomSerializer, CreateRoomSerializer, UpdateRoomSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.
class RoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


# Get data from the room { votes_to_skip, guest_can_pause, is_host }
class GetRoom(APIView):
    lookup_url_kwarg = "code"
    serialzer_class = RoomSerializer
    
    def get(self, request, format=None):
        code = request.GET.get(self.lookup_url_kwarg)
        if code != None:
            room = Room.objects.filter(code=code)
            if len(room) > 0:
                data = RoomSerializer(room[0]).data
                data["is_host"] = self.request.session.session_key == room[0].host

                return Response(data, status=status.HTTP_200_OK)
            return Response({"Room Not Found": "Invalid Room Code"},
                            status=status.HTTP_404_NOT_FOUND)
        return Response({"Bad Request": "Code parameter not found in request"}, 
                        status=status.HTTP_400_BAD_REQUEST)


# Register room code into user's session and validate the code
class JoinRoom(APIView):
    lookup_url_kwarg = "code"

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        
        code = request.data.get(self.lookup_url_kwarg)
        if code != None:
            room_result = Room.objects.filter(code=code)
            if len(room_result) > 0:
                room = room_result[0]

                self.request.session["room_code"] = code
                
                return Response({"message": "Room Joined!"}, status=status.HTTP_200_OK)
            return Response({"Bad Request": "Invalid Room Code"}, status=status.HTTP_400_BAD_REQUEST)  
        return Response({"Bad Request": "Invalid post data, did not find a code key"},
                        status=status.HTTP_400_BAD_REQUEST)


# Create a new room
class CreateRoomView(APIView):
    serializer_class = CreateRoomSerializer

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get("guest_can_pause")
            votes_to_skip = serializer.data.get("votes_to_skip")
            host = self.request.session.session_key

            queryset = Room.objects.filter(host=host)
            if queryset.exists():
                room = queryset[0]

                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                room.save(update_fields=["guest_can_pause", "votes_to_skip"])

                self.request.session["room_code"] = room.code

                return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)
            else:
                room = Room(host=host, guest_can_pause=guest_can_pause, votes_to_skip=votes_to_skip)
                room.save()
                
                self.request.session["room_code"] = room.code

                return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)
        return Response({"Bad Request': 'Invalid data..."}, status=status.HTTP_400_BAD_REQUEST)
        

# Verify if the user is in the a room to redirect him to the room he belongs
class UserInRoom(APIView):
    def get(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        data = {
            "code": self.request.session.get("room_code")
        }
        return JsonResponse(data, status=status.HTTP_200_OK)


# Remove the room code from the session (user) if the session is the host, delete the room
class LeaveRoom(APIView):
    def post(self, request, format=None):
        if "room_code" in self.request.session:
            # Remove the code from the session
            self.request.session.pop("room_code")

            # Delete the room in case the host is the one leaving
            host_id = self.request.session.session_key
            room_results = Room.objects.filter(host=host_id)
            if len(room_results) > 0:
                room = room_results[0]
                room.delete()

        return Response({"Message": "Success"}, status=status.HTTP_200_OK)


# Verify if the user is the host. If he is, update the data he posted
class UpdateRoom(APIView):
    serailizer_class = UpdateRoomSerializer

    def patch(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serailizer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get("guest_can_pause")
            votes_to_skip = serializer.data.get("votes_to_skip")
            code = serializer.data.get("code")

            queryset = Room.objects.filter(code=code)
            if not queryset.exists():
                return Response({"Message": "Room not Found"}, status=status.HTTP_404_NOT_FOUND)
            
            room = queryset[0]
            user_id = self.request.session.session_key
            if room.host != user_id:
                return Response({"Message": "You are not the host of this room"}, status=status.HTTP_403_FORBIDDEN)

            room.guest_can_pause = guest_can_pause
            room.votes_to_skip = votes_to_skip
            room.save(update_fields=["guest_can_pause", "votes_to_skip"])
            
            return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)

        return Response({"Bad request": "Invalid Data..."}, status=status.HTTP_400_BAD_REQUEST)
