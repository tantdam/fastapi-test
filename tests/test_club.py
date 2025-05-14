club_payload = {
    "name": "NK Nogomet",
    "city": "Zagreb",
    "country": "Croatia",
    "league": "HNL"
}

# bearer_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJib3NzcyIsImV4cCI6MTc0NzIzNDIxOH0.Y8Br0wADXD1lvboXLUH6XRjdp8pPzbI3jzqzPtOAGj0"

def test_create_club2(client, app, override_admin):
    response = client.post(
        "/club",
        json=club_payload
    )

    assert response.status_code == 200