from djpaypal.djpay.serializers import ScopeSerializer

def test_scope_serializer(db,single_scope_factory):
    scope = single_scope_factory.create()
    serializer = ScopeSerializer(scope)
    assert serializer.data["name"] == scope.name
    assert serializer.data == {"id":1,"name":scope.name}

