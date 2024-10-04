from django.shortcuts import render

# Create your views here.
import netCDF4 as nc
import xarray as xr
import numpy as np
import pandas as pd
from datetime import datetime
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import TemperatureDataSerializer, PrecipitationDataSerializer
from django.http import FileResponse, HttpResponse
import os

class TemperatureDataView(APIView):
    def get(self, request, format=None):
        # Obtener el parámetro del archivo de la URL
        file_param = request.query_params.get('file', 'default')

        # Mapeo de parámetros a rutas de archivo
        file_paths = {
            'default': 'datos/temperature_data_2024_2035_ssp126.nc',
            'ssp245': 'datos/temperature_data_2024_2035_ssp245.nc',
            'ssp370': 'datos/temperature_data_2024_2035_ssp370.nc',
        }

        # Seleccionar el archivo basado en el parámetro
        file_path = file_paths.get(file_param, file_paths['default'])

        # Verificar si se solicita una descarga
        #download_format = request.query_params.get('download')

        if request.GET.get('download') == 'nc':
            # Descargar el archivo NetCDF original
			#file_path = file_paths.get(file_param, file_paths['default'])
            return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
			
		#if download_format == 'nc':
            # Descargar el archivo NetCDF original
            #return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
		#if request.GET.get('download') == 'nc':
			#file_path = file_paths.get(file_param, file_paths['default'])
			#return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
		
        dataset = xr.open_dataset(file_path)

        tas = dataset['temperature']
        
        '''Crear rango de fecha omitiendo los días bisiestos'''
        f1 = '2024-01-01 03:00:00'
        f2 = '2034-12-29 03:00:00'
        fgregoriano = pd.date_range(f1, f2, freq='3h')
        fecha = fgregoriano[~((fgregoriano.month == 2) & (fgregoriano.day == 29))]

        tas['time'] = fecha

        # Horas disponibles
        available_hours = [0, 3, 6, 9, 12, 15, 18, 21]

        # Obtener la hora de la petición o usar la actual si no se proporciona
        requested_time = request.query_params.get('time', None)
        if requested_time:
            try:
                ''' Convertir y formatear la hora solicitada a "%Y-%m-%d %H:%M:%S" con minutos y segundos en 00'''
                #requested_time = pd.to_datetime(requested_time).strftime("%Y-%m-%d %H:00:00")
                
                ''' Convertir a datetime y extraer la hora '''
                requested_time = pd.to_datetime(requested_time)
                requested_hour = requested_time.hour

                # Encontrar la hora disponible más cercana
                closest_hour = min(available_hours, key=lambda x: abs(x - requested_hour))

                # Ajustar la hora de la solicitud al closest_hour
                requested_time = requested_time.replace(hour=closest_hour, minute=0, second=0, microsecond=0)

            except ValueError:
                return Response({"error": "Invalid time format. Use 'YYYY-MM-DD HH:MM:SS' format."}, status=400)
        else:
            ''' Convertir la hora actual a pandas.Timestamp con formato "%Y-%m-%d %H:00:00"'''
            ##requested_time = pd.to_datetime(datetime.now().strftime('%Y-%m-%d %H:00:00'))
            ##print('Hora 2:')
            ##print(requested_time)

            ''' Obtener la hora actual y redondear a la hora disponible más cercana '''
            current_time = datetime.now()
            current_hour = current_time.hour
            closest_hour = min(available_hours, key=lambda x: abs(x - current_hour))

            # Formatear la hora seleccionada
            requested_time = current_time.replace(hour=closest_hour, minute=0, second=0, microsecond=0).strftime('%Y-%m-%d %H:00:00')



       # Convertir la hora solicitada nuevamente a pandas.Timestamp para la selección
        requested_time = pd.to_datetime(requested_time)
        print('Hora 3:')
        print(requested_time)

        # Filtrar los datos por la hora solicitada
        try:
            temperatura_time = tas.sel(time=requested_time)
            print(temperatura_time)
        except KeyError:
            return Response({"error": f"No data available for the requested time: {requested_time}, use hour: 00, 03, 06, 09, 12, 15, 18, 21"}, status=404)
        except TypeError as e:
            return Response({"error": str(e)}, status=400)
        
        # Convertir la hora a un formato legible antes de devolverla en la respuesta
        time_formatted = pd.to_datetime(str(temperatura_time['time'].values)).strftime('%Y-%m-%d %H:%M:%S')

        time = time_formatted
        print(temperatura_time)
        lat = temperatura_time['lat'].values.tolist()
        lon = temperatura_time['lon'].values.tolist()
        temperature = temperatura_time.values.tolist()
        temperature = np.nan_to_num(temperature)

        # Aquí puedes estructurar los datos como prefieras
        data = {
            "time": time,
            "latitude": lat,
            "longitude": lon,
            #"temperature": temperature,
            "values": temperature,
        }

        serializer = TemperatureDataSerializer(data)
        #return Response(data)
        return Response(serializer.data)


