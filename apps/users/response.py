from rest_framework.response import Response
from rest_framework import status

def system_error(error_message=None):
    """
        Returns System Error JsonResponse
    """
    if not error_message:
        error_message = "Some error occurred (Please try again after sometime)"
    response_data = {'status': 'Failure','message': error_message }
    return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def bad_request_error(error_message=None):
    """
        Returns Bad Request JsonResponse
    """
    if not error_message:
        error_message = 'Something wrong with request format, Please check request body..'
    response_data = {
        'status': 'Failure',
        'message': error_message,
    }
    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


def heath_success():
    """
        Returns health success
    """
    response_data = {'status': 'Success', 'message': 'Server is running'}
    return Response(response_data, status=status.HTTP_200_OK)

def success():
    """
        Returns API success
    """
    response_data = {
        'status': 'Success',
        'message': 'Signup successful!',
    }
    return Response(response_data, status=status.HTTP_201_CREATED)
