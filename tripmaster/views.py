from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from tripmaster.serializers import UserSerializer, TripSerializer, TripMemberSerializer
from django.contrib.auth.models import User
from tripmaster.models import TripDb, TripMemberDb
from rest_framework import authentication, permissions, serializers
from tripmaster.permissions import OwnerOnly
from rest_framework.exceptions import PermissionDenied
# Create your views here.


class SignUpView(APIView):
  def post(self,request):
    form_data = request.data
    serializer_instance = UserSerializer(data=form_data)
    
    if serializer_instance.is_valid():
      serializer_instance.save()
      return Response(data={"message" : "user created successfully..!"}, status=201)

    else:
        return Response(data=serializer_instance.errors, status=400)
    


class UserListView(APIView):
  def get(self,request):
    users = User.objects.all()
    serializer_instance = UserSerializer(users,many=True)
    return Response(data=serializer_instance.data)
    



   
class TripListCreateView(APIView):

    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        qs = TripDb.objects.filter(created_by=request.user)
        serializer_instance = TripSerializer(qs, many=True)
        return Response(data=serializer_instance.data, status=200)


    def post(self, request):
      form_data = request.data
      serializer_instance = TripSerializer(data=form_data)

      if serializer_instance.is_valid():
        serializer_instance.save(created_by=request.user)
        return Response(data={"message": "trip created successfully..!",
                             "trip":serializer_instance.data},status=201)
      else:
        return Response(data=serializer_instance.errors,status=400)


class TripRetriveUpdateDeleteView(APIView):
  
  authentication_classes = [authentication.BasicAuthentication]
  permission_classes = [OwnerOnly]

  def get(self,request,pk):
    trip_object = get_object_or_404(TripDb,id=pk)
    if trip_object.created_by == request.user:
    
      serializer_instance = TripSerializer(trip_object)
      return Response(data=serializer_instance.data,status=200) 
    else:
      return serializers.ValidationError("you are not allowed to access the trip")     


  def put(self,request,pk):
    trip_object = get_object_or_404(TripDb,id=pk)
   
    form_data = request.data
    serializer_instance = TripSerializer(data=form_data, instance = trip_object)
    if serializer_instance.is_valid():
      serializer_instance.save()
      return Response(data={"message" : "trip updated successfully",
                              "updated trip successfully" : serializer_instance.data}, status=200) 
    else:
      return Response(data=serializer_instance.errors)

  def delete(self,request,pk):
    trip_object = get_object_or_404(TripDb,id=pk)
    if trip_object.created_by == request.user:
      trip_object.delete()
      return Response(data={"message" : "trip deleted successfullly"},status=200)
    else:
      raise serializers.ValidationError("You are not allowed to delete this trip")


class TripMemberListCreateView(APIView):
  authentication_classes = [authentication.BasicAuthentication]
  permission_classes = [OwnerOnly]

  def get(self,request,trip_id):
    trip_object =  get_object_or_404(TripDb, id=trip_id)
    is_owner = trip_object.created_by = request.user
    is_member = TripMemberDb.objects.filter(trip=trip_object,user=request.user).exists()
    if not (is_owner or is_member):
      raise serializers.ValidationError("you are not allowed to access this trip..!")
    members = TripMemberDb.objects.filter(trip=trip_object)
    serializer_instance = TripMemberSerializer(members, many=True) 
    return Response(data=serializer_instance.data, status=200) 



  def post(self,request,trip_id):
    trip_object = get_object_or_404(TripDb, id=trip_id)

    if trip_object.created_by != request.user:
      raise PermissionDenied("only the trip owner can added members..!")

    form_data = request.data
      
    serializer_instance = TripMemberSerializer(data=form_data,context={'trip' : trip_object})

    if serializer_instance.is_valid():
      serializer_instance.save()
      return Response(data={
        "message" : "trip member added successfully..!"
      })
    else:
        return Response(data=serializer_instance.errors)  


class TripMemberDeleteView(APIView):
  authentication_classes = [authentication.BasicAuthentication]
  permission_classes = [permissions.IsAuthenticated]

  def delete(self,request,trip_id,member_id):
    trip_object = get_object_or_404(TripDb,id=trip_id)

    if trip_object.created_by != request.user:
      raise PermissionDenied("only trip owners can delete members..!")

    member_object = get_object_or_404(TripMemberDb, id=member_id, trip=trip_object)

    member_object.delete()
    return Response(data={
      "message":"trip member deleted successfully..!"
    })  


