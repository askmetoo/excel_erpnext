import uuid


def autoname(doc, method=None):
	doc.name = str(uuid.uuid4())
