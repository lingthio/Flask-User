from ..tokens import TokenManager

def test_encrypt_16byte():
    manager = TokenManager()
    manager.setup('test')

    encrypted = manager.encrypt_id(123)
    assert len(encrypted) == 22

    id = manager.decrypt_id(encrypted)
    assert id == 123

def test_encrypt_32byte():
    manager = TokenManager()
    manager.setup('test')

    encrypted = manager.encrypt_id(12312313234555544433)
    assert len(encrypted) == 43

    id = manager.decrypt_id(encrypted)
    assert id == 12312313234555544433
