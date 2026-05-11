from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_analyze_text():
    r = client.post("/analyze", data={"text": "In conclusion, it is important to note "
                                              "that this plays a crucial role."})
    assert r.status_code == 200
    body = r.json()
    assert "ai_probability" in body
    assert body["source"] == "text"


def test_analyze_rejects_empty():
    r = client.post("/analyze", data={})
    assert r.status_code == 400


def test_report_pdf():
    a = client.post("/analyze", data={"text": "This is a short sample sentence."})
    assert a.status_code == 200
    r = client.post("/report", json={"result": a.json(), "case_name": "demo"})
    assert r.status_code == 200
    assert r.headers["content-type"] == "application/pdf"
    assert r.content[:4] == b"%PDF"
