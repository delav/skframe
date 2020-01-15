from google.protobuf.descriptor import FieldDescriptor as FD


def str2bin(strings):
    """
    把字符串转化为二进制数据
    """
    byte = bytearray(strings)
    lists = []
    for i in range(len(byte)):
        lists.append(byte[i])
    return lists


def dict2pb(cls, adict, strict=False):
    """
    把字典转为ProtoBuf类
    """
    obj = cls()
    for field in obj.DESCRIPTOR.fields:
        if field.label != field.LABEL_REQUIRED:
            continue
        if not field.has_default_value:
            continue
        if field.name not in adict:
            raise Exception('Field "%s" missing from descriptor dictionary.' % field.name)
    field_names = set([field.name for field in obj.DESCRIPTOR.fields])
    if strict:
        for key in adict.keys():
            if key not in field_names:
                raise Exception('Key "%s" can not be mapped to field in %s class.' % (key, type(obj)))
    for field in obj.DESCRIPTOR.fields:
        if field.name not in adict:
            continue
        msg_type = field.message_type
        if field.label == FD.LABEL_REPEATED:
            if field.type == FD.TYPE_MESSAGE:
                for sub_dict in adict[field.name]:
                    item = getattr(obj, field.name).add()
                    item.CopyFrom(dict2pb(msg_type._concrete_class, sub_dict))
            else:
                map(getattr(obj, field.name).append, adict[field.name])
        else:
            if field.type == FD.TYPE_MESSAGE:
                value = dict2pb(msg_type._concrete_class, adict[field.name])
                getattr(obj, field.name).CopyFrom(value)
            else:
                setattr(obj, field.name, adict[field.name])
    return obj


def pb2dict(obj):
    """
    把ProtoBuf类转化为字典
    """
    adict = {}
    if not obj.IsInitialized():
        return None
    for field in obj.DESCRIPTOR.fields:
        # 如果不是复合结构
        if field.label != FD.LABEL_REPEATED:
            if not field.type == FD.TYPE_MESSAGE:
                adict[field.name] = getattr(obj, field.name)
            else:
                value = pb2dict(getattr(obj, field.name))
                adict[field.name] = value
                if value:
                    adict[field.name] = value
                else:
                    adict[field.name] = ''
        else:
            if field.type == FD.TYPE_MESSAGE:
                ob_name = field.message_type.name
                ob = eval(ob_name + '()')
                bdict = pb2dict(ob)
                adict[field.name] = bdict
            else:
                adict[field.name] = [v for v in getattr(obj, field.name)]
    return adict


class Dict2Obj(dict):
    """
    把字典转化为对象
    """

    def __init__(self, *args, **kwargs):
        super(Dict2Obj, self).__init__(*args, **kwargs)

    def __getattr__(self, key):
        value = self.get(key)
        if isinstance(value, dict):
            value = Dict2Obj(value)
        if isinstance(value, list):
            result = []
            for item in value:
                if isinstance(item, dict):
                    result.append(Dict2Obj(item))
                result.append(item)
            value = result
        return value

    def __setattr__(self, key, value):
        self[key] = value
