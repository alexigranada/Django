from django.shortcuts import render
import xarray as xr
import numpy as np
import pandas as pd
from datetime import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import TemperatureDataSerializer, PrecipitationDataSerializer
from django.http import FileResponse
import os

class TemperatureDataView(APIView):
    def get(self, request, format=None):
        file_param = request.query_params.get('file', 'default')
        file_paths = {
            'default': 'datos/temperature_data_2024_2035_ssp126.nc',
            'ssp245': 'datos/temperature_data_2024_2035_ssp245.nc',
            'ssp370': 'datos/temperature_data_2024_2035_ssp370.nc',
        }
        file_path = file_paths.get(file_param, file_paths['default'])

        if request.GET.get('download') == 'nc':
            return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))

        dataset = xr.open_dataset(file_path)
        tas = dataset['temperature']

        requested_time = request.query_params.get('time', None)
        if requested_time:
            try:
                requested_time = pd.to_datetime(requested_time)
            except ValueError:
                return Response({"error": "Invalid time format. Use 'YYYY-MM-DD HH:MM:SS' format."}, status=400)
        else:
            requested_time = pd.to_datetime(datetime.now().replace(minute=0, second=0, microsecond=0))

        try:
            temperatura_time = tas.sel(time=requested_time, method='nearest')
        except KeyError:
            return Response({"error": f"No data available for the requested time: {requested_time}"}, status=404)
        except TypeError as e:
            return Response({"error": str(e)}, status=400)

        time_formatted = pd.to_datetime(str(temperatura_time['time'].values)).strftime('%Y-%m-%d %H:%M:%S')
        
        data = {
            "time": time_formatted,
            "latitude": temperatura_time['lat'].values.tolist(),
            "longitude": temperatura_time['lon'].values.tolist(),
            "values": np.nan_to_num(temperatura_time.values).tolist(),
        }

        serializer = TemperatureDataSerializer(data)
        return Response(serializer.data)

class PrecipitationDataView(APIView):
    def get(self, request, format=None):
        file_param = request.query_params.get('file', 'default')
        file_paths = {
            'default': 'datos/pr_3hr_GFDL-ESM4_ssp126_r1i1p1f1_gr1_201501010130-203412312230_ssp126.nc',
            'ssp245': 'datos/pr_1hr_GFDL-ESM4_ssp126_r1i1p1f1_gr1_201501010130-203412312230_ssp245.nc',
            'ssp370': 'datos/pr_1hr_GFDL-ESM4_ssp126_r1i1p1f1_gr1_201501010130-203412312230_ssp370.nc',
        }
        file_path = file_paths.get(file_param, file_paths['default'])

        if request.GET.get('download') == 'nc':
            return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))

        dataset = xr.open_dataset(file_path)
        pr = dataset['pr']

        requested_time = request.query_params.get('time', None)
        if requested_time:
            try:
                requested_time = pd.to_datetime(requested_time)
            except ValueError:
                return Response({"error": "Invalid time format. Use 'YYYY-MM-DD HH:MM:SS' format."}, status=400)
        else:
            requested_time = pd.to_datetime(datetime.now().replace(minute=0, second=0, microsecond=0))

        try:
            precipitation_time = pr.sel(time=requested_time, method='nearest')
        except KeyError:
            return Response({"error": f"No data available for the requested time: {requested_time}"}, status=404)
        except TypeError as e:
            return Response({"error": str(e)}, status=400)

        time_formatted = pd.to_datetime(str(precipitation_time['time'].values)).strftime('%Y-%m-%d %H:%M:%S')
        
        data = {
            "time": time_formatted,
            "latitude": precipitation_time['lat'].values.tolist(),
            "longitude": precipitation_time['lon'].values.tolist(),
            "values": np.nan_to_num(precipitation_time.values, nan=-99).tolist(),
        }

        serializer = PrecipitationDataSerializer(data)
        return Response(serializer.data)