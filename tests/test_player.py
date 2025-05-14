player_payload = {
    # TODO
    ...
}

bearer_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJib3NzcyIsImV4cCI6MTc0NzIzNDIxOH0.Y8Br0wADXD1lvboXLUH6XRjdp8pPzbI3jzqzPtOAGj0"

def test_create_club2(client, app, db_session):
    response = client.post(
        "/club",
        json=player_payload,
        headers={"Authorization": f"Bearer {bearer_token}"}
    )

    assert response.status_code == 200