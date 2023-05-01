from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PanicSerializer, CallSerializer, TrackMeSerializer, LocationSerializer, ImageSerializer, NotificationSerializer
from .models import PanicRequest, CallRequest, TrackMeRequest, StaffLocation, Images, Notifications
from django.contrib.auth import get_user_model
from rest_framework import status, generics
from accounts.serializers import UserDetailSerializer
from django.http import Http404
from accounts.permissions import IsAdmin, IsSuperUser
from rest_framework.permissions import IsAuthenticated

User = get_user_model()

def notification_handler(user, status):
    notify = Notifications.objects.create(user=user, status=status)

    return notify





class PanicView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        serializer = PanicSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(user=request.user)
        status = "new panic request"
        notification_handler(user=request.user, status=status)
        data = {
            "message": "panic request sent",
            "user": {
                "phone": request.user.phone
            }
        }
        return Response(data, status=200)
    

class GetPanicRequestAdmin(APIView):
    permission_classes = (IsAdmin,)

    def get(self, request):
        users = User.objects.filter(user=request.user.id)
        
        data = []
        for user in users:
            panic_requests = PanicRequest.objects.filter(user=user, is_deleted=False).order_by('-id')
            for panic_request in panic_requests:
                serializer = PanicSerializer(panic_request)
                request_data = {
                    "id": serializer.data['id'],
                    "longitude": serializer.data['longitude'],
                    "latitude": serializer.data['latitude'],
                    "location": serializer.data['location'],
                    "is_reviewed": serializer.data['is_reviewed'],
                    "timestamp": serializer.data['timestamp'],
                    "user": {
                        "id": user.id,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "email": user.email,
                        "location": user.location,
                        "phone": user.phone,
                        "role": user.role
                    }
                }
                data.append(request_data)

        return Response(data, status=200)

class PanicActions(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAdmin,)
    queryset = PanicRequest.objects.filter(is_deleted=False)
    serializer_class = PanicSerializer

    def delete(self, request, pk):
        try:
            obj = PanicRequest.objects.get(id=pk)
        except PanicRequest.DoesNotExist:
            return Response({"error": "panic request not found"}, status=404)
        if not obj.is_deleted:
            obj.is_deleted = True
            obj.save()
            return Response({"message": "success"}, status=200)

        else:
            return Response({"error": "object already deleted"}, status=400)


class PanicReview(APIView):
    permission_classes = (IsAdmin,)
    def post(self, request, pk):
        try:
            obj = PanicRequest.objects.get(id=pk)
        except PanicRequest.DoesNotExist:
            return Response({"error": "reqeust not found"}, status=404)
        if not obj.is_reviewed:
            obj.is_reviewed = True
            obj.save()
            return Response({"message": "review success"}, status=200)
        else:
            return Response({"error": "request already reviewed"}, status=400)
        
    def delete(self, request, pk):
        try:
            obj = PanicRequest.objects.get(id=pk)
        except PanicRequest.DoesNotExist:
            return Response({"error": "reqeust not found"}, status=404)
        if obj.is_reviewed:
            obj.is_reviewed = False
            obj.save()
            return Response({"message": "unreviewed!"}, status=200)
        else:
            return Response({"error": "request not reviewed"}, status=400)

class PanicGenuineView(APIView):
    permission_classes = (IsAdmin,)
    def post(self, request, pk):
        try:
            obj = PanicRequest.objects.get(id=pk)
        except PanicRequest.DoesNotExist:
            return Response({"error": "reqeust not found"}, status=404)
        if obj.is_genuine:
            obj.is_genuine = False
            obj.save()
            return Response({"message": "review success"}, status=200)
        else:
            return Response({"error": "request already reviewed"}, status=400)
        
    def delete(self, request, pk):
        try:
            obj = PanicRequest.objects.get(id=pk)
        except PanicRequest.DoesNotExist:
            return Response({"error": "reqeust not found"}, status=404)
        if not obj.is_genuine:
            obj.is_genuine = True
            obj.save()
            return Response({"message": "unreviewed!"}, status=200)
        else:
            return Response({"error": "request not reviewed"}, status=400)


class AllPanicRequest(generics.ListAPIView):
    queryset = PanicRequest.objects.all().order_by('-id')
    permission_classes = (IsAdmin,)
    serializer_class = PanicSerializer

    
class CallRequestView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        serializer = CallSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, phone=request.user.phone)
        status = "new call request"
        notification_handler(user=request.user, status=status)
        data = {
            "message": "call request successful",
            "id": request.user.id
        }
        return Response(data, status=200)

