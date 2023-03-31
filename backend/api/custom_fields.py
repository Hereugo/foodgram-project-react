# https://github.com/Hipo/drf-extra-fields/blob/master/drf_extra_fields/fields.py

import base64
import binascii
import imghdr
import io
import uuid

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.fields import ImageField


class Base64FieldMixin:
    EMPTY_VALUES = (None, '', [], (), {})

    @property
    def allowed_types(self):
        raise NotImplementedError

    @property
    def invalid_file_message(self):
        raise NotImplementedError

    @property
    def invalid_type_message(self):
        raise NotImplementedError

    def __init__(self, *args, **kwargs):
        self.trust_provided_content_type = kwargs.pop(
            'trust_provided_content_type',
            False
        )
        self.represent_in_base64 = kwargs.pop('represent_in_base64', False)
        super().__init__(*args, **kwargs)

    def to_internal_value(self, base64_data):
        # Check if this is a base64 string
        if base64_data in self.EMPTY_VALUES:
            return None

        if isinstance(base64_data, str):
            file_mime_type = None

            # Strip base64 header, get mime_type from base64 header.
            if ';base64,' in base64_data:
                header, base64_data = base64_data.split(';base64,')
                if self.trust_provided_content_type:
                    file_mime_type = header.replace('data:', '')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(base64_data)
            except (TypeError, binascii.Error, ValueError):
                raise ValidationError(self.invalid_file_message)

            # Generate file name:
            file_name = self.get_file_name(decoded_file)

            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            if file_extension not in self.allowed_types:
                raise ValidationError(self.invalid_type_message)

            complete_file_name = file_name + '.' + file_extension
            data = SimpleUploadedFile(
                name=complete_file_name,
                content=decoded_file,
                content_type=file_mime_type
            )

            return super().to_internal_value(data)

        raise ValidationError(
            f'Invalid type. This is not an base64 string: {type(base64_data)}'
        )

    def get_file_extension(self, filename, decoded_file):
        raise NotImplementedError

    def get_file_name(self, decoded_file):
        return str(uuid.uuid4())

    def to_representation(self, file):
        if self.represent_in_base64:
            if not file:
                return ""

            try:
                with open(file.path, "rb") as f:
                    return base64.b64encode(f.read()).decode()
            except Exception:
                raise OSError("Error encoding file")
        else:
            return super().to_representation(file)


class Base64ImageField(Base64FieldMixin, ImageField):
    """
    A django-rest-framework field for handling image-uploads through raw post.
    """
    allowed_types = (
        'jpeg',
        'jpg',
        'png',
        'gif'
    )
    invalid_file_message = 'Please upload a valid image.'
    invalid_type_message = 'The type of the image couldn\'t be determined.'

    def get_file_extension(self, filename, decoded_file):
        try:
            from PIL import Image
        except ImportError:
            raise ImportError('Pillow is not installed.')
        extension = imghdr.what(filename, decoded_file)

        # Try with PIL as fallback if format not detected due
        # to bug in imghdr https://bugs.python.org/issue16512
        if extension is None:
            try:
                image = Image.open(io.BytesIO(decoded_file))
            except OSError:
                raise ValidationError(self.invalid_file_message)

            extension = image.format.lower()

        return 'jpg' if extension == 'jpeg' else extension
