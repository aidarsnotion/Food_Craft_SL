from django.contrib.auth.models import Group
from main.models import *
from django.contrib.auth import authenticate
from itertools import groupby
from collections import defaultdict


from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * username
      * password.
    It will try to authenticate the user with when validated.
    """
    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        # Take username and password from request
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']





"""   Сериализация данных для мобилки  """

class RegionSerializer(serializers.ModelSerializer):
    """   Регионы  """
    class Meta:
        model = Regions
        fields = ['id',
                  'region',
                  'language',]

class CategorySerializer(serializers.ModelSerializer):
    """   Категории продуктов  """
    Name_of_Region = serializers.CharField(source='Region.region')
    
    class Meta:
        model = Categories
        fields = ['id',
                  'Name_of_category',
                  'Name_of_Region',
                  'language']


class ProductsSerializer(serializers.ModelSerializer):
    """   Продукты питания  """
    category_name = serializers.CharField(source='Category.Name_of_category')
    Region = serializers.CharField(source='Category.Region.region')

    class Meta:
        model = Products
        fields = ['id', 
                  'attribute_name', 
                  'category_name', 
                  'Region',
                  'date_analis',]
        

class ChemicalsSerializer(serializers.ModelSerializer):
    """   Химический состав продуктов питания  """
    # product_id = serializers.SerializerMethodField()
    # product_name = serializers.SerializerMethodField()
    # language = serializers.SerializerMethodField()

    class Meta:
        model = Chemicals
        fields = [
                  'soluable_solids',
                  'ascorbic_acids',
                  'ash_content',
                  'moisture',
                  'protein',
                  'fat',
                  'carbohydrates',
                  ]
    
    # def get_product_id(self, obj):
    #     return obj.product.id if obj.product else None

    # def get_product_name(self, obj):
    #     return obj.product.attribute_name if obj.product else None

    # def get_language(self, obj):
    #     return obj.product.language if obj.product else None
        
class FatacidsTypesSerilizer(serializers.ModelSerializer):
    """   Вид жирнокислоты (Насыщенный, Мононенасыщенный)  """
    class Meta:
        model = FatAcidsType
        fields = ['id',
                  'name',]

class FatAcidsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FatAcids
        fields = ['id',
                  'name']
        
class FatacidCompositionSerializer(serializers.ModelSerializer):
    """   Жирнокислотный состав продуктов питания  """
    # product_id = serializers.IntegerField(source='product.id')
    # product_name = serializers.CharField(source='product.attribute_name')
    # language = serializers.CharField(source='product.language')
    fat_acid_types = serializers.CharField(source='types.name')
    lipid_name = serializers.CharField(source='fat_acid.name')

    class Meta:
        model = FatAcidCompositionOfMeal
        fields = [
                  'fat_acid_types',
                  'lipid_name',
                  'value',
                  ]


#Здесь повторяются записи, но модельки организованы правильно
# class FatAcidsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FatAcids
#         fields = ['name']

# class FatAcidCompositionSerializer(serializers.ModelSerializer):
#     fat_acid = FatAcidsSerializer()

#     class Meta:
#         model = FatAcidCompositionOfMeal
#         fields = ['fat_acid', 'value']

# class FatAcidsTypeSerializer(serializers.ModelSerializer):
#     fat_acids = serializers.SerializerMethodField()

#     class Meta:
#         model = FatAcidsType
#         fields = ['fat_acids']

#     def get_fat_acids(self, obj):
#         compositions = FatAcidCompositionOfMeal.objects.filter(types=obj.types, product=obj.product).order_by('fat_acid__name')
#         fat_acids_data = {}
#         for composition in compositions:
#             fat_acids_data.setdefault(composition.types.name, []).append({
#                 'lipid_name': composition.fat_acid.name,
#                 'value': composition.value
#             })

#         grouped_data = []
#         for fat_acid_type, fat_acids in fat_acids_data.items():
#             # Проверяем, был ли уже добавлен тип жирных кислот
#             if not any(data['types'] == fat_acid_type for data in grouped_data):
#                 grouped_data.append({
#                     'types': fat_acid_type,
#                     'fat_acids': fat_acids
#                 })

#         return grouped_data



class AminoAcidCompositionSerializer(serializers.ModelSerializer):
    """   Аминокислотный состав продуктов питания  """
    # product_id = serializers.IntegerField(source='product.id')
    # product_name = serializers.CharField(source='product.attribute_name')
    # language = serializers.CharField(source='product.language')

    class Meta:
        model = AminoAcidComposition
        fields = [
                  'asparing',
                  'glutamin',
                  'serin',
                  'gistidin',
                  'glitsin',
                  'treonin',
                  'arginin',
                  'alanin',
                  'tirosin',
                  'tsistein',
                  'valin',
                  'metionin',
                  'triptofan',
                  'fenilalalin',
                  'izoleitsin',
                  'leitsin',
                  'lisin',
                  'prolin',
                  ]
                  
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Проверяем, все ли значения равны
        if all(value is None or value == '' or value == 0 for value in data.values()):
            return None
        return data
        
class MineralCompositionSerializer(serializers.ModelSerializer):
    """   Минеральный состав продуктов питания  """
    # product_id = serializers.IntegerField(source='product.id')
    # product_name = serializers.CharField(source='product.attribute_name')
    # language = serializers.CharField(source='product.language')

    class Meta:
        model = MineralComposition
        fields = [
                  'Ca',
                  'Na',
                  'K',
                  'P',
                  'Mn',
                  'Zn',
                  'Se',
                  'Cu',
                  'Fe',
                  'I',
                  'B',
                  'Li',
                  'Al',
                  'Mg',
                  'V',
                  'Ni',
                  'Co',
                  'Cr',
                  'Sn',
                  ]


        
class ProcessRecipeSerializer(serializers.Serializer):
    recip_name = serializers.CharField()
    reg = serializers.ListField(child=serializers.CharField())
    ingredient = serializers.ListField(child=serializers.CharField())
    mass_fraction = serializers.ListField(child=serializers.FloatField())
    price = serializers.ListField(child=serializers.FloatField())


class CalculationResultsSerializer(serializers.Serializer):
    protein = serializers.FloatField()
    fatacid = serializers.FloatField()
    carbohydrates = serializers.FloatField()
    price_100 = serializers.FloatField()
    price_1kg = serializers.FloatField()
    isol = serializers.FloatField()
    leit = serializers.FloatField()
    val = serializers.FloatField()
    met_tsist1 = serializers.FloatField()
    fenilalalin_tirosin1 = serializers.FloatField()
    tripto = serializers.FloatField()
    lis = serializers.FloatField()
    treon = serializers.FloatField()
    isolecin2 = serializers.FloatField()
    leitsin2 = serializers.FloatField()
    valin2 = serializers.FloatField()
    met_tsist3 = serializers.FloatField()
    fenilalalin_tirosin3 = serializers.FloatField()
    triptofan2 = serializers.FloatField()
    lisin2 = serializers.FloatField()
    treonin2 = serializers.FloatField()
    isolecin_a = serializers.FloatField()
    leitsin_a = serializers.FloatField()
    valin_a = serializers.FloatField()
    met_tsist_a = serializers.FloatField()
    fenilalalin_tirosin_a = serializers.FloatField()
    triptofan_a = serializers.FloatField()
    lisin_a = serializers.FloatField()
    treonin_a = serializers.FloatField()
    Cmin = serializers.FloatField()
    power_kkal = serializers.FloatField()
    power_kDj = serializers.FloatField()
    kras = serializers.FloatField()
    bc = serializers.FloatField()
    U = serializers.FloatField()
    G = serializers.FloatField()
    my_time = serializers.FloatField()
    chart_kras = serializers.CharField()
    chart_bc = serializers.CharField()
    chart_U = serializers.CharField()
    chart_G = serializers.CharField()


class DetailedProductSerializer(serializers.ModelSerializer):
    chemicals = ChemicalsSerializer(many=True, read_only=True)
    aminoacids = AminoAcidCompositionSerializer(many=True, read_only=True)
    minerals = MineralCompositionSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='Category.Name_of_category')
    Region = serializers.CharField(source='Category.Region.region')

    class Meta:
        model = Products
        fields = ['id', 
                  'attribute_name', 
                  'category_name', 
                  'Region',
                  'date_analis',
                  'chemicals',
                  'aminoacids',
                  'minerals',
                  ]
