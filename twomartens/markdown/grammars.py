# coding=utf-8

"""markdown.grammars: Contains the grammars for markdown."""
import modgrammar

grammar_whitespace_mode = "optional"
grammar_whitespace = modgrammar.WS_NOEOL


class Heading(modgrammar.Grammar):
    """Defines the grammar for a heading."""
    grammar = (modgrammar.BOL, modgrammar.REPEAT(modgrammar.L("#"), min=1, max=6),
               modgrammar.REST_OF_LINE, modgrammar.EOL)

    def grammar_elem_init(self, sessiondata):
        """Saves the headline for later use."""
        self.text = self[3].string
        hashtags = self[1].string
        self.tag = "h" + str(len(hashtags))


class EmptyLine(modgrammar.Grammar):
    """Defines the grammar for an empty line."""
    grammar = (modgrammar.BOL, modgrammar.EOL)
    grammar_whitespace_mode = "explicit"


class Bold(modgrammar.Grammar):
    """Defines the grammar for bold text."""
    grammar = (modgrammar.L(" **"), modgrammar.WORD("\w \t", fullmatch=True, escapes=True), modgrammar.L("** "))

    def grammar_elem_init(self, sessiondata):
        """Saves the text for later use."""
        self.text = self[1].string
        self.tag = "b"


class Italic(modgrammar.Grammar):
    """Defines the grammar for italic text."""
    grammar = (modgrammar.L(" *"), modgrammar.WORD("\w \t", fullmatch=True, escapes=True), modgrammar.L("* "))

    def grammar_elem_init(self, sessiondata):
        """Saves the text for later use."""
        self.text = self[1].string
        self.tag = "i"


class QuoteLine(modgrammar.Grammar):
    """Defines the grammar for a single line quote."""
    grammar = (modgrammar.BOL, modgrammar.L(">"), modgrammar.REST_OF_LINE, modgrammar.EOL)

    def grammar_elem_init(self, sessiondata):
        """Saves the text for later use."""
        self.quoteLine = self[2].string


class Quote(modgrammar.Grammar):
    """Defines the grammar for a quote."""
    grammar = (modgrammar.REPEAT(QuoteLine, min=1))

    def grammar_elem_init(self, sessiondata):
        """Saves the text for later use."""
        quote = ""
        for elem in self.find_all(QuoteLine):
            quote = quote + " " + elem.quoteLine

        self.text = quote
        self.tag = "quote"


class ListItem(modgrammar.Grammar):
    """Defines the grammar for a list item."""
    grammar = (modgrammar.BOL, modgrammar.L("* "), modgrammar.REST_OF_LINE)

    def grammar_elem_init(self, sessiondata):
        """Saves the text for later use."""
        self.text = self[2].string
        self.tag = "li"


class List(modgrammar.Grammar):
    """Defines the grammar for a list."""
    grammar = (modgrammar.LIST_OF(ListItem, sep=modgrammar.EOL), modgrammar.EOL)

    def grammar_elem_init(self, sessiondata):
        """Saves the text for later use."""
        self.tag = "list"


class SimpleText(modgrammar.Grammar):
    """Defines the grammar for simple text."""
    grammar = (modgrammar.WORD("\S \t", escapes=True, fullmatch=True))

    def grammar_elem_init(self, sessiondata):
        """Saves the text for later use."""
        self.text = self[0].string
        self.tag = "text"


class Text(modgrammar.Grammar):
    """Defines the grammar for normal text."""
    grammar = (modgrammar.REPEAT(modgrammar.OR(Bold, Italic, Quote, SimpleText),
                                 modgrammar.EOL, min=1))


class Paragraph(modgrammar.Grammar):
    """Defines the grammar for a paragraph."""
    grammar = (EmptyLine, Text, modgrammar.OPTIONAL(EmptyLine))

    def grammar_elem_init(self, sessiondata):
        """Saves the text for later use."""
        self.tag = "p"


class MarkdownGrammar(modgrammar.Grammar):
    """Provides the grammar for Markdown."""
    grammar = (modgrammar.REPEAT(modgrammar.OR(Heading, Paragraph, List, EmptyLine)))

    def grammar_elem_init(self, sessiondata):
        """Saves the text for later use."""
        self.content = self[0].string
