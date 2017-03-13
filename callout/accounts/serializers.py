from rest_framework import serializers
from accounts.models import User as UserModel

#Create ModelSerializer classes

class RegisterSerializer(serializers.ModelSerializer):

    def create(self, data):
        user = UserModel(
            email=data['email'],
        )
        user.set_password(data['password'])
        user.save()
        return user
    
    date_of_birth = serializers.DateField(format=None, required=True)
    
    class Meta:
        model = UserModel
        fields = ('email', 'password', 'first_name', 'last_name', 'date_of_birth')
        readonly_fields = ()

class UserIDSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ('user_id',)
        
class UserSerializer(serializers.ModelSerializer):
    """ Get the image url of the user's profile picture """
    """ image_url = serializers.HyperlinkedIdentityField(view_name='<modelname>-detail') """
    display_picture = serializers.StringRelatedField(many=False)
    class Meta:
        model = UserModel
        fields = ('user_id', 'first_name', 'middle_name', 'last_name', 'display_picture')


class EditUserSerializer(serializers.ModelSerializer):
    """ get data to be changed, fields that are not being changed should be blank. field being changed to blank should be null """

    date_of_birth = serializers.DateField(format="%d-%m-%Y")
    
    class Meta:
        model = UserModel
        fields = ('first_name', 'middle_name', 'last_name', 'date_of_birth', 'cell_number', 'country')


class ExtendedUserSerializer(serializers.ModelSerializer):
    """ Get the image url of the user's profile picture """
    """ image_url = serializers.HyperlinkedIdentityField(view_name='<modelname>-detail') """
    """ num_followers = perform count of user in friends table """
    date_of_birth = serializers.DateField(format="%d-%m-%Y", required=True)
    
    class Meta:
        model = UserModel
        fields = fields = ('user_id', 'first_name', 'middle_name', 'last_name', 'date_of_birth', 'cell_number', 'country', 'won', 'drew', 'lost')

