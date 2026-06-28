from urllib.parse import quote


def test_get_activities(client):
    # Arrange: client fixture provides a fresh TestClient

    # Act
    response = client.get('/activities')

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert 'Chess Club' in data


def test_signup_success(client):
    # Arrange
    activity = 'Chess Club'
    email = 'new.student@mergington.edu'

    # Act
    response = client.post(f"/activities/{quote(activity)}/signup?email={quote(email)}")

    # Assert
    assert response.status_code == 200
    body = response.json()
    assert 'Signed up' in body.get('message', '')

    # Verify participant recorded
    activities = client.get('/activities').json()
    assert email in activities[activity]['participants']


def test_signup_duplicate(client):
    # Arrange
    activity = 'Programming Class'
    email = 'duplicate.student@mergington.edu'

    # Act - first signup should succeed
    r1 = client.post(f"/activities/{quote(activity)}/signup?email={quote(email)}")
    assert r1.status_code == 200

    # Act - second signup should be rejected
    r2 = client.post(f"/activities/{quote(activity)}/signup?email={quote(email)}")

    # Assert
    assert r2.status_code == 400
    assert 'already' in r2.json().get('detail', '').lower()


def test_signup_full(client):
    # Arrange: create a small activity with max_participants = 1
    import importlib
    app_module = importlib.import_module('src.app')
    app_module.activities['Tiny Club'] = {
        'description': 'A tiny club',
        'schedule': 'Now',
        'max_participants': 1,
        'participants': ['filled@mergington.edu']
    }

    # Act
    response = client.post('/activities/Tiny%20Club/signup?email=new@mergington.edu')

    # Assert
    assert response.status_code == 400
    assert 'full' in response.json().get('detail', '').lower()


def test_root_redirects_to_static(client):
    # Arrange/Act
    response = client.get('/', follow_redirects=False)

    # Assert: Redirect to /static/index.html
    assert response.status_code in (302, 307)
    assert response.headers.get('location') == '/static/index.html'
