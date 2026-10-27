import importlib

from llm import FakeLLM

lesson = importlib.import_module("01_hello_brain")


def test_dataset_loads_and_labels_are_known():
    emails = lesson.load_emails()
    assert len(emails) >= 30
    assert {e["label"] for e in emails} <= set(lesson.CATEGORIES)


def test_normalize_handles_messy_llm_output():
    assert lesson.normalize("Category: Alert.") == "alert"
    assert lesson.normalize("**change request**") == "change_request"
    assert lesson.normalize("I am not sure") == "unknown"


def test_classify_sends_system_prompt_and_email_to_model():
    llm = FakeLLM(replies=["incident"])
    email = lesson.load_emails()[5]

    assert lesson.classify(email, llm) == "incident"

    sent = llm.calls[0]["messages"]
    assert sent[0]["role"] == "system" and "phishing" in sent[0]["content"]
    assert email["subject"] in sent[1]["content"]


def test_keyword_baseline_gets_obvious_alert_right():
    alert = lesson.load_emails()[0]
    assert lesson.classify(alert, FakeLLM()) == "alert"