class CallRequestActions(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAdmin,)
    queryset = CallRequest.objects.filter(is_deleted=False)
    serializer_class = CallSerializer

    def delete(self, request, pk):
        try:
            obj = CallRequest.objects.get(id=pk)
        except CallRequest.DoesNotExist:
            return Response({"error": "object not found"}, status=404)
        if not obj.is_deleted:
            obj.is_deleted = True
            obj.save()
            return Response({"message": "success"}, status=200)
        else:
            return Response({"error": "object is already deleted"}, status=400)
        

class GetCallRequestAdmin(APIView):
    permission_classes = (IsAdmin,)
 
    def get(self, request):
        users = User.objects.filter(user=request.user.id)
        
        data = []
        for user in users:
            call_requests = CallRequest.objects.filter(user=user, is_deleted=False).order_by('-id')
            for call_request in call_requests:
                serializer = CallSerializer(call_request)
                request_data = {
                    "id": serializer.data['id'],
                    "phone": serializer.data['phone'],
                    "is_reviewed": serializer.data['is_reviewed'],
                    "timestamp": serializer.data['timestamp'],
                    "user": {
                        "id": user.id,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "email": user.email,
                        "location": user.location,
                        "phone": user.phone,
                        "role": user.role
                    }
                }
                data.append(request_data)

        return Response(data, status=200)
    

class CallReview(APIView):
    permission_classes = (IsAdmin,)
    def post(self, request, pk):
        try:
            obj = CallRequest.objects.get(id=pk)
        except CallRequest.DoesNotExist:
            return Response({"error": "reqeust not found"}, status=404)
        if not obj.is_reviewed:
            obj.is_reviewed = True
            obj.save()
            return Response({"message": "review success"}, status=200)
        else:
            return Response({"error": "request already reviewed"}, status=400)

    def delete(self, request, pk):
        try:
            obj = CallRequest.objects.get(id=pk)
        except CallRequest.DoesNotExist:
            return Response({"error": "reqeust not found"}, status=404)
        if obj.is_reviewed:
            obj.is_reviewed = False
            obj.save()
            return Response({"message": "unreviewed!"}, status=200)
        else:
            return Response({"error": "request not reviewed"}, status=400)


class IncidentCounts(APIView):
    permission_classes = (IsAdmin,)
    def get(self, request):
        try:
            user_obj = User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            return Response({"error": "user not found"}, status=404)
        total_panic = user_obj.total_admin_panic
        total_reviewed = user_obj.total_reviewed_panic
        total_unreviewed = user_obj.total_unreviewed_panic
        total_ingenuine = user_obj.total_ingenuine_panic

        data = {
            "total_panic": total_panic,
            "total_reviewed": total_reviewed,
            "total_unreviewed": total_unreviewed,
            "total_ingenuine": total_ingenuine
        }

        return Response(data, status=200)
       


class TrackMeRequestView(APIView):
    def post(self, request):
        serializer = TrackMeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        status = "new track me request"
        notification_handler(user=request.user, status=status)
        data = {
            "message": "tracking request sent",
            "user": {
                "phone": request.user.phone,
            }
        }
        return Response(data, status=200)
    

class TrackActions(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAdmin,)
    queryset = TrackMeRequest.objects.filter(is_deleted=False)
    serializer_class = TrackMeSerializer

    def delete(self, request, pk):
        try:
            obj = TrackMeRequest.objects.get(id=pk)
        except TrackMeRequest.DoesNotExist:
            return Response({"error": "object not found"}, status=404)
        if not obj.is_deleted:
            obj.is_deleted = True
            obj.save()
            return Response({"message": "success"}, status=200)
        else:
            return Response({"error": "object already deleted"}, status=400)
        
        
class GetTrackMeRequestAdmin(APIView):
    permission_classes = (IsAdmin,)
 
    def get(self, request):
        users = User.objects.filter(user=request.user)
        
        data = []
        for user in users:
            track_requests = TrackMeRequest.objects.filter(user=user, is_deleted=False).order_by('-id')
            for track_request in track_requests:
                serializer = TrackMeSerializer(track_request)
                request_data = {
                    "id": serializer.data['id'],
                    "longitude": serializer.data['longitude'],
                    "latitude": serializer.data['latitude'],
                    "location": serializer.data['location'],
                    "is_reviewed": serializer.data['is_reviewed'],
                    "timestamp": serializer.data['timestamp'],
                    "user": {
                        "id": user.id,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "email": user.email,
                        "location": user.location,
                        "phone": user.phone,
                        "role": user.role
                    }
                }
                data.append(request_data)

        return Response(data, status=200)


