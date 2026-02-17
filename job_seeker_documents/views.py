from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import ApplicantDocument
from .serializers import JobSeekerDocumentSerializer

class CreateDocuments(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        files = request.FILES.getlist('files')  # <-- GET MULTIPLE FILES
        
        if not files:
            return Response({"error": "No files uploaded"}, status=400)

        saved_documents = []
        for file in files:
            doc = ApplicantDocument.objects.create(user=user, documents=file)
            saved_documents.append(doc)
        
        serializer = JobSeekerDocumentSerializer(saved_documents, many=True)
        return Response(serializer.data)
