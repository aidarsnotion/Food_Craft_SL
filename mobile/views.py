from main.models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.core.exceptions import ObjectDoesNotExist
from collections import namedtuple
from django.db.models import Q
from main.calculation import process_recipe
from django.http import Http404
from rest_framework.permissions import AllowAny
from mobile.serializers import *  
from .models import APIKey
from main.forms import UserPasswordResetForm
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend



def filter_data(queryset, filter_d, ordering_field=None, request=None):
    """
    Функция для динамической фильтрации и сортировки
    """
    try:
        # Создаем объект Q для динамической фильтрации
        and_conditions = Q()
        
        # Перебираем все атрибуты и значения и строим условия фильтрации
        for key, value in filter_d._asdict().items():
            if value is not None:  # Проверяем, что значение не равно None
                and_conditions &= Q(**{key:value}) #создание логического "И" (AND) для фильтрации
        
        # Применяем фильтр к queryset
        queryset = queryset.filter(and_conditions)
        
        # Применяем сортировку
        if ordering_field:
            queryset = queryset.order_by(ordering_field)
        
    except ObjectDoesNotExist:
        error_message = "Error: One or more filter values do not exist"
        print(error_message)
        queryset = queryset.model.objects.all()
    
    return queryset


def filter_data_product(queryset, filter_d, ordering_field=None, category_name=None, region_name=None):
    """
    Функция для динамической фильтрации и сортировки
    """
    try:
        # Создаем объект Q для динамической фильтрации
        and_conditions = Q()

        categories_list = [category.strip() for category in category_name.split('"') if category.strip()] if category_name else []
        regions_list = [region.strip() for region in region_name.split('"') if region.strip()] if region_name else []

        # Добавляем условия фильтрации по категориям, если они указаны
        if categories_list:
            # Создаем объект Q для фильтрации категорий
            category_conditions = Q()
            for category in categories_list:
                category_conditions |= Q(Category__Name_of_category=category)  # Удаляем лишние пробелы
            and_conditions &= category_conditions

        # Добавляем условия фильтрации по регионам, если они указаны
        if regions_list:
            # Создаем объект Q для фильтрации регионов
            region_conditions = Q()
            for region in regions_list:
                region_conditions |= Q(Category__Region__region=region.strip())  # Удаляем лишние пробелы
            and_conditions &= region_conditions

        # Перебираем все атрибуты и значения и строим условия фильтрации
        for key, value in filter_d._asdict().items():
            if value is not None:  # Проверяем, что значение не равно None
                and_conditions &= Q(**{key:value}) #создание логического "И" (AND) для фильтрации
        
        # Применяем фильтр к queryset
        queryset = queryset.filter(and_conditions)
        
        # Применяем сортировку
        if ordering_field:
            queryset = queryset.order_by(ordering_field)
        
    except ObjectDoesNotExist:
        error_message = "Error: One or more filter values do not exist"
        print(error_message)
        queryset = queryset.model.objects.all()
    
    return queryset




def filter_data_region(queryset, filter_d, request=None):
    """
    Функция для динамической фильтрации и сортировки
    """
    try:
        # Создаем объект Q для динамической фильтрации
        and_conditions = Q()
        
        # Перебираем все атрибуты и значения и строим условия фильтрации
        for key, value in filter_d._asdict().items():
            if value is not None:  # Проверяем, что значение не равно None
                and_conditions &= Q(**{key:value}) #создание логического "И" (AND) для фильтрации
        
        # Применяем фильтр к queryset
        queryset = queryset.filter(and_conditions)
        
    except ObjectDoesNotExist:
        error_message = "Error: One or more filter values do not exist"
        print(error_message)
        queryset = queryset.model.objects.all()
    
    return queryset

    

