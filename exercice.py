#!/usr/bin/env python
# -*- coding: utf-8 -*-


def check_brackets(text, brackets):
	opening_brackets = dict(zip(brackets[0::2], brackets[1::2]))
	closing_brackets = dict(zip(brackets[1::2], brackets[0::2]))

	bracket_stack = []
	for chr in text:
		if chr in opening_brackets:
			bracket_stack.append(chr)
		elif chr in closing_brackets:
			if len(bracket_stack) == 0 or bracket_stack[-1] != closing_brackets[chr]:
				return False
			bracket_stack.pop()

	return len(bracket_stack) == 0

def remove_comments(full_text, comment_start, comment_end):
	while True:
		index_start = full_text.find(comment_start)										#Trouver le prochain début de commentaire
		index_end = full_text.find(comment_end)   										#Trouver la prochaine fin de commentaire
		if index_end == -1 and index_start == -1:										#Si l'on trouve aucun des deux
			return full_text
		if index_end < index_start or (index_start == -1) != (index_end == -1):				#Si fermermeture précède ouverture ou aucune fin trouvée
			return None
		full_text = full_text[: index_start] + full_text[index_end + len(comment_end) :]			#Enlever le commentaire de la string
	return full_text

def get_tag_prefix(text, opening_tags, closing_tags):
	for t in zip(opening_tags,closing_tags):
		if text.startswith(t[0]):
			return (t[0], None)
		if text.startswith(t[1]):
			return (None, t[1])

	return (None, None)

def check_tags(full_text, tag_names, comment_tags):
	text= remove_comments(full_text, *comment_tags)
	if text is None:
		return False

	otags = {f"<{name}>": f"</{name}>" for name in tag_names}
	ctags = dict((v,k) for k,v in otags.items())

	tag_stack = []
	while len(text) != 0:
		tag = get_tag_prefix(text, otags, ctags)
		if tag[0] is not None:
			tag_stack.append(tag[0])
			text = text[len(tag[0]):]
		elif tag[1] is not None:
			if len(tag_stack) == 0 or tag_stack[-1] != ctags[tag[1]]:
				return False
			tag_stack.pop()
			text = text[len(tag[1]):]
		else:
			text = text[1:]
	return len(tag_stack) == 0



if __name__ == "__main__":
	brackets = ("(", ")", "{", "}")
	yeet = "(yeet){yeet}"
	yeeet = "({yeet})"
	yeeeet = "({yeet)}"
	yeeeeet = "(yeet"
	print(check_brackets(yeet, brackets))
	print(check_brackets(yeeet, brackets))
	print(check_brackets(yeeeet, brackets))
	print(check_brackets(yeeeeet, brackets))
	print()

	spam = "Hello, /* OOGAH BOOGAH */world!"
	eggs = "Hello, /* OOGAH BOOGAH world!"
	parrot = "Hello, OOGAH BOOGAH*/ world!"
	print(remove_comments(spam, "/*", "*/"))
	print(remove_comments(eggs, "/*", "*/"))
	print(remove_comments(parrot, "/*", "*/"))
	print()

	otags = ("<head>", "<body>", "<h1>")
	ctags = ("</head>", "</body>", "</h1>")
	print(get_tag_prefix("<body><h1>Hello!</h1></body>", otags, ctags))
	print(get_tag_prefix("<h1>Hello!</h1></body>", otags, ctags))
	print(get_tag_prefix("Hello!</h1></body>", otags, ctags))
	print(get_tag_prefix("</h1></body>", otags, ctags))
	print(get_tag_prefix("</body>", otags, ctags))
	print()

	spam = (
		"<html>"
		"  <head>"
		"    <title>"
		"      <!-- Ici j'ai écrit qqch -->"
		"      Example"
		"    </title>"
		"  </head>"
		"  <body>"
		"    <h1>Hello, world</h1>"
		"    <!-- Les tags vides sont ignorés -->"
		"    <br>"
		"    <h1/>"
		"  </body>"
		"</html>"
	)
	eggs = (
		"<html>"
		"  <head>"
		"    <title>"
		"      <!-- Ici j'ai écrit qqch -->"
		"      Example"
		"    <!-- Il manque un end tag"
		"    </title>-->"
		"  </head>"
		"</html>"
	)
	parrot = (
		"<html>"
		"  <head>"
		"    <title>"
		"      Commentaire mal formé -->"
		"      Example"
		"    </title>"
		"  </head>"
		"</html>"
	)
	tags = ("html", "head", "title", "body", "h1")
	comment_tags = ("<!--", "-->")
	print(check_tags(spam, tags, comment_tags))
	print(check_tags(eggs, tags, comment_tags))
	print(check_tags(parrot, tags, comment_tags))
	print()