class TrackMeReview(APIView):
    permission_classes = (IsAdmin,)
    def post(self, request, pk):
        try:
            obj = TrackMeRequest.objects.get(id=pk)
        except TrackMeRequest.DoesNotExist:
            return Response({"error": "reqeust not found"}, status=404)
        if not obj.is_reviewed:
            obj.is_reviewed = True
            obj.save()
            return Response({"message": "review success"}, status=200)
        else:
            return Response({"error": "request already reviewed"}, status=400)
    def delete(self, request, pk):
        try:
            obj = TrackMeRequest.objects.get(id=pk)
        except TrackMeRequest.DoesNotExist:
            return Response({"error": "reqeust not found"}, status=404)
        if obj.is_reviewed:
            obj.is_reviewed = False
            obj.save()
            return Response({"message": "unreviewed!"}, status=200)
        else:
            return Response({"error": "request not reviewed"}, status=400)


class LocationCreateView(APIView):
    permission_classes = (IsAdmin,)
    def post(self, request):
        serializer = LocationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response({"message": "location created"}, status=200)
    
class GetAdminLocations(APIView):
    permission_classes = (IsAdmin,)
    def get(self, request):
        try:
            locations = StaffLocation.objects.filter(user=request.user.id, is_deleted=False)
        except StaffLocation.DoesNotExist:
            return Response({"error": "location not found"}, status=404)
        serializer = LocationSerializer(locations, many=True)
        data = {
            "locations": serializer.data
        }

        return Response(data, status=200)

class LocationActions(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAdmin,)
    queryset = StaffLocation.objects.filter(is_deleted=False)
    serializer_class = LocationSerializer

    def delete(self, request, pk):
        try:
            obj = StaffLocation.objects.get(id=pk)
        except StaffLocation.DoesNotExist:
            return Response({"error": "location object not found"}, status=404)
        if not obj.is_deleted:
            obj.is_deleted = True
            obj.save()
            return Response({"message": "success"}, status=200)

        else:
            return Response({"error": f"location {obj.id} is already deleted"}, status=400)

class ImageView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        serializer = ImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        status = "new image request"
        notification_handler(user=request.user, status=status)
        data = {
            "message": "image request successful"
            
        }
        return Response(data, status=200)


class GetImageRequestAdmin(APIView):
    permission_classes = (IsAdmin,)
 
    def get(self, request):
        users = User.objects.filter(user=request.user)
        data = []
        for user in users:
            image_requests = Images.objects.filter(user=user, is_deleted=False).order_by('-id')
            for image_request in image_requests:
                serializer = ImageSerializer(image_request)
                request_data = {
                    "id": serializer.data['id'],
                    "image": serializer.data['image'],
                    "description": serializer.data['description'],
                    "location": serializer.data['location'],
                    "is_reviewed": serializer.data['is_reviewed'],
                    "timestamp": serializer.data['timestamp'],
                    "user": {
                        "id": user.id,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "email": user.email,
                        "location": user.location,
                        "phone": user.phone,
                        "role": user.role
                    }
                }
                data.append(request_data)

        return Response(data, status=200)
    

class ImageActions(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAdmin,)
    queryset = Images.objects.filter(is_deleted=False)
    serializer_class = ImageSerializer

    def delete(self, request, pk):
        try:
            obj = Images.objects.get(id=pk)
        except Images.DoesNotExist:
            return Response({"error": "image object not found"}, status=404)
        if not obj.is_deleted:
            obj.is_deleted = True
            obj.save()
            return Response({"message": "success"}, status=200)

        else:
            return Response({"error": f"Image id {obj.id} is already deleted"}, status=400)
            

class GetAdminNotifications(APIView):
    permission_classes = (IsAdmin,)

    def get(self, request):
        users = User.objects.filter(user=request.user)
        data = []
        for user in users:
            notifications = Notifications.objects.filter(user=user, is_deleted=False).order_by('-id')
            for notification in notifications:
                serializer = NotificationSerializer(notification)

                data.append(serializer.data)
        return Response(data, status=200)


class NotifficationActions(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAdmin,)
    queryset = Notifications.objects.filter(is_deleted=False)
    serializer_class = NotificationSerializer

    def delete(self, request, pk):
        try:
            obj = Notifications.objects.get(id=pk)
        except Notifications.DoesNotExist:
            return Response({"error": "notification object not found"}, status=404)
        if not obj.is_deleted:
            obj.is_deleted = True
            obj.save()
            return Response({"message": "success"}, status=200)

        else:
            return Response({"error": "already deleted"}, status=400)
