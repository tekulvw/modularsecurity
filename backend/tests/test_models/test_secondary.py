from models.secondary import Secondary


def test_create(random_owner, user_factory):
    other = user_factory.get()
    system = random_owner.system_key.get()
    sec = Secondary.create(other, system)
    sec.put()

    assert sec.system_key == system.key
    assert sec.user_key == other.key


def test_from_id(random_secondary):
    id_ = random_secondary.key.integer_id()

    assert Secondary.from_id(id_) == random_secondary


def test_from_user(random_secondary):
    random_user = random_secondary.user_key.get()

    users = Secondary.from_user(random_user)

    assert len(users) > 0
    assert all(sec.user_key == random_user.key for sec in users)


def test_from_system(random_secondary):
    system = random_secondary.system_key.get()

    assert random_secondary in Secondary.from_system(system)


def test_from_user_system(random_secondary):
    user = random_secondary.user_key.get()
    system = random_secondary.system_key.get()

    assert random_secondary == Secondary.from_system_user(system, user)
