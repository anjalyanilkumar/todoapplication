from multiprocessing import context
from django.shortcuts import render
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from api.models import Todos
from api.serializers import TodoSerializer, RegistrationSerializer
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework import authentication, permissions


# Create your views here.
class TodosView(ViewSet):
    def list(self,request,*args,**kwargs):
        qs=Todos.objects.all()
        ser = TodoSerializer(qs,many=True)
        return Response(data=ser.data)
    
    def create(self,request,*args,**kwargs):
        ser = TodoSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(data=ser.data)
        else:
            return Response(data=ser.errors)

    def retrieve(self,request,*args,**kwargs):
        rid = kwargs.get('pk')
        qs = Todos.objects.get(id=rid)
        ser= TodoSerializer(qs,many=False)
        return Response(data=ser.data)
    
    def update(self,request,*args,**kwargs):
        uid = kwargs.get('pk')
        obj = Todos.objects.get(id=uid)
        ser = TodoSerializer(data=request.data, instance=obj)
        if ser.is_valid():
            ser.save()
            return Response(data=ser.data)
        else:
            return Response(data=ser.errors)

    def destroy(self,request,*args,**kwargs):
        did = kwargs.get('pk')
        Todos.objects.get(id = did).delete()
        return Response(data='Deleted')


class TodosModelViews(ModelViewSet):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = TodoSerializer
    queryset = Todos.objects.all()

    def create(self, request, *args, **kwargs):
        ser =TodoSerializer(data=request.data, context={'user': self.request.user})
        if ser.is_valid():
            ser.save()
            # Todos.objects.create(**ser.validated_data, user=request.user)
            return Response(data=ser.data)
        else:
            return Response(data=ser.errors)

    # def perform_create(self, serializer):
    #     return serializer.save(user=self.request.user)

    # def list(self, request, *args, **kwargs):
    #     qs = Todos.objects.filter(user=request.user)
    #     ser = TodoSerializer(qs,many=True)
    #     return Response(data=ser.data)

    def get_queryset(self):
        return Todos.objects.filter(user=self.request.user)
        
    @action(methods=["GET"], detail=False)
    def pending_todos(self,request,*args,**kwargs):
        qs = Todos.objects.filter(status=False)
        ser = TodoSerializer(qs,many=True)
        return Response(data=ser.data)
        
    @action(methods=["GET"], detail=False)
    def completed_todos(self,request,*args,**kwargs):
        qs = Todos.objects.filter(status=True)
        ser = TodoSerializer(qs,many=True)
        return Response(data=ser.data)

    @action(methods=["POST"], detail=True)
    def mark_as_done(self,request,*args,**kwargs):
        uid = kwargs.get('pk')
        # Todos.objects.filter(id=uid).update(status=True)
        qs = Todos.objects.get(id=uid)
        qs.status=True
        qs.save()
        ser = TodoSerializer(qs, many=False)
        return Response(data=ser.data)


class UsersView(ModelViewSet):
    serializer_class = RegistrationSerializer
    queryset = User.objects.all()

    # def create(self, request, *args, **kwargs):
    #     ser = RegistrationSerializer(data=request.data)
    #     if ser.is_valid():
    #         usr = User.objects.create_user(**ser.validated_data)
    #         return Response(data=ser.data)
    #     else:
    #         return Response(data=ser.errors)

    