class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class LoginAPIView(APIView):
    serializer_class = LoginUserSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=LoginUserSerializer,
        responses={
            200: CalculationResultsSerializer,
            400: "Error message"
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        # Получаем данные запроса
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')

            # Проверяем, что оба поля заполнены
            if not username or not password:
                return Response({'error': 'Both username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

            # Аутентификация пользователя
            user = authenticate(username=username, password=password)

            # Проверяем успешность аутентификации
            if user is None:
                return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

            # Проверяем, существует ли API ключ для данного пользователя
            api_key, created = APIKey.objects.get_or_create(user=user)
            print("API Key created:", api_key.key)
            print("Authenticated user:", user)
            #APIKey.objects.all().delete()
            # Возвращаем успешный ответ с данными пользователя и API ключом
            return Response({'username': user.username, 'api_key': api_key.key}, status=status.HTTP_200_OK)


class Regions_APIView(APIView):
    """
    API получение регионов
    """
    serializer_class = RegionSrializer
    queryset = Regions.objects.all()
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
        )},
        manual_parameters=[
            openapi.Parameter('language', openapi.IN_QUERY, description="Язык", type=openapi.TYPE_STRING),
        ]
    )

    def get(self, request, *args, **kwargs):
        language = request.query_params.get('language')

        fil_data = namedtuple('filter_data', 'language')
        fl_data = fil_data(language)

        queryset = filter_data_region(self.queryset, fl_data, request)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class Categories_APIView(APIView):
    """
    API получение категории
    """
    serializer_class = CategorySerializer
    queryset = Categories.objects.all()
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
        )},
        manual_parameters=[
            openapi.Parameter('language', openapi.IN_QUERY, description="Язык", type=openapi.TYPE_STRING),
        ]
    )

    def get(self, request, *args, **kwargs):
        language = request.query_params.get('language')

        fil_data = namedtuple('filter_data', 'language')
        fl_data = fil_data(language)
        queryset = None
        queryset = filter_data(self.queryset, fl_data, queryset, request)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class ProductSearchAPIView(APIView):
    """
    API Поиск продукта по названию
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
        )},
        manual_parameters=[
            openapi.Parameter('attribute_name', openapi.IN_QUERY, description="Наименование продукта", type=openapi.TYPE_STRING),
        ]
    )

    def get(self, request, format=None):
        try:
            attribute_name = request.query_params.get('attribute_name', None)

            queryset = Products.objects.all()
            
            if attribute_name:
                queryset = queryset.filter(attribute_name__icontains=attribute_name)

            serializer = ProductsSerializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        


class ProductDetail_APIView(APIView):
    """
    API Детальной информации о продукте питания
    """
    queryset = Products.objects.all()
    serializer_class = DetailedProductSerializer
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination

    @swagger_auto_schema(
        responses={200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
        )},
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_QUERY, description="ID продукта", type=openapi.TYPE_INTEGER),
        ]
    )
        
    def get(self, request, *args, **kwargs):
        product_id = request.query_params.get('id')
        
        fil_data = namedtuple('filter_data', 'id')
        fl_data = fil_data(product_id)

        queryset = filter_data_region(self.queryset, fl_data, request)

        # Получаем все записи FatAcidCompositionOfMeal для указанного продукта
        fatacidcomps = FatAcidCompositionOfMeal.objects.filter(product_id=fl_data)
        
        # Создаем словарь для хранения сгруппированных данных
        grouped_data = defaultdict(list)
        
        # Группируем записи по типам жирных кислот
        for fatacidcomp in fatacidcomps:
            grouped_data[fatacidcomp.types.name].append({
                'lipid_name': fatacidcomp.fat_acid.name,
                'value': fatacidcomp.value
            })
        
        # Проверяем, все ли значения value равны 0
        all_zero = all(comp['value'] == 0 for comps in grouped_data.values() for comp in comps)

        # Если все значения равны 0, устанавливаем fatacid_ser равным None
        if all_zero:
            fatacid_ser = None
        else:
            # Проходим по сгруппированным данным и добавляем их в основной словарь
            fatacid_ser = {}
            for types, data in grouped_data.items():
                fatacid_ser[types] = data
                
        serializer = self.serializer_class(queryset, many=True)

        response_data = {'data': serializer.data, 'fatacid': fatacid_ser}

        return Response(response_data)
    


class ProductsList_APIViewSet(APIView):
    """
    API для продуктов питания - пример "Мясной""Овощи, Фрукты" или "Иссыкк-кульская область""Чуйская область"
    """
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination
    
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['language', 'Category__Name_of_category', 'Category__Region__region']
    ordering_fields = ['attribute_name', 'date_analis', '-attribute_name', '-date_analis']

    @swagger_auto_schema(
        responses={200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'attribute_name': openapi.Schema(type=openapi.TYPE_STRING),
                'Category': openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'name': openapi.Schema(type=openapi.TYPE_STRING),
                }),
                'date_analis': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                'language': openapi.Schema(type=openapi.TYPE_STRING),
            }
        )},
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_QUERY, description="ID продукта", type=openapi.TYPE_INTEGER),
            openapi.Parameter('language', openapi.IN_QUERY, description="Язык продукта", type=openapi.TYPE_STRING),
            openapi.Parameter('page', openapi.IN_QUERY, description="Номер страницы", type=openapi.TYPE_STRING),
            openapi.Parameter('Category__Name_of_category', openapi.IN_QUERY, description="Наименование категории Пример: Мясной", type=openapi.TYPE_STRING),
            openapi.Parameter('Category__Region__region', openapi.IN_QUERY, description="Наименование региона Пример: Иссык-кульская область", type=openapi.TYPE_STRING),
            openapi.Parameter('ordering', openapi.IN_QUERY, description="Поля для сортировки ('attribute_name', 'date_analis', '-attribute_name' это сортировка по убыванию)", type=openapi.TYPE_STRING),
        ]
    )

    def get(self, request, *args, **kwargs):
        product_id = request.query_params.get('id')
        language = request.query_params.get('language')
        category_name = request.query_params.get('Category__Name_of_category')
        region_name = request.query_params.get('Category__Region__region')
        ordering = request.query_params.get('ordering', None)

        if ordering not in self.ordering_fields:
            ordering = None

        fil_data = namedtuple('filter_data', 'id language')
        fl_data = fil_data(product_id, language)

        queryset = filter_data_product(self.queryset, fl_data, ordering, category_name, region_name)

        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        serializer = self.serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)


class Chemicals_APIView(APIView):
    """
    API для Химического состава продуктов питания
    """
    queryset = Chemicals.objects.all()
    serializer_class = ChemicalsSerializer
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination

    @swagger_auto_schema(
        responses={200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'product': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'attribute_name': openapi.Schema(type=openapi.TYPE_STRING),
                        'Category': openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'Name_of_category': openapi.Schema(type=openapi.TYPE_STRING),
                        }),
                        'date_analis': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                        'language': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                ),
                'soluable_solids': openapi.Schema(type=openapi.TYPE_NUMBER),
                'ascorbic_acids': openapi.Schema(type=openapi.TYPE_NUMBER),
                'ash_content': openapi.Schema(type=openapi.TYPE_NUMBER),
                'moisture': openapi.Schema(type=openapi.TYPE_NUMBER),
                'protein': openapi.Schema(type=openapi.TYPE_NUMBER),
                'fat': openapi.Schema(type=openapi.TYPE_NUMBER),
                'carbohydrates': openapi.Schema(type=openapi.TYPE_NUMBER),
            }
        )},
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_QUERY, description="ID химического состава ", type=openapi.TYPE_INTEGER),
            openapi.Parameter('product_id', openapi.IN_QUERY, description="ID продукта", type=openapi.TYPE_INTEGER),
            openapi.Parameter('language', openapi.IN_QUERY, description="Язык продукта", type=openapi.TYPE_STRING),
            openapi.Parameter('page', openapi.IN_QUERY, description="Номер страницы", type=openapi.TYPE_STRING),
        ]
    )

    def get(self, request, *args, **kwargs):
        chemical_id = request.query_params.get('id')
        product_id = request.query_params.get('product_id')
        language = request.query_params.get('language')

        fil_data = namedtuple('filter_data', 'id product product__language')
        fl_data = fil_data(chemical_id, product_id, language)

        queryset = filter_data(self.queryset, fl_data, request)

        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        serializer = self.serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)


class Fatacids_APIView(APIView):
    """
    API для Жирнокислотного состава продуктов питания
    """
    queryset = FatAcidCompositionOfMeal.objects.all()

    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination

    @swagger_auto_schema(
        responses = {
                200: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'product': openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'attribute_name': openapi.Schema(type=openapi.TYPE_STRING),
                                    'Category': openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                        'Name_of_category': openapi.Schema(type=openapi.TYPE_STRING),
                                    }),
                                    'date_analis': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                                    'language': openapi.Schema(type=openapi.TYPE_STRING),
                                }
                            ),
                        'types': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'fat_acid': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'value': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'language': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                )},
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_QUERY, description="ID химического состава ", type=openapi.TYPE_INTEGER),
            openapi.Parameter('product_id', openapi.IN_QUERY, description="ID продукта", type=openapi.TYPE_INTEGER),
            openapi.Parameter('language', openapi.IN_QUERY, description="Язык продукта", type=openapi.TYPE_STRING),
            openapi.Parameter('page', openapi.IN_QUERY, description="Номер страницы", type=openapi.TYPE_STRING),
        ]
    )

    def get(self, request, *args, **kwargs):
        fatacid_id = request.query_params.get('id')
        product_id = request.query_params.get('product_id')
        language = request.query_params.get('language')

        fil_data = namedtuple('filter_data', 'id product product__language')
        fl_data = fil_data(fatacid_id, product_id, language)

        queryset = filter_data(self.queryset, fl_data, request)

        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        serializer = self.serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)


class Aminoacid_APIView(APIView):
    """
    API для Аминокислотного состава продуктов питания
    """
    queryset = AminoAcidComposition.objects.all()
    serializer_class = AminoAcidCompositionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination

    @swagger_auto_schema(
        responses = {
                200: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'product': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'attribute_name': openapi.Schema(type=openapi.TYPE_STRING),
                                'Category': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                        'Name_of_category': openapi.Schema(type=openapi.TYPE_STRING),
                                    },
                                ),
                                'date_analis': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                                'language': openapi.Schema(type=openapi.TYPE_STRING),
                            },
                        ),
                        'types': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'fat_acid': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'value': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'language': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                )},
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_QUERY, description="ID химического состава ", type=openapi.TYPE_INTEGER),
            openapi.Parameter('product_id', openapi.IN_QUERY, description="ID продукта", type=openapi.TYPE_INTEGER),
            openapi.Parameter('language', openapi.IN_QUERY, description="Язык продукта", type=openapi.TYPE_STRING),
            openapi.Parameter('page', openapi.IN_QUERY, description="Номер страницы", type=openapi.TYPE_STRING),
        ]
    )

    def get(self, request, *args, **kwargs):
        fatacid_id = request.query_params.get('id')
        product_id = request.query_params.get('product_id')
        language = request.query_params.get('language')

        fil_data = namedtuple('filter_data', 'id product product__language')
        fl_data = fil_data(fatacid_id, product_id, language)

        queryset = filter_data(self.queryset, fl_data, request)

        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        serializer = self.serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)



class Minerals_APIView(APIView):
    """
    API для Минерального состава продуктов питания
    """
    queryset = MineralComposition.objects.all()
    serializer_class = MineralCompositionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination

    @swagger_auto_schema(
        responses = {
                200: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'product': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'attribute_name': openapi.Schema(type=openapi.TYPE_STRING),
                                'Category': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                        'Name_of_category': openapi.Schema(type=openapi.TYPE_STRING),
                                    },
                                ),
                                'date_analis': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                                'language': openapi.Schema(type=openapi.TYPE_STRING),
                            },
                        ),
                        'Ca': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'Na': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'K': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'P': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'Mn': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'Zn': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'Se': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'Cu': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'Fe': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'I': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'B': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'Li': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'Al': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'Mg': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'V': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'Ni': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'Co': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'Cr': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'Sn': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'language': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                )},
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_QUERY, description="ID химического состава ", type=openapi.TYPE_INTEGER),
            openapi.Parameter('product_id', openapi.IN_QUERY, description="ID продукта", type=openapi.TYPE_INTEGER),
            openapi.Parameter('language', openapi.IN_QUERY, description="Язык продукта", type=openapi.TYPE_STRING),
            openapi.Parameter('page', openapi.IN_QUERY, description="Номер страницы", type=openapi.TYPE_STRING),
        ]
    )

    def get(self, request, *args, **kwargs):
        fatacid_id = request.query_params.get('id')
        product_id = request.query_params.get('product_id')
        language = request.query_params.get('language')

        fil_data = namedtuple('filter_data', 'id product product__language')
        fl_data = fil_data(fatacid_id, product_id, language)

        queryset = filter_data(self.queryset, fl_data, request)

        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        serializer = self.serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)
    
class ProcessRecipeSerializer(serializers.Serializer):
    recip_name = serializers.CharField()
    reg = serializers.ListField(child=serializers.CharField())
    ingredient = serializers.ListField(child=serializers.CharField())
    mass_fraction = serializers.ListField(child=serializers.FloatField())
    price = serializers.ListField(child=serializers.FloatField())


class ProcessRecipeAPIView(APIView):
    #authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=ProcessRecipeSerializer,
        responses={
            200: CalculationResultsSerializer,
            400: "Error message"
        },
    )
    def post(self, request):
        print(request.data)
        serializer = ProcessRecipeSerializer(data=request.data)
        if serializer.is_valid():
            recip_name = serializer.data.get('recip_name')
            reg = serializer.data.get('reg')
            ingredient = serializer.data.get('ingredient')
            mass_fraction = serializer.data.get('mass_fraction')
            price = serializer.data.get('price')
            size = len(ingredient)

            calculation_results = process_recipe(recip_name, reg, ingredient, mass_fraction, price, size)

            if isinstance(calculation_results, list):
                return Response({'error': calculation_results[0]}, status=400)
            elif calculation_results.error_flag != 0:
                return Response({'error': calculation_results.error_flag}, status=400)

            serializer_results = CalculationResultsSerializer(calculation_results)

            return Response(serializer_results.data, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductsRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['id', 'attribute_name', 'Category', 'date_analis', 'language']


class LoadProductsFromRegionAPIView(APIView):
    """
    Получение списка продуктов из указанного региона.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={
            200: ProductsRegionSerializer,
            400: "Error message"
        },
        manual_parameters=[
            openapi.Parameter('region', openapi.IN_QUERY, description="Регион для получения продукта", type=openapi.TYPE_INTEGER),
        ]
    )
    def get(self, request, *args, **kwargs):
        # Получаем значение параметра region из запроса
        region = request.query_params.get('region')

        # Проверяем, что параметр region был передан
        if not region:
            return Response({'error': 'The region parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Фильтруем продукты по указанному региону
        products = Products.objects.filter(Category__Region__pk=region)

        # Проверяем, что найдены продукты для указанного региона
        if not products.exists():
            return Response({'message': 'No products found for the specified region'}, status=status.HTTP_200_OK)

        # Сериализуем найденные продукты и отправляем в ответе
        serializer = ProductsRegionSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LoadProductsByCategoryAPIView(APIView):
    """
    Получение списка продуктов по категории.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={
            200: ProductsRegionSerializer,
            400: "Error message"
        },
        manual_parameters=[
            openapi.Parameter('Category__Name_of_category', openapi.IN_QUERY, description="Категория для получения продуктов", type=openapi.TYPE_STRING),
        ]
    )
    def get(self, request, *args, **kwargs):
        # Получаем значение параметра region из запроса
        cateogry = request.query_params.get('Category__Name_of_category')

        # Проверяем, что параметр region был передан
        if not cateogry:
            return Response({'error': 'The cateogry parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Фильтруем продукты по указанному региону
        products = Products.objects.filter(Category__Name_of_category=cateogry)

        # Проверяем, что найдены продукты для указанного региона
        if not products.exists():
            return Response({'message': 'No products found for the specified cateogry'}, status=status.HTTP_200_OK)

        # Сериализуем найденные продукты и отправляем в ответе
        serializer = ProductsRegionSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PasswordResetRequestAPIView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        responses={
            200: "Success",
            400: "Error: Invalid email or header"
        }
    )
    def post(self, request):
        password_reset_form = UserPasswordResetForm(request.data)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = CustomUser.objects.filter(email=data)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Запрос на сброс данных"
                    email_template_name = "admin_templates/pages/user/password_reset_email.html"
                    c = {
                        "email": user.email,
                        'domain': 'http://127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'csmbishkek@gmail.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return Response({'error': 'Invalid header found.'}, status=status.HTTP_400_BAD_REQUEST)
                    return Response({'success': 'Password reset link has been sent to your email.'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid email.'}, status=status.HTTP_400_BAD_REQUEST)