'''CLASE PARA SERVIR DATOS DE PRECIPITACION'''

class PrecipitationDataView(APIView):
    def get(self, request, format=None):
        # Obtener el parámetro del archivo de la URL
        file_param = request.query_params.get('file', 'default')

        # Mapeo de parámetros a rutas de archivo
        file_paths = {
            'default': 'datos/pr_3hr_GFDL-ESM4_ssp126_r1i1p1f1_gr1_201501010130-203412312230_ssp126.nc',
            'ssp245': 'datos/pr_3hr_GFDL-ESM4_ssp126_r1i1p1f1_gr1_201501010130-203412312230_ssp245.nc',
            'ssp370': 'datos/pr_3hr_GFDL-ESM4_ssp126_r1i1p1f1_gr1_201501010130-203412312230_ssp370.nc',
        }

        # Seleccionar el archivo basado en el parámetro
        file_path = file_paths.get(file_param, file_paths['default'])

        # Verificar si se solicita una descarga
        #download_format = request.query_params.get('download')

        if request.GET.get('download') == 'nc':
            # Descargar el archivo NetCDF original
			#file_path = file_paths.get(file_param, file_paths['default'])
            return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
        
        dataset = xr.open_dataset(file_path)

        pr = dataset['pr']
        
        '''Crear rango de fecha omitiendo los días bisiestos'''
        f1 = '2015-01-01 03:00:00'
        f2 = '2035-01-01 00:00:00'
        fgregoriano = pd.date_range(f1, f2, freq='3h')
        fecha = fgregoriano[~((fgregoriano.month == 2) & (fgregoriano.day == 29))]

        pr['time'] = fecha

        # Horas disponibles
        available_hours = [0, 3, 6, 9, 12, 15, 18, 21]

        # Obtener la hora de la petición o usar la actual si no se proporciona
        requested_time = request.query_params.get('time', None)
        if requested_time:
            try:
                ''' Convertir y formatear la hora solicitada a "%Y-%m-%d %H:%M:%S" con minutos y segundos en 00'''
                #requested_time = pd.to_datetime(requested_time).strftime("%Y-%m-%d %H:00:00")
                
                ''' Convertir a datetime y extraer la hora '''
                requested_time = pd.to_datetime(requested_time)
                requested_hour = requested_time.hour

                # Encontrar la hora disponible más cercana
                closest_hour = min(available_hours, key=lambda x: abs(x - requested_hour))

                # Ajustar la hora de la solicitud al closest_hour
                requested_time = requested_time.replace(hour=closest_hour, minute=0, second=0, microsecond=0)

            except ValueError:
                return Response({"error": "Invalid time format. Use 'YYYY-MM-DD HH:MM:SS' format."}, status=400)
        else:
            ''' Convertir la hora actual a pandas.Timestamp con formato "%Y-%m-%d %H:00:00"'''
            ##requested_time = pd.to_datetime(datetime.now().strftime('%Y-%m-%d %H:00:00'))
            ##print('Hora 2:')
            ##print(requested_time)

            ''' Obtener la hora actual y redondear a la hora disponible más cercana '''
            current_time = datetime.now()
            current_hour = current_time.hour
            closest_hour = min(available_hours, key=lambda x: abs(x - current_hour))

            # Formatear la hora seleccionada
            requested_time = current_time.replace(hour=closest_hour, minute=0, second=0, microsecond=0).strftime('%Y-%m-%d %H:00:00')



       # Convertir la hora solicitada nuevamente a pandas.Timestamp para la selección
        requested_time = pd.to_datetime(requested_time)
        print('Hora 3:')
        print(requested_time)

        # Filtrar los datos por la hora solicitada
        try:
            precipitation_time = pr.sel(time=requested_time)
            print(precipitation_time)
        except KeyError:
            return Response({"error": f"No data available for the requested time: {requested_time}, use hour: 00, 03, 06, 09, 12, 15, 18, 21"}, status=404)
        except TypeError as e:
            return Response({"error": str(e)}, status=400)
        
        # Convertir la hora a un formato legible antes de devolverla en la respuesta
        time_formatted = pd.to_datetime(str(precipitation_time['time'].values)).strftime('%Y-%m-%d %H:%M:%S')

        time = time_formatted
        print(precipitation_time)
        lat = precipitation_time['lat'].values.tolist()
        lon = precipitation_time['lon'].values.tolist()
        precipitation = precipitation_time.values.tolist()
        precipitation = np.nan_to_num(precipitation, nan=-99)

        # Aquí puedes estructurar los datos como prefieras
        data = {
            "time": time,
            "latitude": lat,
            "longitude": lon,
            #"precipitation": precipitation,
            "values": precipitation
        }

        #return Response(data)
        serializer = PrecipitationDataSerializer(data)
        return Response(serializer.data)