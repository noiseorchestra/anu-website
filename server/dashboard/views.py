from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from dashboard.models import NoiseAudioWeb
from rest_framework import views
from django.views.decorators.csrf import csrf_exempt
from dashboard.serializers import Recordings, RecordingSerializer
import os
import boto3
from django.http import HttpResponse, JsonResponse

SPACES_BASE_URL = "https://pypatcher-recordings.fra1.digitaloceanspaces.com"

session = boto3.session.Session()
client = session.client('s3',
                        region_name='fra1',
                        endpoint_url='https://fra1.digitaloceanspaces.com',
                        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

def get_recording_url(file_path):
    return SPACES_BASE_URL + "/" + file_path

@login_required
def dashboard(request, slug="noise-orchestra-web"):
    data = get_object_or_404(NoiseAudioWeb, slug=slug)

    nawData = {
        'name': data.name,
        'slug': data.slug,
        'about': data.about,
        'owner': data.owner,
        'jacktrip_hub_server': data.jacktrip_hub_server,
        'influxdb': data.influxdb,
        'stream_address': data.stream_address,
        'file_storage': data.file_storage,
    }

    return render(request, 'dashboard/dashboard.html', {'data': nawData})


@csrf_exempt
def recordings_list(request):
    if request.method == 'GET':
        response = client.list_objects(Bucket='pypatcher-recordings')
        urls = [get_recording_url(obj['Key']) for obj in response['Contents']]
        serializer = RecordingSerializer(Recordings(urls))
        return JsonResponse(serializer.data, safe=False)
