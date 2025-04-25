from rest_framework import serializers
from .models import Report, Image

class ReportSerializer(serializers.ModelSerializer):
    image_file = serializers.ImageField(write_only=True, required=True)

    class Meta:
        model = Report
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'image')

    def create(self, validated_data):
        image_file = validated_data.pop("image_file")

        image_instance = Image.objects.create(
            image_file=image_file,
            file_format=image_file.name.split('.')[-1].upper(),
            file_size_kb=round(image_file.size / 1024)
        )

        report = Report.objects.create(
            image=image_instance,
            **validated_data
        )
        return report