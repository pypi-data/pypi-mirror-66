from typing import Type, List
from django.utils.encoding import force_text
from jutil.dict import choices_label


def get_object_or_none(cls, **kwargs):
    """
    Returns model instance or None if not found.
    :param cls: Class or queryset
    :param kwargs: Filters for get() call
    :return: Object or None
    """
    try:
        qs = cls._default_manager.all() if hasattr(cls, '_default_manager') else cls  # pylint: disable=protected-access
        return qs.get(**kwargs)
    except Exception:
        return None


def get_model_field_label_and_value(instance, field_name: str) -> (str, str):
    """
    Returns model field label and value (as text).
    :param instance: Model instance
    :param field_name: Model attribute name
    :return: (label, value) tuple
    """
    label = field_name
    value = str(getattr(instance, field_name))
    for f in instance._meta.fields:
        if f.attname == field_name:
            label = f.verbose_name
            if hasattr(f, 'choices') and f.choices:
                value = choices_label(f.choices, value)
            break
    return label, force_text(value)


def is_model_field_changed(instance, field_name: str) -> bool:
    """
    Compares model instance field value to value stored in DB.
    If object has not been stored in DB (yet) field is considered unchanged.
    :param instance: Model instance
    :param field_name: Model attribute name
    :return: True if field value has been changed compared to value stored in DB.
    """
    assert hasattr(instance, field_name)
    if not hasattr(instance, 'pk') or instance.pk is None:
        return False
    qs = instance.__class__.objects.all()
    params = {'pk': instance.pk, field_name: getattr(instance, field_name)}
    return qs.filter(**params).first() is None


def get_model_keys(instance, cls: Type or None = None,
                   exclude_fields: tuple = ('id',), base_class_suffix: str = '_ptr') -> List[str]:
    if cls is None:
        cls = instance.__class__
    return [f.name for f in cls._meta.fields if f.name not in exclude_fields and not f.name.endswith(base_class_suffix)]


def clone_model(instance, cls: Type or None = None, commit: bool = True,
                exclude_fields: tuple = ('id',), base_class_suffix: str = '_ptr', **kw):
    """
    Assigns model fields to new object. Ignores exclude_fields list and
    attributes ending with pointer suffix (default '_ptr')
    :param instance: Instance to copy
    :param cls: Class name
    :param commit: Save or not
    :param exclude_fields: List of fields to exclude
    :param base_class_suffix: End of name for base class pointers, e.g. model Car(Vehicle) has implicit vehicle_ptr
    :return: New instance
    """
    if cls is None:
        cls = instance.__class__
    keys = get_model_keys(instance, cls=cls, exclude_fields=exclude_fields, base_class_suffix=base_class_suffix)
    new_instance = cls()
    for k in keys:
        setattr(new_instance, k, getattr(instance, k))
    for k, v in kw.items():
        setattr(new_instance, k, v)
    if commit:
        new_instance.save()
    return new_instance
