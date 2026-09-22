from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET', 'POST']) # GET ist hier der default
def first_view(request):
    if request.method == 'GET':
        # Anstatt einen Json- oder HttpResponse haben wir in DRF einfach einen 'Response'
        return Response({"message": "Hello, world!"})
    
    if request.method == 'POST':
        try:
            msg = request.data['message']
            return Response({'your_message': msg}, status=status.HTTP_201_CREATED)
        
        except:
            return Response({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST)
        
