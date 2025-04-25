from rest_framework import serializers
from .models import Report, Image
import json

class ReportSerializer(serializers.ModelSerializer):
    image_file = serializers.ImageField(write_only=True, required=True)

    class Meta:
        model = Report
        fields = '__all__'
        read_only_fields = (
            'id',
            'created_at',
            'image',
            'user',
        )  

    def create(self, validated_data):
        print("\n Raw validated_data received:")
        def repr_safely(val):
            try:
                return repr(val)
            except Exception as e:
                return f"<Unprintable object: {e}>"

        for key, value in validated_data.items():
            print(f"  {key}: {repr_safely(value)}")


        # Ensure user is not duplicated
        validated_data.pop("user", None)

        # Parse diagnostic_probabilities safely
        diagnostic_probs = validated_data.get("diagnostic_probabilities")
        if isinstance(diagnostic_probs, str):
            try:
                diagnostic_probs = json.loads(diagnostic_probs)
                validated_data["diagnostic_probabilities"] = diagnostic_probs
            except json.JSONDecodeError:
                raise serializers.ValidationError({
                    "diagnostic_probabilities": "Invalid JSON format."
                })

        # Fail-safe: prevent missing field
        if "diagnostic_probabilities" not in validated_data:
            raise serializers.ValidationError({
                "diagnostic_probabilities": "This field is required."
            })
        

        image_file = validated_data.pop("image_file")

        image_instance = Image.objects.create(
            image_file=image_file,
            file_format=image_file.name.split('.')[-1].upper(),
            file_size_kb=round(image_file.size / 1024)
        )

        report = Report.objects.create(
            image=image_instance,
            user=self.context['request'].user,
            **validated_data
        )
        return report