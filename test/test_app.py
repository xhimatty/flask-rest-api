from flask_jwt_extended import create_access_token

def test_product_list_requires_authentication(client):
    response = client.get('/products/')

    assert response.status_code == 401

def test_admin_can_access_product_list(client):
    access_token = create_access_token(identity=str(1), additional_claims={'role': 'admin'})
    response = client.get(
        '/products/',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == 200

def test_regular_user_cannot_access_product_list(client):
    access_token = create_access_token(identity=str(1), additional_claims={'role': 'user'})
    response = client.get(
        '/products/',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == 403