from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from dashboard.models import NoiseAudioWeb


@login_required
def dashboard(request, slug="noise-orchestra-web"):
    data = get_object_or_404(NoiseAudioWeb, slug=slug)

    naw = {
        'name': data.name,
        'slug': data.slug,
        'about': data.about,
        'owner': data.owner,
        'jacktrip_hub_server': data.jacktrip_hub_server,
        'influxdb': data.influxdb,
        'stream_address': data.stream_address,
        'file_storage': data.file_storage,
    }

    return render(request, 'templates/vue/_vue_base_dashboard.html', {'data': {'naw': naw}})
