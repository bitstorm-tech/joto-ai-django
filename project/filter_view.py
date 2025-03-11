from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
import os
import uuid

from project import filters


class FilterView(View):
    def get(self, request):
        context = {'uploaded_image': request.session.get('uploaded_image')}
        return render(request, 'index.html', context)

    def post(self, request):
        if 'image' in request.FILES:
            image = request.FILES['image']
            file_uuid = f"{uuid.uuid4()}"
            filename = f"{file_uuid}@{image.name}"
            filename_filtered = f"{file_uuid}-filtered@{image.name}"

            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

            file_path = os.path.join(settings.MEDIA_ROOT, filename)
            with open(file_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            file_path_filtered = os.path.join(
                settings.MEDIA_ROOT, filename_filtered)
            filters.pencil_sketch(file_path, file_path_filtered)

            return redirect(f"{settings.MEDIA_URL}{filename_filtered}")

        return redirect('home')
